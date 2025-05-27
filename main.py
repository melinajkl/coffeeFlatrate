from fastapi import FastAPI
from api import users, cafes, abos, report

app = FastAPI(
    title="Kaffee Abo System",
    description="Ein Backend-System zur Verwaltung von Kaffeeabos für Cafés",
    version="0.1.0"
)

# Include your routers
app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(cafes.router, prefix="/cafes", tags=["Cafés"])
# app.include_router(abos.router, prefix="/abos", tags=["Abos"])
# app.include_router(report.router, prefix="/reports", tags=["Reports"])

@app.get("/")
def read_root():
    return {"message": "Willkommen im Kaffee-Abo-System API!"}
