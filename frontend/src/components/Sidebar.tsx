import { useEffect, useState } from 'react';
import { AlertCircle, AlertTriangle, Activity, Database, Server, Info } from 'lucide-react';
import { api } from '../api/client';
import type { Incident } from '../types';

interface SidebarProps {
  onSelectIncident: (incident: Incident) => void;
  selectedIncidentId: number | null;
}

export default function Sidebar({ onSelectIncident, selectedIncidentId }: SidebarProps) {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch incidents on load
    api.getIncidents()
      .then(data => {
        setIncidents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError("Failed to connect to Operations API");
        setLoading(false);
      });
  }, []);

  // Helper to grab the right icon based on severity or service
  const getIcon = (severity: string, service: string) => {
    const iconClass = "w-4 h-4 mt-0.5 mr-3 shrink-0";
    if (severity === 'Critical') return <AlertCircle className={`${iconClass} text-terminal-red`} />;
    if (severity === 'High') return <AlertTriangle className={`${iconClass} text-terminal-yellow`} />;
    if (service.includes('db')) return <Database className={`${iconClass} text-terminal-cyan`} />;
    return <Server className={`${iconClass} text-terminal-cyan`} />;
  };

  const getSeverityColor = (severity: string) => {
    if (severity === 'Critical') return 'text-terminal-red';
    if (severity === 'High') return 'text-terminal-yellow';
    if (severity === 'Medium') return 'text-terminal-cyan';
    return 'text-terminal-dim';
  };

  return (
    <div className="flex flex-col h-full p-4">
      {/* Header */}
      <div className="mb-8 mt-2 pb-4 border-b border-terminal-border">
        <h1 className="text-xl font-bold tracking-widest text-white">OPS<span className="text-terminal-cyan">MIND</span></h1>
        <p className="text-xs text-terminal-dim mt-1 uppercase tracking-widest">AI Command Center</p>
      </div>

      {/* List Header */}
      <div className="flex items-center justify-between mb-4">
        <span className="text-xs font-bold text-terminal-dim tracking-widest">ACTIVE INCIDENTS</span>
        <span className="bg-terminal-red/10 text-terminal-red text-[10px] px-2 py-0.5 rounded-sm border border-terminal-red/30">
          {incidents.length} DETECTED
        </span>
      </div>

      {/* The List */}
      <div className="flex flex-col space-y-2 overflow-y-auto">
        {loading && <div className="text-xs text-terminal-dim animate-pulse">Scanning systems...</div>}
        {error && <div className="text-xs text-terminal-red">{error}</div>}
        
        {incidents.map((incident) => {
          const isSelected = selectedIncidentId === incident.id;
          return (
            <button 
              key={incident.id}
              onClick={() => onSelectIncident(incident)}
              className={`flex items-start p-3 text-left border transition-colors group
                ${isSelected 
                  ? 'border-terminal-cyan/50 bg-terminal-cyan/5' 
                  : 'border-transparent hover:border-terminal-border hover:bg-terminal-panel'}`}
            >
              <div className={isSelected ? 'animate-pulse' : ''}>
                {getIcon(incident.severity, incident.affected_service)}
              </div>
              <div>
                <div className={`text-xs font-bold mb-1 uppercase ${getSeverityColor(incident.severity)}`}>
                  [{incident.severity}]
                </div>
                <div className={`text-sm font-medium transition-colors ${isSelected ? 'text-white' : 'text-terminal-dim group-hover:text-white'}`}>
                  {incident.title}
                </div>
                <div className="text-xs text-terminal-dim mt-1 flex items-center opacity-50">
                  <Activity className="w-3 h-3 mr-1" /> {incident.affected_service}
                </div>
              </div>
            </button>
          )
        })}
      </div>

      {/* Footer System Status */}
      <div className="mt-auto pt-4 border-t border-terminal-border">
        <div className="flex items-center text-xs text-terminal-green">
          <div className="w-2 h-2 rounded-full bg-terminal-green animate-pulse mr-2 shadow-glow-cyan"></div>
          SYSTEM ONLINE
        </div>
      </div>
    </div>
  )
}