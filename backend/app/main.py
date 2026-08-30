from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from . import models, schemas
from .database import engine, get_db, Base
from .seed import seed

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed()
    yield


app = FastAPI(
    title="SOC 2 Control Tracker",
    description="Tracks the status of SOC 2 trust-service controls: SSO, SAST, "
    "dependency scanning, vulnerability remediation, and more.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"service": "soc2-control-tracker", "status": "ok"}


@app.get("/controls", response_model=list[schemas.ControlOut])
def list_controls(db: Session = Depends(get_db)):
    return db.query(models.Control).order_by(models.Control.id).all()


@app.post("/controls", response_model=schemas.ControlOut, status_code=201)
def create_control(control: schemas.ControlCreate, db: Session = Depends(get_db)):
    db_control = models.Control(**control.model_dump())
    db.add(db_control)
    db.commit()
    db.refresh(db_control)
    return db_control


@app.patch("/controls/{control_id}", response_model=schemas.ControlOut)
def update_control(control_id: int, patch: schemas.ControlUpdate, db: Session = Depends(get_db)):
    db_control = db.query(models.Control).filter(models.Control.id == control_id).first()
    if not db_control:
        raise HTTPException(status_code=404, detail="Control not found")
    for field, value in patch.model_dump(exclude_unset=True).items():
        setattr(db_control, field, value)
    db_control.last_reviewed = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_control)
    return db_control


@app.delete("/controls/{control_id}", status_code=204)
def delete_control(control_id: int, db: Session = Depends(get_db)):
    db_control = db.query(models.Control).filter(models.Control.id == control_id).first()
    if not db_control:
        raise HTTPException(status_code=404, detail="Control not found")
    db.delete(db_control)
    db.commit()
    return None


@app.get("/controls/summary", response_model=schemas.SummaryOut)
def summary(db: Session = Depends(get_db)):
    controls = db.query(models.Control).all()
    total = len(controls)
    counts = {status.value: 0 for status in models.ControlStatus}
    for c in controls:
        counts[c.status.value] += 1
    percent = round((counts["verified"] + counts["implemented"]) / total * 100, 1) if total else 0.0
    return schemas.SummaryOut(
        total=total,
        not_started=counts["not_started"],
        in_progress=counts["in_progress"],
        implemented=counts["implemented"],
        verified=counts["verified"],
        percent_complete=percent,
    )
