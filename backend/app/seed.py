from .database import SessionLocal, engine, Base
from .models import Control, ControlStatus, TrustCategory

SEED_CONTROLS = [
    dict(
        name="Single sign-on (SSO)",
        description="All production systems require SSO via the corporate identity provider; no standalone credentials.",
        category=TrustCategory.security,
        status=ControlStatus.verified,
        owner="Jaskaran Singh",
        evidence_url="https://example.com/evidence/sso",
    ),
    dict(
        name="Static application security testing (SAST)",
        description="Every pull request is scanned for known vulnerability patterns before merge.",
        category=TrustCategory.security,
        status=ControlStatus.verified,
        owner="Jaskaran Singh",
        evidence_url="https://example.com/evidence/sast",
    ),
    dict(
        name="Dependency scanning",
        description="Automated scanning of third-party dependencies for known CVEs on every build.",
        category=TrustCategory.security,
        status=ControlStatus.implemented,
        owner="Jaskaran Singh",
        evidence_url="https://example.com/evidence/dependency-scan",
    ),
    dict(
        name="Vulnerability remediation SLA",
        description="Critical vulnerabilities are remediated within 7 days, high within 30 days.",
        category=TrustCategory.security,
        status=ControlStatus.implemented,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Access review (quarterly)",
        description="Quarterly review of who has access to production systems and data stores.",
        category=TrustCategory.security,
        status=ControlStatus.in_progress,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Encryption at rest",
        description="All production databases and object storage are encrypted at rest.",
        category=TrustCategory.confidentiality,
        status=ControlStatus.verified,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Encryption in transit",
        description="TLS 1.2+ enforced for all external and internal service-to-service traffic.",
        category=TrustCategory.confidentiality,
        status=ControlStatus.verified,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Backup restoration testing",
        description="Quarterly test restore of production backups to verify recoverability.",
        category=TrustCategory.availability,
        status=ControlStatus.in_progress,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Incident response plan",
        description="Documented incident response runbook with defined escalation paths.",
        category=TrustCategory.availability,
        status=ControlStatus.implemented,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Change management",
        description="All production changes go through code review and a documented deploy process.",
        category=TrustCategory.processing_integrity,
        status=ControlStatus.verified,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Centralized logging & monitoring",
        description="Application and infrastructure logs are centralized with alerting on anomalies.",
        category=TrustCategory.availability,
        status=ControlStatus.implemented,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Vendor risk management",
        description="Third-party vendors handling customer data are reviewed before onboarding.",
        category=TrustCategory.security,
        status=ControlStatus.not_started,
        owner="Jaskaran Singh",
    ),
    dict(
        name="Security awareness training",
        description="Annual security awareness training completed by all engineering staff.",
        category=TrustCategory.security,
        status=ControlStatus.not_started,
        owner="Jaskaran Singh",
    ),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Control).count() == 0:
            for row in SEED_CONTROLS:
                db.add(Control(**row))
            db.commit()
            print(f"Seeded {len(SEED_CONTROLS)} controls.")
        else:
            print("Controls already present, skipping seed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
