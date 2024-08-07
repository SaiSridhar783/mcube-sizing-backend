from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import users_controller, mcube_estimation_controller, sizing_req_controller, role_controller, deployment_option_controller, selected_component_controller, component_size_slab_controller, deployment_region_controller, mcube_component_controller, suggest_controller, deployment_spec_controller


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(role_controller.router, prefix="/role", tags=["Roles"])
app.include_router(users_controller.router, prefix="/users", tags=["Users"])
app.include_router(deployment_option_controller.router,
                   prefix="/deployment-option", tags=["Deployment Options"])
app.include_router(deployment_region_controller.router,
                   prefix="/deployment-region", tags=["Deployment Regions"])
app.include_router(mcube_component_controller.router,
                   prefix="/mcube-component", tags=["Mcube Components"])
app.include_router(component_size_slab_controller.router,
                   prefix="/mcube-component-size-slab", tags=["Mcube Component Size Slabs"])
app.include_router(mcube_estimation_controller.router,
                   prefix="/estimations", tags=["Estimations"])
app.include_router(sizing_req_controller.router,
                   prefix="/sizing", tags=["Sizing Requirements"])
app.include_router(selected_component_controller.router,
                   prefix="/selected-components", tags=["Selected Components"])
app.include_router(deployment_spec_controller.router,
                   prefix="/deployment-specs", tags=["Specifications for Deployment"])
app.include_router(suggest_controller.router,
                   prefix = "/suggestions", tags = ["Suggestions based on sizing"])
