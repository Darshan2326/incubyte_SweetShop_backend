import pytest
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from app.user.utils import JWT_SECRET
from app.auth.dependencies import fetch_current_user

# Test for the actual dependency function


def test_fetch_current_user_valid_token(mocker):
    """Test fetch_current_user with a valid token"""
    # Mock the token and jwt decode
    mock_token = mocker.MagicMock()
    mock_token.credentials = "valid_token"

    # Mock jwt.decode to return a valid payload
    mocker.patch('jwt.decode', return_value={
                 "user_id": "123", "email": "test@example.com"})

    # Call the actual dependency function
    result = fetch_current_user(mock_token)

    # Assertions
    assert result == {"user_id": "123", "email": "test@example.com"}


def test_fetch_current_user_invalid_token(mocker):
    """Test fetch_current_user with an invalid token"""
    # Mock the token
    mock_token = mocker.MagicMock()
    mock_token.credentials = "invalid_token"

    # Mock jwt.decode to raise an exception
    mocker.patch('jwt.decode', side_effect=Exception("Invalid token"))

    # Expect HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        fetch_current_user(mock_token)

    assert exc_info.value.status_code == 401
