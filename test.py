import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from models import model
from database import get_db
from uuid import uuid4

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_db] = override_get_db

# Create tables before tests run
model.Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_employee_with_cafe():
    # Step 1: Create a café
    cafe_id = str(uuid4())
    cafe_payload = {
        "id": cafe_id,
        "iban": "DE89370400440532013000",
        "bic": "COBADEFFXXX",
        "account_holder": "Cafe Latte",
        "abolist": []
    }
    cafe_response = client.post("/cafes/", json=cafe_payload)
    assert cafe_response.status_code == 200

    # Step 2: Create an employee assigned to that café
    employee_payload = {
        "name": "Alice",
        "password": "strongpassword123",
        "sudo": True,
        "cafe_id": cafe_id
    }
    emp_response = client.post("/employees/", json=employee_payload)
    assert emp_response.status_code == 200
    data = emp_response.json()
    assert data["name"] == "Alice"
    assert data["sudo"] is True
    assert data["cafe_id"] == cafe_id
