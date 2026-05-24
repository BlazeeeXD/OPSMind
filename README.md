# OPSMIND
### AI-Powered Incident Investigation Platform

OpsMind is an AI-powered incident investigation platform that helps engineers identify the root cause of production outages in seconds.

Instead of manually searching through logs, metrics, deployment histories, and monitoring dashboards, OpsMind automatically analyzes operational telemetry, reconstructs the sequence of events, identifies probable root causes, and generates actionable remediation plans.

Built for modern SRE, DevOps, and Platform Engineering teams.

---

## The Problem

When a production outage occurs, engineers are often forced to jump between:

- Logs
- Metrics
- Deployment histories
- Monitoring dashboards
- Alerting systems

Finding the answer to a simple question:

> **What actually happened?**

This process can take hours.

OpsMind reduces that investigation time to seconds by transforming operational chaos into structured incident reports.

---

## Demo

### Incident Investigation Workflow

```text
Production Incident
        │
        ▼
Telemetry Collection
(Log Events, Metrics, Deployments)
        │
        ▼
Evidence Extraction Engine
(Deterministic Analytics)
        │
        ▼
AI Root Cause Investigation
        │
        ▼
Remediation Planning
        │
        ▼
Timeline Reconstruction
        │
        ▼
Final Incident Report
```

---

## Features

### AI Root Cause Analysis

Automatically identifies likely causes of outages using telemetry evidence and contextual reasoning.

### Deterministic Evidence Extraction

Rather than sending thousands of raw logs to an LLM, OpsMind extracts high-signal evidence first:

- Error frequency analysis
- Exception grouping
- Metric anomaly detection
- Deployment correlation

This reduces hallucinations and improves reliability.

### Timeline Reconstruction

Automatically rebuilds the incident timeline:

```text
17:00 Deployment

17:01 Configuration Failure

17:02 Readiness Probe Failed

17:04 CrashLoopBackOff

17:05 Service Outage
```

### Confidence Scoring

Every root cause includes confidence estimates and supporting evidence.

### Remediation Planning

Generates:

- Recommended actions
- Recovery estimates
- Operational risks
- Expected impact

### Terminal-Inspired Command Center

A purpose-built engineering dashboard designed around information density and rapid incident comprehension.

---

# Architecture

OpsMind uses a hybrid Deterministic + AI architecture.

```text
RAW TELEMETRY
(Logs, Metrics, Deployments)
          │
          ▼
DETERMINISTIC ANALYTICS
(Log Analyzer)
(Metric Analyzer)
(Deployment Correlator)
          │
          ▼
EVIDENCE PACKAGE
(JSON Facts)
          │
          ▼
AI INVESTIGATION LAYER
(Investigator Agent)
(Remediation Agent)
          │
          ▼
VALIDATION LAYER
(Pydantic Models)
          │
          ▼
FINAL INCIDENT REPORT
```

The deterministic layer extracts objective facts.

The AI layer focuses exclusively on reasoning over evidence rather than raw telemetry.

---

# Technology Stack

## Backend

- FastAPI
- SQLModel
- SQLite
- Pydantic
- Google Gemini
- Async Background Tasks

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS
- Lucide Icons
- JetBrains Mono

---

# Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── agents/
│   ├── analyzers/
│   ├── builders/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
└── .env

frontend/
│
├── src/
│   ├── api/
│   ├── components/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
│
├── package.json
└── vite.config.ts
```

---

# Demo Scenarios

OpsMind ships with four built-in incident simulations.

### Database Overload

Simulates:

- CPU saturation
- Connection pool exhaustion
- Query lock contention
- Service degradation

### Memory Leak

Simulates:

- Progressive memory growth
- OOMKilled containers
- Pod restart loops

### Payment API Outage

Simulates:

- Third-party dependency failure
- Latency spikes
- Checkout disruption

### Bad Deployment

Simulates:

- Missing configuration values
- Startup failures
- CrashLoopBackOff states

These scenarios enable reliable demonstrations without requiring external infrastructure.

---

# Running Locally

## Prerequisites

- Python 3.12+
- Node.js 18+
- Gemini API Key

---

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Create `.env`

```env
GEMINI_API_KEY=your_api_key_here
```

Run server:

```bash
uvicorn app.main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Application:

```text
http://localhost:5173
```

---

# Demo Flow

1. Open Swagger UI
2. Seed a scenario

```text
POST /demo/seed/database-overload
POST /demo/seed/memory-leak
POST /demo/seed/payment-outage
POST /demo/seed/bad-deployment
```

3. Open OpsMind
4. Select incident
5. Start Investigation
6. Review:
   - Timeline
   - Root Cause Analysis
   - Confidence Scores
   - Remediation Plan

---

# Reliability Features

### JSON Validation

All AI responses are validated using Pydantic before reaching the frontend.

### Fallback Responses

If AI provider limits are reached, deterministic fallback responses are generated to ensure demo stability.

### Safe Re-Investigation

Existing reports are safely replaced when incidents are re-analyzed.

---

# Future Improvements

- Real-time telemetry ingestion
- Datadog integration
- Grafana integration
- Kubernetes event streams
- Historical incident memory
- Automated remediation workflows
- Vector-search powered incident retrieval

---

# Built For

HackHazards 2026

### Problem Statement #3
**AI Incident Root Cause Analyzer for SRE Teams**
