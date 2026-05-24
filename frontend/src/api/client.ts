const BASE_URL = 'https://opsmind-api-jx8z.onrender.com';

export const api = {
  // Get all active incidents
  getIncidents: async () => {
    const res = await fetch(`${BASE_URL}/incidents/`);
    if (!res.ok) throw new Error('Failed to fetch incidents');
    return res.json();
  },

  // Trigger an investigation and get a Job ID
  triggerInvestigation: async (incidentId: number) => {
    const res = await fetch(`${BASE_URL}/investigations/trigger/${incidentId}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to start investigation');
    return res.json(); // { job_id, message }
  },

  // Poll the job status
  getJobStatus: async (jobId: string) => {
    const res = await fetch(`${BASE_URL}/investigations/jobs/${jobId}`);
    if (!res.ok) throw new Error('Failed to fetch job status');
    return res.json(); // { status, stage }
  },

  // Get the final formatted report
  getReport: async (incidentId: number) => {
    const res = await fetch(`${BASE_URL}/investigations/report/${incidentId}`);
    if (!res.ok) throw new Error('Failed to fetch report');
    return res.json();
  }
};