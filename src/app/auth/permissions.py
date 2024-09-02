# from fastapi import Depends, HTTPException, status, Request
# from fastapi.security import OAuth2PasswordBearer
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from src.service.domain import users
# from src.utils.constants import USER_DB
# from src.utils.mongodb.mongodb import MongoService

# from env.envConfig import env
# import os
# from functools import wraps

# SECRET_KEY = env.get("SECRET_KEY")
# ALGORITHM = env.get("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = env.get("ACCESS_TOKEN_EXPIRE_MINUTES")

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_password(plain_password, hashed_password):
#     """
#     Verify the password against the hashed password.
#     """
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     """
#         Hash the password.
#     """
#     return pwd_context.hash(password)

# def get_user(email: str):
#     """
#     Retrieve user information from the database.
#     """
#     return MongoService.fetch(USER_DB, {"email": email})

# def authenticate_user(email: str, password: str):
#     """
#     Authenticate the user.
#     """
#     user = get_user(email)
#     if not user or not verify_password(password, user["hashed_password"]):
#         return False
#     return user

# def create_access_token(username: str):
#     """
#     Create the access token for the user authentication.
#     """
#     token_expire_duration = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode = {
#         "sub": username, 
#         "exp": token_expire_duration
#     }
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     """
#     Get the current user from the token.
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
    
#     user = get_user(username)
#     if user is None:
#         raise credentials_exception
#     return user

# def get_current_active_user(current_user: dict = Depends(get_current_user)):
#     """
#     Get the current active user.
#     """
#     if current_user["is_active"]:
#         return current_user
#     raise HTTPException(status_code=400, detail="Inactive user")

# def sign_up(user: dict):
#     """
#     Sign up the user.
#     """
#     if get_user(user["email"]):
#         raise HTTPException(status_code=400, detail="User already registered")
#     user["hashed_password"] = get_password_hash(user.pop("password"))

#     response = users.create_user(**user)
#     return response

# def login_user(username: str, password: str):
#     """
#     Login the user.
#     """
#     user = authenticate_user(username, password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     access_token = create_access_token(username)
#     return {"access_token": access_token, "token_type": "bearer"}

# # Decorator to authenticate endpoints
# # def authenticate():
# #     def decorator(func):
# #         @wraps(func)
# #         async def wrapper(request: Request, *args, **kwargs):
# #             if request.url.path in ["/signup", "/login", "/docs", "/swagger", "/openapi.json", "/"]:
# #                 return func(request, *args, **kwargs)

# #             token = request.headers.get("Authorization")
# #             if not token:
# #                 raise HTTPException(status_code=401, detail="Token is missing")

# #             try:
# #                 payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #                 username: str = payload.get("sub")
# #                 if username is None:
# #                     raise HTTPException(status_code=401, detail="Invalid token")
# #                 user = get_user(username)
# #                 get_current_active_user(user)
# #             except jwt.JWTError:
# #                 raise HTTPException(status_code=401, detail="Invalid token")
# #             return func(**kwargs, request=request)
# #         return wrapper
# #     return decorator

# def secure_endpoint(request: Request, token: str = Depends(oauth2_scheme)):
#     """
#     Dependency function to secure endpoints with JWT token authentication.
#     """
#     if request.url.path in ["/signup", "/login", "/docs", "/swagger", "/openapi.json", "/"]:
#         return
#     else:
#         if not token:
#             raise HTTPException(status_code=401, detail="Token is missing")
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username: str = payload.get("sub")
#             if username is None:
#                 raise HTTPException(status_code=401, detail="Invalid token")
#             user = get_user(username)
#             # Check depending on the user of get_current_active_user
#             get_current_active_user(user)
#         except jwt.JWTError:
#             raise HTTPException(status_code=401, detail="Invalid token")

# # def authenticate_user(request: Request, call_next):
# #     """
# #     Middleware function to authenticate the user if it is not signup or login.
# #     """
# #     print(f"\n\n\n Request: {request.url.path}")
# #     if request.url.path in ["/signup", "/login", "/docs", "/swagger", "/openapi.json", "/"]:
# #         return call_next(request)
# #     else:
# #         token = request.headers.get("Authorization")
# #         print(f"\n\n\n Token: {token}")
# #         if not token:
# #             raise HTTPException(status_code=401, detail="Token is missing")
# #         try:
# #             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #             username: str = payload.get("sub")
# #             if username is None:
# #                 raise HTTPException(status_code=401, detail="Invalid token")
# #             user = get_user(username)
# #             # Check depending on the user of get_current_active_user
# #             get_current_active_user(user)
# #         except JWTError:
# #             raise HTTPException(status_code=401, detail="Invalid token")
        
# #         return call_next(request)