import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { InvestigationReport } from '../types';
import { ShieldAlert, CheckCircle2, Clock } from 'lucide-react';

interface ReportProps {
  incidentId: number;
}

export default function ReportDashboard({ incidentId }: ReportProps) {
  const [report, setReport] = useState<InvestigationReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getReport(incidentId)
      .then(data => {
        setReport(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load report", err);
        setLoading(false);
      });
  }, [incidentId]);

  if (loading) return <div className="text-terminal-cyan animate-pulse">DECRYPTING REPORT DATA...</div>;
  if (!report) return <div className="text-terminal-red">ERROR: REPORT NOT FOUND OR CORRUPTED.</div>;

  return (
    <div className="w-full h-full flex flex-col pt-4 pb-24 pr-4">
      {/* Header */}
      <div className="mb-6 flex justify-between items-end border-b border-terminal-border pb-4">
        <div>
          <div className="text-terminal-red text-xs font-bold tracking-widest mb-1">
            [{report.summary.severity.toUpperCase()}] INCIDENT RESOLVED
          </div>
          <h2 className="text-2xl font-bold text-white">{report.summary.title}</h2>
          <div className="text-terminal-dim text-sm mt-1">Target: {report.summary.affected_service}</div>
        </div>
        <div className="text-right">
          <div className="text-terminal-dim text-xs tracking-widest">REPORT GENERATED</div>
          <div className="text-terminal-cyan font-mono text-sm">{new Date(report.created_at).toLocaleTimeString()}</div>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-12 gap-6 overflow-hidden">
        
        {/* Left Column: Timeline (Col Span 4) */}
        <div className="col-span-4 flex flex-col h-full bg-terminal-panel/30 border border-terminal-border p-4 overflow-y-auto">
          <h3 className="text-terminal-dim text-xs font-bold tracking-widest mb-4 flex items-center">
            <Clock className="w-4 h-4 mr-2" /> EVENT TIMELINE
          </h3>
          <div className="space-y-6 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-terminal-border before:to-transparent">
            {report.timeline.map((item, idx) => (
              <div key={idx} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                <div className="flex items-center justify-center w-5 h-5 rounded-full border border-terminal-cyan bg-terminal-bg shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-glow-cyan z-10">
                  <div className="w-1.5 h-1.5 bg-terminal-cyan rounded-full"></div>
                </div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-3 rounded border border-terminal-border bg-terminal-panel/50 text-left">
                  <div className="text-terminal-cyan font-mono text-xs mb-1">{item.time}</div>
                  <div className="text-white text-xs leading-relaxed">{item.event}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: AI Analysis (Col Span 8) */}
        <div className="col-span-8 flex flex-col gap-6 h-full overflow-y-auto">
          
          {/* Root Causes */}
          <div className="border border-terminal-border bg-terminal-panel/30 p-5">
            <h3 className="text-terminal-dim text-xs font-bold tracking-widest mb-4 flex items-center">
              <ShieldAlert className="w-4 h-4 mr-2 text-terminal-red" /> ROOT CAUSE ANALYSIS
            </h3>
            <div className="space-y-4">
              {report.root_causes.causes.map((cause, idx) => (
                <div key={idx} className={`p-4 border ${idx === 0 ? 'border-terminal-red/50 bg-terminal-red/5' : 'border-terminal-border'}`}>
                  <div className="flex justify-between items-start mb-2">
                    <h4 className={`font-bold ${idx === 0 ? 'text-terminal-red text-lg' : 'text-terminal-yellow'}`}>
                      {idx === 0 ? 'PRIMARY: ' : 'SECONDARY: '}{cause.cause}
                    </h4>
                    <span className="text-terminal-cyan font-mono text-sm border border-terminal-cyan/30 px-2 py-0.5">
                      CONFIDENCE: {cause.confidence}%
                    </span>
                  </div>
                  <p className="text-terminal-dim text-sm leading-relaxed">{cause.reasoning}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Remediation Plan */}
          <div className="border border-terminal-border bg-terminal-panel/30 p-5">
            <h3 className="text-terminal-dim text-xs font-bold tracking-widest mb-4 flex items-center">
              <CheckCircle2 className="w-4 h-4 mr-2 text-terminal-green" /> REMEDIATION PLAN
            </h3>
            
            <div className="flex gap-4 mb-6">
              <div className="flex-1 border border-terminal-border p-3 bg-terminal-bg">
                <div className="text-terminal-dim text-[10px] tracking-widest mb-1">EST. RECOVERY TIME</div>
                <div className="text-terminal-cyan text-sm">{report.recommendations.recovery_time}</div>
              </div>
              <div className="flex-1 border border-terminal-border p-3 bg-terminal-bg">
                <div className="text-terminal-dim text-[10px] tracking-widest mb-1">EXECUTION RISK</div>
                <div className="text-terminal-yellow text-sm">{report.recommendations.risk}</div>
              </div>
            </div>

            <ul className="space-y-3">
              {report.recommendations.actions.map((action, idx) => (
                <li key={idx} className="flex items-start text-sm">
                  <span className="text-terminal-cyan mr-3 font-mono">[{idx + 1}]</span>
                  <span className="text-white leading-relaxed">{action}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}