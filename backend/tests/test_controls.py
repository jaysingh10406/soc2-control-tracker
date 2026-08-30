import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DB_URL = "sqlite:///./test_soc2_tracker.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_and_list_control():
    resp = client.post(
        "/controls",
        json={"name": "Test control", "status": "not_started", "category": "security"},
    )
    assert resp.status_code == 201
    control_id = resp.json()["id"]

    resp = client.get("/controls")
    assert resp.status_code == 200
    assert any(c["id"] == control_id for c in resp.json())


def test_update_control_status():
    resp = client.post("/controls", json={"name": "Encryption at rest"})
    control_id = resp.json()["id"]

    resp = client.patch(f"/controls/{control_id}", json={"status": "verified"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "verified"


def test_delete_control():
    resp = client.post("/controls", json={"name": "Temp control"})
    control_id = resp.json()["id"]

    resp = client.delete(f"/controls/{control_id}")
    assert resp.status_code == 204

    resp = client.get("/controls")
    assert all(c["id"] != control_id for c in resp.json())


def test_summary_counts():
    client.post("/controls", json={"name": "A", "status": "verified"})
    client.post("/controls", json={"name": "B", "status": "not_started"})

    resp = client.get("/controls/summary")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 2
    assert body["verified"] == 1
    assert body["not_started"] == 1


def test_update_missing_control_returns_404():
    resp = client.patch("/controls/9999", json={"status": "verified"})
    assert resp.status_code == 404
