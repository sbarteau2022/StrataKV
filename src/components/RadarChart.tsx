import React, { useEffect, useRef } from 'react';

export const RadarChart: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h / 2;
    const radius = Math.min(cx, cy) - 55;

    ctx.clearRect(0, 0, w, h);

    const labels = [
      'RULER 256K', 'NIAH 10/10', 'Corona Def', 'LongBench', 'NoLiMa',
      'SWE-bench', 'SC Reuse', 'Terminal', 'WikiText', 'PG-19',
      'AgentDojo', 'Ultra 3K', 'Metal Bandwidth', 'LongMemEval'
    ];
    const total = labels.length;

    // StrataKV Normalized Scores [0.0 to 1.0]
    const strataScores = [0.94, 1.00, 1.00, 0.65, 0.69, 0.39, 0.85, 0.46, 0.98, 0.97, 0.98, 1.00, 0.72, 0.98];
    // Baseline Full Attention (Cliffs at OOM)
    const baselineScores = [0.50, 0.50, 0.01, 0.40, 0.62, 0.14, 0.12, 0.10, 0.99, 0.98, 0.21, 0.11, 0.10, 0.89];

    // Background web circles
    ctx.strokeStyle = 'rgba(121, 121, 107, 0.25)';
    ctx.lineWidth = 1;
    for (let r = 0.2; r <= 1.0; r += 0.2) {
      ctx.beginPath();
      for (let i = 0; i < total; i++) {
        const angle = (i * 2 * Math.PI / total) - Math.PI / 2;
        const x = cx + radius * r * Math.cos(angle);
        const y = cy + radius * r * Math.sin(angle);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.stroke();
    }

    // Axis lines & labels
    ctx.fillStyle = '#C0BDB2';
    ctx.font = '10px Georgia, serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (let i = 0; i < total; i++) {
      const angle = (i * 2 * Math.PI / total) - Math.PI / 2;
      const x = cx + radius * Math.cos(angle);
      const y = cy + radius * Math.sin(angle);

      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.stroke();

      const lx = cx + (radius + 24) * Math.cos(angle);
      const ly = cy + (radius + 24) * Math.sin(angle);
      ctx.fillText(labels[i], lx, ly);
    }

    // Baseline Polygon (Error / Warning tint)
    ctx.beginPath();
    for (let i = 0; i < total; i++) {
      const angle = (i * 2 * Math.PI / total) - Math.PI / 2;
      const val = baselineScores[i];
      const x = cx + radius * val * Math.cos(angle);
      const y = cy + radius * val * Math.sin(angle);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(237, 176, 166, 0.18)';
    ctx.fill();
    ctx.strokeStyle = 'rgba(237, 176, 166, 0.85)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // StrataKV Polygon (Gold accent)
    ctx.beginPath();
    for (let i = 0; i < total; i++) {
      const angle = (i * 2 * Math.PI / total) - Math.PI / 2;
      const val = strataScores[i];
      const x = cx + radius * val * Math.cos(angle);
      const y = cy + radius * val * Math.sin(angle);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(221, 194, 140, 0.25)';
    ctx.fill();
    ctx.strokeStyle = '#DDC28C';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Vertices
    for (let i = 0; i < total; i++) {
      const angle = (i * 2 * Math.PI / total) - Math.PI / 2;
      const val = strataScores[i];
      const x = cx + radius * val * Math.cos(angle);
      const y = cy + radius * val * Math.sin(angle);
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, 2 * Math.PI);
      ctx.fillStyle = '#B8CDB1';
      ctx.fill();
      ctx.strokeStyle = '#F0EADD';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center">
      <canvas ref={canvasRef} width={500} height={420} className="max-w-full" />
      <div className="flex flex-wrap justify-center gap-4 text-xs pt-3 border-t border-[rgba(121,121,107,0.25)] w-full">
        <span className="flex items-center gap-1.5 text-[var(--color-gold)] font-semibold">
          <span className="w-2.5 h-2.5 rounded-full bg-[var(--color-gold)]"></span> StrataKV Active (Optimal)
        </span>
        <span className="flex items-center gap-1.5 text-[var(--color-muted)] font-medium">
          <span className="w-2.5 h-2.5 rounded-full bg-[rgba(121,121,107,0.6)]"></span> Full Attention (OOM Cliff)
        </span>
        <span className="flex items-center gap-1.5 text-[var(--color-error)] font-medium">
          <span className="w-2.5 h-2.5 rounded-full bg-[var(--color-error)]"></span> Baseline Sliding Window
        </span>
      </div>
    </div>
  );
};
