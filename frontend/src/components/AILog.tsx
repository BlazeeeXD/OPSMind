import { TerminalSquare } from 'lucide-react';

export default function AILog() {
  return (
    <div className="absolute bottom-4 right-8 w-80 bg-[#02050A] border border-terminal-border shadow-glow-cyan overflow-hidden z-50">
      <div className="bg-terminal-border/30 px-3 py-1 flex items-center text-[10px] text-terminal-dim font-bold tracking-widest">
        <TerminalSquare className="w-3 h-3 mr-2" />
        AI_INVESTIGATION.LOG
      </div>
      <div className="p-3 text-[10px] font-mono text-terminal-dim space-y-1.5 opacity-80">
        <div className="text-terminal-cyan">{">"} Ingesting operational telemetry...</div>
        <div>{">"} Correlating 50+ metric snapshots...</div>
        <div>{">"} Searching deployment commit history...</div>
        <div className="text-terminal-yellow">{">"} Anomaly detected at T-05:00...</div>
        <div className="text-terminal-green">{">"} Root cause isolated (Confidence: High)</div>
        <div className="text-terminal-cyan animate-pulse">{">"} Awaiting operator action_</div>
      </div>
    </div>
  );
}