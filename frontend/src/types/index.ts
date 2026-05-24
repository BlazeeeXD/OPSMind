export interface Incident {
  id: number;
  title: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  status: string;
  affected_service: string;
  created_at: string;
}

export interface RootCause {
  cause: string;
  confidence: number;
  reasoning: string;
}

export interface InvestigationReport {
  incident_id: number;
  created_at: string;
  summary: {
    title: string;
    severity: string;
    affected_service: string;
  };
  root_causes: {
    causes: RootCause[];
  };
  recommendations: {
    actions: string[];
    recovery_time: string;
    impact: string;
    risk: string;
  };
  timeline: {
    time: string;
    event: string;
  }[];
}