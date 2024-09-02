from env.envConfig import env
from fastapi import FastAPI, Depends, Request
import os
from fastapi.middleware.cors import CORSMiddleware
# from src.app.validator import users as users_validator
# from fastapi.security import OAuth2PasswordRequestForm
# from src.app.auth.permissions import sign_up, login_user, secure_endpoint
from src.utils.logging import logger
svc_name = env.get("APP_NAME", "de")
logger.info(f"svc_name: {svc_name}")

app_params = {
    "title": f"{svc_name} public API",
    "description": f"{svc_name} public api",
    "version": "0.1.0",
    "docs_url": '/swagger',
    "redoc_url": '/docs',
}

app = FastAPI(**app_params)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(request: Request):
    return {f"{svc_name}": "Running public API"}

# @app.post("/signup", tags=["Sign Up / Login"])
# def sign_up_user(user: users_validator.CreateUser):
#     return sign_up(user.__dict__)
    

# @app.post("/token", tags=["Sign Up / Login"])
# def login(form: OAuth2PasswordRequestForm = Depends()):
#     return login_user(form.username, form.password)



# Add the routes from the routers
from src.app.views import users
from src.app.views import employee
# app.include_router(users.router, dependencies=[Depends(secure_endpoint)])
app.include_router(users.router)
app.include_router(employee.router)
