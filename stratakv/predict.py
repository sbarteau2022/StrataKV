"""
StrataKV Prediction Operator P
==============================
Port of the Rust harness prediction operator (harness-dhng/src/predict.rs) and
worker (src/predict.ts) into StrataKV.

Provides one-step forecasting with residual-as-surprise for the Meta/Orchestrator
in the Agentic AI Runbook:
- Competitive multi-method forecasting: Persistence vs EMA (alpha=0.3) vs AR(2)
- Best-of selected by running one-step MAE (Hyndman & Koehler 2006 out-of-sample skill)
- Welford running moments for residual z-score calculation
- Precision-weighted prediction error / surprise z
- Token spend envelope prediction for Active Inference steering
"""

import math
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

PREDICT_EMA_ALPHA = 0.3
PREDICT_WINDOW = 64
PREDICT_MIN_AR_HISTORY = 6
PREDICT_MIN_Z_COUNT = 3
PREDICT_Z_STD_FLOOR = 1e-9


class Welford:
    """Welford running moments (z-score BEFORE ingesting observation)."""
    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.m2 = 0.0

    def z_then_update(self, x: float) -> float:
        if self.count >= PREDICT_MIN_Z_COUNT:
            var = self.m2 / (self.count - 1)
            std = math.sqrt(max(var, 0.0))
            z = (x - self.mean) / max(std, PREDICT_Z_STD_FLOOR)
        else:
            z = 0.0

        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        self.m2 += delta * (x - self.mean)
        return float(z)


class RunningMae:
    """Running Mean Absolute Error tracker."""
    def __init__(self):
        self.count = 0
        self.sum_abs = 0.0

    def update(self, abs_err: float):
        self.count += 1
        self.sum_abs += abs(abs_err)

    def mean(self) -> Optional[float]:
        return None if self.count == 0 else self.sum_abs / self.count


def ar1_forecast(series: List[float]) -> Optional[float]:
    """AR(1) with intercept: fallback for singular/ramp series."""
    n = len(series)
    if n < 3:
        return None
    k = n - 1
    sx, sy, sxx, sxy = 0.0, 0.0, 0.0, 0.0
    for t in range(1, n):
        x = series[t - 1]
        y = series[t]
        sx += x
        sy += y
        sxx += x * x
        sxy += x * y
    det = k * sxx - sx * sx
    if abs(det) < 1e-9 * (1.0 + abs(k * sxx)):
        return None
    p = (k * sxy - sx * sy) / det
    c = (sy - p * sx) / k
    forecast = c + p * series[-1]
    return float(forecast) if math.isfinite(forecast) else None


def ar2_forecast(series: List[float]) -> Optional[float]:
    """AR(2) with intercept via Cramer's rule on 3x3 normal equations."""
    n = len(series)
    if n < PREDICT_MIN_AR_HISTORY:
        return None
    s1, s2, sy = 0.0, 0.0, 0.0
    s11, s12, s22 = 0.0, 0.0, 0.0
    s1y, s2y = 0.0, 0.0
    m = n - 2
    for t in range(2, n):
        x1 = series[t - 1]
        x2 = series[t - 2]
        y = series[t]
        s1 += x1
        s2 += x2
        sy += y
        s11 += x1 * x1
        s12 += x1 * x2
        s22 += x2 * x2
        s1y += x1 * y
        s2y += x2 * y

    det = m * (s11 * s22 - s12 * s12) - s1 * (s1 * s22 - s12 * s2) + s2 * (s1 * s12 - s11 * s2)
    if abs(det) < 1e-9 * (1.0 + abs(m * s11 * s22)):
        return ar1_forecast(series)

    det_c = sy * (s11 * s22 - s12 * s12) - s1 * (s1y * s22 - s12 * s2y) + s2 * (s1y * s12 - s11 * s2y)
    det_p1 = m * (s1y * s22 - s12 * s2y) - sy * (s1 * s22 - s12 * s2) + s2 * (s1 * s2y - s1y * s2)
    det_p2 = m * (s11 * s2y - s1y * s12) - s1 * (s1 * s2y - s1y * s2) + sy * (s1 * s12 - s11 * s2)

    c = det_c / det
    p1 = det_p1 / det
    p2 = det_p2 / det
    forecast = c + p1 * series[-1] + p2 * series[-2]
    return float(forecast) if math.isfinite(forecast) else None


class PredictionOperator:
    """
    The Prediction Operator P:
    One-step forecasting with residual-as-surprise for agentic swarms.
    Operates on both scalar series (e.g. cumulative token spend) and
    vector series (e.g. hidden state / key trajectory).
    """
    def __init__(self, dim: int = 1, alpha: float = PREDICT_EMA_ALPHA, window_cap: int = PREDICT_WINDOW):
        self.dim = dim
        self.alpha = alpha
        self.window_cap = max(window_cap, PREDICT_MIN_AR_HISTORY)
        self.history: List[np.ndarray] = []
        self.ema_level: Optional[np.ndarray] = None
        self.mae_persistence = RunningMae()
        self.mae_ema = RunningMae()
        self.mae_ar2 = RunningMae()
        self.welford = Welford()
        self.step_count = 0

    def _forecast_persistence(self) -> Optional[np.ndarray]:
        return self.history[-1].copy() if self.history else None

    def _forecast_ema(self) -> Optional[np.ndarray]:
        return self.ema_level.copy() if self.ema_level is not None else None

    def _forecast_ar2(self) -> Optional[np.ndarray]:
        if len(self.history) < PREDICT_MIN_AR_HISTORY:
            return None
        out = np.zeros(self.dim, dtype=np.float32)
        for d in range(self.dim):
            series = [float(v[d]) for v in self.history]
            f = ar2_forecast(series)
            if f is None:
                return None
            out[d] = f
        return out

    def _choose_method(self) -> str:
        best = "persistence"
        best_mae = self.mae_persistence.mean() or float("inf")
        ema_m = self.mae_ema.mean()
        if ema_m is not None and ema_m < best_mae:
            best = "ema"
            best_mae = ema_m
        ar2_m = self.mae_ar2.mean()
        if ar2_m is not None and ar2_m < best_mae:
            best = "ar2"
        return best

    def step(self, obs: np.ndarray) -> Dict[str, Any]:
        """
        Step P: Forecast next observation using past history, compute surprise,
        then ingest the current observation.
        """
        obs_vec = np.atleast_1d(obs).astype(np.float32)
        if obs_vec.shape[0] != self.dim:
            if self.dim == 1 and obs_vec.size > 0:
                obs_vec = np.array([float(obs_vec.flat[0])], dtype=np.float32)
            else:
                raise ValueError(f"Observation dimension {obs_vec.shape[0]} != {self.dim}")

        method = self._choose_method()
        if method == "persistence":
            forecast = self._forecast_persistence()
        elif method == "ema":
            forecast = self._forecast_ema()
        else:
            forecast = self._forecast_ar2()

        if forecast is not None:
            residual = float(np.linalg.norm(forecast - obs_vec))
            surprise_z = self.welford.z_then_update(residual)
        else:
            residual = 0.0
            surprise_z = 0.0

        # Score candidates for next round
        fp = self._forecast_persistence()
        if fp is not None:
            self.mae_persistence.update(float(np.linalg.norm(fp - obs_vec)))
        fe = self._forecast_ema()
        if fe is not None:
            self.mae_ema.update(float(np.linalg.norm(fe - obs_vec)))
        fa = self._forecast_ar2()
        if fa is not None:
            self.mae_ar2.update(float(np.linalg.norm(fa - obs_vec)))

        # Ingest into history
        if self.ema_level is not None:
            self.ema_level = self.alpha * obs_vec + (1.0 - self.alpha) * self.ema_level
        else:
            self.ema_level = obs_vec.copy()

        self.history.append(obs_vec.copy())
        if len(self.history) > self.window_cap:
            self.history.pop(0)

        self.step_count += 1

        # Predict future envelope (e.g. 50 steps ahead for token spend)
        pred_future = None
        if forecast is not None:
            if method == "ar2" and len(self.history) >= 2:
                slope = float(obs_vec[0] - self.history[-2][0]) if self.dim == 1 else 0.0
                pred_future = float(obs_vec[0] + max(slope, 0.0) * 50.0) if self.dim == 1 else None
            elif self.dim == 1:
                pred_future = float(obs_vec[0] * 1.5)

        return {
            "forecast": forecast,
            "method": method if forecast is not None else "cold_start",
            "residual": residual,
            "surprise_z": surprise_z,
            "predicted_envelope": pred_future,
            "step": self.step_count
        }
