from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import users_controller, mcube_estimation_controller, sizing_req_controller, role_controller, mcube_component_controller, deployment_target_controller

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(users_controller.router, prefix="/users", tags=["Users"])
app.include_router(mcube_estimation_controller.router,
                   prefix="/estimations", tags=["Estimations"])
app.include_router(sizing_req_controller.router,
                   prefix="/sizing", tags=["Sizing Requirements"])
app.include_router(mcube_component_controller.router,
                   prefix="/component", tags=["Mcube Components"])
app.include_router(role_controller.router, prefix="/role", tags=["Roles"])
app.include_router(deployment_target_controller.router,
                   prefix="/deployment_target", tags=["Deployment Targets"])
