from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import AuthHandler
from crud.user import create_user, get_user_by_username, reset_password
from models.user import User as ModelUser
from schemas.user import ChangePassword, Staff, User, UserCreate
from schemas.token import Token

import database

router = APIRouter(prefix="/user", tags=["User"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# An instance of AuthHandler class
# from auth.py which contains authentication functions.
auth_handler = (AuthHandler())

"""
 API Endpoints for "user" submodule.

"""


@router.post("/register", status_code=201, response_model=User)
async def register(
    user: UserCreate,
    current_user: ModelUser = Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)
):
    if current_user.staff != Staff.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to perform this action"
        )

    # Use "validate_password" function from "Auth_Handler" class
    # to check password combinations, throw exception if
    # the combinations are bad.
    if not auth_handler.validate_password(user.password):
        raise HTTPException(
            status_code=401,
            detail=(
                "Password not accepted. It must contain one uppercase "
                "letter, one lowercase letter, one numeral, "
                "one special character and should be longer "
                "than 6 characters and shorter than 20 characters"
            )
        )

    user_dict = user.dict()
    user_dict["password"] = auth_handler.get_password_hash(user.password)
    db_user = create_user(db, user_dict)
    return db_user


@router.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Use "get_user_by_username" function to get user from the database.
    user_db = get_user_by_username(db, form_data.username)

    # If user doesn't exist in database, raise an exception.
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f" User '{form_data.username}' doesn't exist, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password = user_db.password
    verify_password = auth_handler.verify_password(
        form_data.password, password
    )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = user_db.username
    token = auth_handler.encode_token(username)
    return {"token": token, "token_type": "Bearer"}


@router.get("/profile", response_model=User)
def profile(
    current_user: ModelUser = Depends(auth_handler.auth_wrapper)
):
    return current_user


@router.patch("/change-password")
async def change_password(
    passwords: ChangePassword,
    current_user: ModelUser = Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db),
):
    if not auth_handler.validate_password(passwords.new_password):
        raise HTTPException(
            status_code=401,
            detail=(
                "Password not accepted. It must contain one uppercase "
                "letter, one lowercase letter, one numeral, "
                "one special character and should be longer "
                "than 6 characters and shorter than 20 characters"
            )
        )

    password = current_user.password

    verify_password = auth_handler.check_password(
        passwords.old_password, password
    )

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify password, try again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if passwords.new_password != passwords.confirm_password:
        raise HTTPException(
            status_code=404,
            detail="New password and Confirm Password do not match"
        )
    new_password_hash = auth_handler.get_password_hash(
        passwords.new_password
    )
    user = User.from_orm(current_user)
    reset_password(db, user.id, new_password_hash)

    return {
        "message": f"Password updated for the user: {current_user.username}"
    }