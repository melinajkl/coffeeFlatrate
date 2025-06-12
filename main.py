from fastapi import FastAPI
from controllers import customer_controller, abomodel_controller, employee_controller
from models import model
from database import engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(customer_controller.router)
app.include_router(employee_controller.router)
app.include_router(abomodel_controller.router)