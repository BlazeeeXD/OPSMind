import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { Terminal } from 'lucide-react';

interface LoadingProps {
  jobId: string;
  onComplete: () => void;
}

const STAGES = {
  initializing: "Booting investigation engine",
  extracting_evidence: "Extracting telemetry and parsing logs",
  analyzing_root_cause: "AI models analyzing evidence correlations",
  generating_remediation: "Synthesizing remediation steps",
  building_timeline: "Constructing chronological event timeline",
  finalizing_report: "Assembling final JSON report",
  completed: "Investigation successful"
};

type StageKey = keyof typeof STAGES;

export default function LoadingTerminal({ jobId, onComplete }: LoadingProps) {
  const [currentStage, setCurrentStage] = useState<StageKey>('initializing');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const pollInterval = setInterval(async () => {
      try {
        const job = await api.getJobStatus(jobId);
        
        if (job.status === 'failed') {
          setError(job.error || "Unknown error occurred.");
          clearInterval(pollInterval);
          return;
        }

        setCurrentStage(job.stage as StageKey);

        if (job.status === 'success' || job.stage === 'completed') {
          clearInterval(pollInterval);
          // Small delay before showing the report so the user sees the final checkmark
          setTimeout(onComplete, 800); 
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }, 1000); // Poll every 1 second

    return () => clearInterval(pollInterval);
  }, [jobId, onComplete]);

  // Determine if a step is done, active, or pending
  const getStepStatus = (stepKey: StageKey) => {
    const stageOrder = Object.keys(STAGES);
    const currentIndex = stageOrder.indexOf(currentStage);
    const stepIndex = stageOrder.indexOf(stepKey);

    if (stepIndex < currentIndex) return 'done';
    if (stepIndex === currentIndex) return 'active';
    return 'pending';
  };

  return (
    <div className="w-full max-w-2xl mx-auto border border-terminal-border bg-terminal-panel p-6 shadow-glow-cyan">
      <div className="flex items-center text-terminal-cyan mb-6 pb-4 border-b border-terminal-border/50">
        <Terminal className="w-5 h-5 mr-2" />
        <h3 className="font-bold tracking-widest">AI INVESTIGATION PROTOCOL ACTIVE</h3>
      </div>

      {error ? (
        <div className="text-terminal-red">
          <span className="animate-pulse">FATAL ERROR:</span> {error}
        </div>
      ) : (
        <div className="space-y-4 font-mono">
          {Object.entries(STAGES).map(([key, text]) => {
            if (key === 'completed') return null; // Hide the final state from the list

            const status = getStepStatus(key as StageKey);
            
            return (
              <div key={key} className="flex items-center text-sm">
                <span className="w-8 shrink-0">
                  {status === 'done' && <span className="text-terminal-green">[✓]</span>}
                  {status === 'active' && <span className="text-terminal-yellow animate-pulse">[*]</span>}
                  {status === 'pending' && <span className="text-terminal-dim">[ ]</span>}
                </span>
                
                <span className={`
                  ${status === 'done' ? 'text-terminal-dim' : ''}
                  ${status === 'active' ? 'text-white shadow-glow-cyan' : ''}
                  ${status === 'pending' ? 'text-terminal-dim opacity-50' : ''}
                `}>
                  {text}...
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}