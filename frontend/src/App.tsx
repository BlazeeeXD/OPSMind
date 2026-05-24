import { useState } from 'react'
import Sidebar from './components/Sidebar'
import LoadingTerminal from './components/LoadingTerminal'
import { api } from './api/client'
import type { Incident } from './types'
import ReportDashboard from './components/ReportDashboard'
import AILog from './components/AILog'

function App() {
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);
  
  // Investigation State
  const [jobId, setJobId] = useState<string | null>(null);
  const [showReport, setShowReport] = useState(false);
  const [isTriggering, setIsTriggering] = useState(false);

  // Reset workspace when a new incident is clicked
  const handleSelectIncident = async (incident: Incident) => {
    setSelectedIncident(incident);
    setJobId(null);
    setShowReport(false);
    setIsTriggering(false);

    // Ping the backend to see if a report already exists for this incident
    try {
      await api.getReport(incident.id);
      // If the above line doesn't throw an error, the report exists!
      setShowReport(true); 
    } catch (error) {
      // 404 Error means no report exists yet. 
      // The UI stays on the "START INVESTIGATION" screen.
    }
  };

  const handleStartInvestigation = async () => {
    if (!selectedIncident) return;
    setIsTriggering(true);
    try {
      const response = await api.triggerInvestigation(selectedIncident.id);
      setJobId(response.job_id);
    } catch (error) {
      console.error("Failed to trigger API:", error);
      alert("Failed to start AI investigation. Check backend logs.");
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden">
      <div className="w-80 h-full border-r border-terminal-border bg-terminal-panel/50 flex flex-col shrink-0">
        <Sidebar 
          onSelectIncident={handleSelectIncident} 
          selectedIncidentId={selectedIncident?.id || null} 
        />
      </div>

      <div className="flex-1 h-full relative overflow-y-auto bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-terminal-panel/20 via-terminal-bg to-terminal-bg">
        <div className="p-8 h-full flex flex-col items-center justify-center">
          
          {!selectedIncident && (
             <p className="text-terminal-dim animate-pulse tracking-widest">
               WAITING FOR INCIDENT SELECTION...
             </p>
          )}

          {/* State 1: Ready to Investigate */}
          {selectedIncident && !jobId && !showReport && (
            <div className="text-center w-full max-w-xl">
              <div className="inline-block px-3 py-1 bg-terminal-cyan/10 border border-terminal-cyan/30 text-terminal-cyan text-xs tracking-widest mb-4">
                INCIDENT ID: {selectedIncident.id}
              </div>
              <h2 className="text-3xl font-bold text-white mb-2">{selectedIncident.title}</h2>
              <p className="text-terminal-dim mb-12 uppercase tracking-widest">Target System: {selectedIncident.affected_service}</p>
              
              <button 
                onClick={handleStartInvestigation}
                disabled={isTriggering}
                className="px-8 py-4 bg-transparent border-2 border-terminal-cyan text-terminal-cyan hover:bg-terminal-cyan hover:text-terminal-bg transition-all font-bold tracking-[0.2em] rounded-sm group relative overflow-hidden disabled:opacity-50"
              >
                <div className="absolute inset-0 w-full h-full bg-terminal-cyan/20 group-hover:bg-transparent transition-colors -z-10"></div>
                {isTriggering ? 'INITIALIZING...' : 'START INVESTIGATION'}
              </button>
            </div>
          )}

          {/* State 2: Investigating (Theater of Work) */}
          {jobId && !showReport && (
            <LoadingTerminal 
              jobId={jobId} 
              onComplete={() => setShowReport(true)} 
            />
          )}

          {/* State 3: Final Report */}
          {showReport && selectedIncident && (
            <>
              <ReportDashboard incidentId={selectedIncident.id} />
              <AILog />
            </>
          )}

        </div>
      </div>
    </div>
  )
}

export default App