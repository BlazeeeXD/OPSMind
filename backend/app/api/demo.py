from fastapi import APIRouter, Depends
from sqlmodel import Session
from datetime import datetime, timezone, timedelta
from app.database.db import get_session
from app.models.incident import Incident
from app.models.telemetry import LogEntry, MetricSnapshot, DeploymentEvent
from app.builders.evidence_builder import EvidenceBuilder

router = APIRouter(prefix="/demo", tags=["Demo Prep"])

@router.post("/seed/database-overload")
def seed_database_overload(session: Session = Depends(get_session)):
    now = datetime.now(timezone.utc)
    
    # 1. Create the Incident
    incident = Incident(
        title="Checkout DB CPU Saturation & Outage",
        severity="Critical",
        affected_service="checkout-db",
        status="investigating",
        created_at=now
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)
    
    inc_id = incident.id

    # 2. Create a Deployment Event (10 minutes before the incident)
    deployment = DeploymentEvent(
        incident_id=inc_id,
        service="checkout-db",
        commit_hash="a1b2c3d4",
        author="sre-eng@company.com",
        deployment_time=now - timedelta(minutes=10)
    )
    session.add(deployment)

    # 3. Create Metrics (Simulating Normal -> Spike)
    for i in range(10):
        t = now - timedelta(minutes=10 - i)
        
        # CPU spikes at minute 5, Latency shoots up
        cpu_val = 45.0 if i < 5 else 98.5
        latency_val = 120.0 if i < 5 else 4500.0
        error_rate_val = 0.01 if i < 5 else 0.45
        
        metric = MetricSnapshot(
            incident_id=inc_id,
            timestamp=t,
            cpu=cpu_val,
            memory=60.0,
            latency=latency_val,
            error_rate=error_rate_val,
            request_count=1000 + (i * 100)
        )
        session.add(metric)

    # 4. Create Logs (The breadcrumb trail)
    logs_data = [
        ("INFO", "Starting database migration script: add_indexes_to_orders", 10),
        ("INFO", "Migration completed successfully", 9),
        ("WARNING", "Connection pool reaching 80% capacity", 5),
        ("ERROR", "Connection timeout acquiring database lock", 4),
        ("ERROR", "Query timeout for SELECT * FROM checkout_sessions", 3),
        ("ERROR", "Database CPU utilization critical: 98%", 2),
        ("CRITICAL", "Checkout service database completely unresponsive", 1)
    ]
    
    for level, msg, mins_ago in logs_data:
        log = LogEntry(
            incident_id=inc_id,
            timestamp=now - timedelta(minutes=mins_ago),
            service="checkout-db",
            level=level,
            message=msg
        )
        session.add(log)

    session.commit()
    
    return {
        "status": "success", 
        "message": "Demo data seeded perfectly. Ready for AI investigation.",
        "incident_id": inc_id
    }
    


@router.get("/verify-evidence/{incident_id}")
def verify_evidence(incident_id: int, session: Session = Depends(get_session)):
    """Temporary route to check what the LLM will see."""
    builder = EvidenceBuilder(session)
    evidence_package = builder.build(incident_id)
    return evidence_package

@router.post("/seed/memory-leak")
def seed_memory_leak(session: Session = Depends(get_session)):
    now = datetime.now(timezone.utc)
    
    incident = Incident(
        title="Image Processor OOM Crash Loop",
        severity="High",
        affected_service="image-processor",
        status="investigating",
        created_at=now
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)
    
    inc_id = incident.id

    # Metrics: Memory climbs steadily over 30 minutes, then crashes
    for i in range(15):
        t = now - timedelta(minutes=15 - i)
        
        # Memory goes from 40% up to 99%, then drops to 10% after pod restart
        memory_val = 40.0 + (i * 4.0) if i < 14 else 10.0
        error_rate_val = 0.01 if i < 13 else 0.80
        
        metric = MetricSnapshot(
            incident_id=inc_id, timestamp=t,
            cpu=30.0, memory=memory_val, latency=200.0,
            error_rate=error_rate_val, request_count=500
        )
        session.add(metric)

    # Logs: The classic OOM sequence
    logs_data = [
        ("WARNING", "Garbage collection taking longer than expected (>500ms)", 10),
        ("WARNING", "Heap memory utilization at 85%", 5),
        ("ERROR", "Failed to allocate memory for image buffer", 2),
        ("CRITICAL", "Fatal error: java.lang.OutOfMemoryError: Java heap space", 1),
        ("CRITICAL", "Pod evicted: OOMKilled", 0)
    ]
    
    for level, msg, mins_ago in logs_data:
        session.add(LogEntry(
            incident_id=inc_id, timestamp=now - timedelta(minutes=mins_ago),
            service="image-processor", level=level, message=msg
        ))

    session.commit()
    return {"status": "success", "scenario": "Memory Leak", "incident_id": inc_id}

@router.post("/seed/payment-outage")
def seed_payment_outage(session: Session = Depends(get_session)):
    now = datetime.now(timezone.utc)
    
    incident = Incident(
        title="Checkout Failures - Upstream API Timeout",
        severity="Critical",
        affected_service="payment-gateway",
        status="investigating",
        created_at=now
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)
    
    inc_id = incident.id

    # Metrics: Internal systems are healthy, but latency/errors are massive
    for i in range(10):
        t = now - timedelta(minutes=10 - i)
        
        latency_val = 150.0 if i < 4 else 8500.0 # Stripe API hanging
        error_rate_val = 0.0 if i < 4 else 0.65
        
        metric = MetricSnapshot(
            incident_id=inc_id, timestamp=t,
            cpu=25.0, memory=40.0, latency=latency_val, # DB and CPU are fine!
            error_rate=error_rate_val, request_count=800
        )
        session.add(metric)

    # Logs: Pinpointing the third party
    logs_data = [
        ("INFO", "Processing batch payments", 6),
        ("WARNING", "Stripe API response time degraded (>3000ms)", 5),
        ("ERROR", "Stripe API timeout: connection reset by peer", 4),
        ("ERROR", "Circuit breaker opened for downstream service: stripe-api", 3),
        ("CRITICAL", "Payment processing halted. 65% of checkouts failing.", 1)
    ]
    
    for level, msg, mins_ago in logs_data:
        session.add(LogEntry(
            incident_id=inc_id, timestamp=now - timedelta(minutes=mins_ago),
            service="payment-gateway", level=level, message=msg
        ))

    session.commit()
    return {"status": "success", "scenario": "Third Party Outage", "incident_id": inc_id}

@router.post("/seed/bad-deployment")
def seed_bad_deployment(session: Session = Depends(get_session)):
    now = datetime.now(timezone.utc)
    
    incident = Incident(
        title="Auth Service Immediate Crash Loop",
        severity="High",
        affected_service="auth-service",
        status="investigating",
        created_at=now
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)
    
    inc_id = incident.id

    # Deployments: The Bad Push
    session.add(DeploymentEvent(
        incident_id=inc_id, service="auth-service",
        commit_hash="f9e8d7c6", author="junior-dev@company.com",
        deployment_time=now - timedelta(minutes=6)
    ))

    # Metrics: Fast failure
    for i in range(8):
        t = now - timedelta(minutes=8 - i)
        
        error_rate_val = 0.01 if i < 2 else 1.0 # Goes to 100% failure instantly
        
        metric = MetricSnapshot(
            incident_id=inc_id, timestamp=t,
            cpu=10.0, memory=20.0, latency=50.0,
            error_rate=error_rate_val, request_count=300
        )
        session.add(metric)

    # Logs: Missing env var causes instant crash
    logs_data = [
        ("INFO", "Shutting down old pods", 6),
        ("INFO", "Starting auth-service v2.1.4", 5),
        ("CRITICAL", "Environment variable JWT_SECRET is undefined. Halting startup.", 5),
        ("ERROR", "Readiness probe failed: connection refused", 4),
        ("CRITICAL", "Pod auth-service-xxx entered CrashLoopBackOff", 2)
    ]
    
    for level, msg, mins_ago in logs_data:
        session.add(LogEntry(
            incident_id=inc_id, timestamp=now - timedelta(minutes=mins_ago),
            service="auth-service", level=level, message=msg
        ))

    session.commit()
    return {"status": "success", "scenario": "Bad Deployment", "incident_id": inc_id}