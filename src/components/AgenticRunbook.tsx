import React, { useState, useEffect } from 'react';
import { Terminal, Cpu, Wind, CheckCircle2, Play } from 'lucide-react';

export const AgenticRunbook: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      id: 'orchestration',
      title: '1. Orchestration',
      icon: <Cpu className="w-5 h-5" />,
      color: 'text-[var(--color-gold)]',
      bgColor: 'bg-[rgba(221,194,140,0.1)]',
      borderColor: 'border-[var(--color-gold)]',
      logs: [
        "[SYSTEM] Receiving complex user objective...",
        "[ELLE CONDUCTOR] Objective parsed. Task complexity: HIGH.",
        "[ELLE CONDUCTOR] Provisioning 3 specialized sub-agents.",
        "[STRATAKV] Allocating dedicated Tier 2 memory space on Torus.",
        "[SYSTEM] Swarm initialization complete. Agents online."
      ]
    },
    {
      id: 'execution',
      title: '2. Active Inference',
      icon: <Terminal className="w-5 h-5" />,
      color: 'text-[var(--color-silver)]',
      bgColor: 'bg-[rgba(216,223,225,0.1)]',
      borderColor: 'border-[var(--color-silver)]',
      logs: [
        "[AGENT-1] Executing source code analysis...",
        "[AGENT-2] Running unit tests in background...",
        "[STRATAKV] KV Cache expanding rapidly (24.5 GB / 32 GB).",
        "[AGENT-3] Terminal output received. Error detected in line 42.",
        "[AGENT-1] Refining code based on terminal feedback loop."
      ]
    },
    {
      id: 'exhalation',
      title: '3. Thermodynamic Exhalation',
      icon: <Wind className="w-5 h-5" />,
      color: 'text-[var(--color-bronze)]',
      bgColor: 'bg-[rgba(113,85,52,0.1)]',
      borderColor: 'border-[var(--color-bronze)]',
      logs: [
        "[WARNING] KV Cache threshold reached (80%).",
        "[STRATAKV] Triggering Thermodynamic Exhalation.",
        "[STRATAKV] Pinning core invariant goal to Tier 1 Core.",
        "[STRATAKV] Sweeping 18,400 stale terminal logs to Tier 3 Exhale.",
        "[STRATAKV] Tier 2 Basin cleared. 0.92ms zero-copy overhead. Agents uninterrupted."
      ]
    },
    {
      id: 'termination',
      title: '4. Termination & Checkpoint',
      icon: <CheckCircle2 className="w-5 h-5" />,
      color: 'text-[var(--color-success)]',
      bgColor: 'bg-[rgba(184,205,177,0.1)]',
      borderColor: 'border-[var(--color-success)]',
      logs: [
        "[SYSTEM] Objective criteria met. All tests passing.",
        "[ELLE CONDUCTOR] Spinning down sub-agents.",
        "[STRATAKV] Committing final state vector to disk.",
        "[SYSTEM] Swarm offline.",
        "[BILLING] Total cloud API cost for 4.2 million tokens: $0.00."
      ]
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % steps.length);
    }, 4000);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="max-w-6xl mx-auto px-6 pt-12 pb-24">
      <div className="text-center space-y-4 mb-16">
        <h2 className="font-serif text-4xl md:text-5xl text-[var(--color-ivory)]">Agentic Runbook</h2>
        <p className="text-[var(--color-muted)] text-lg max-w-2xl mx-auto">
          The operational lifecycle of a Sovereign Agent Swarm running on the StrataKV Architecture.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* LEFT COLUMN: TIMELINE */}
        <div className="space-y-6">
          {steps.map((step, idx) => {
            const isActive = idx === activeStep;
            return (
              <div 
                key={step.id}
                onClick={() => setActiveStep(idx)}
                className={`glass-card p-6 rounded-2xl cursor-pointer transition-all duration-300 border-l-4 ${isActive ? step.borderColor + ' bg-[rgba(255,255,255,0.02)]' : 'border-transparent opacity-50 hover:opacity-80'}`}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center ${isActive ? step.bgColor : 'bg-transparent'} ${isActive ? step.color : 'text-[var(--color-muted)]'}`}>
                    {step.icon}
                  </div>
                  <h3 className={`font-serif text-2xl ${isActive ? 'text-[var(--color-ivory)]' : 'text-[var(--color-muted)]'}`}>
                    {step.title}
                  </h3>
                </div>
              </div>
            );
          })}
        </div>

        {/* RIGHT COLUMN: TERMINAL */}
        <div className="glass-card rounded-2xl p-6 font-mono text-sm relative overflow-hidden flex flex-col h-[500px]">
          <div className="flex items-center gap-2 mb-6 border-b border-[rgba(255,255,255,0.1)] pb-4">
            <div className="flex gap-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
              <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
            </div>
            <span className="ml-4 text-[var(--color-muted)] text-xs">stratakv-daemon ~ zsh</span>
          </div>
          
          <div className="flex-1 overflow-y-auto space-y-4 flex flex-col justify-center">
            {steps[activeStep].logs.map((log, i) => (
              <div 
                key={i} 
                className="opacity-0 animate-fade-in-up"
                style={{ animationDelay: `${i * 0.4}s`, animationFillMode: 'forwards' }}
              >
                <span className={
                  log.includes('[SYSTEM]') ? 'text-[var(--color-silver)]' :
                  log.includes('[ELLE CONDUCTOR]') ? 'text-[var(--color-gold)]' :
                  log.includes('[WARNING]') ? 'text-red-400' :
                  log.includes('[STRATAKV]') ? 'text-[var(--color-success)]' :
                  'text-[var(--color-ivory)]'
                }>
                  {log}
                </span>
              </div>
            ))}
          </div>
          
          <style dangerouslySetInnerHTML={{__html: `
            @keyframes fadeInUp {
              from { opacity: 0; transform: translateY(10px); }
              to { opacity: 1; transform: translateY(0); }
            }
            .animate-fade-in-up {
              animation: fadeInUp 0.5s ease-out;
            }
          `}} />
        </div>
      </div>
    </div>
  );
};
