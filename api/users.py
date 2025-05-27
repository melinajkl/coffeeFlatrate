from fastapi import APIRouter
from utils.csv_storage import read_csv, append_csv

router = APIRouter()

@router.get("/")
def get_users():
    return read_csv("users.csv")

@router.post("/")
def create_user(user: dict):
    append_csv("users.csv", user)
    return {"msg": "User created successfully"}