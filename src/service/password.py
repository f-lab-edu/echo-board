import hashlib
import re

from fastapi import HTTPException, status


def hash_password(password: str) -> str:
    return hashlib.sha512(password.encode("utf-8")).hexdigest()


def check_password(input_password: str, stored_hashed_password: str) -> None:
    if hash_password(input_password) != stored_hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long.",
        )

    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter.",
        )
