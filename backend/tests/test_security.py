from app.core.security import hash_password, verify_password, create_access_token, decode_token


def test_password_hash_and_verify():
    hashed = hash_password("Passw0rd!123")
    assert hashed != "Passw0rd!123"
    assert verify_password("Passw0rd!123", hashed)
    assert not verify_password("WrongPassword", hashed)


def test_jwt_roundtrip():
    token = create_access_token(subject="user-123", role="CRIME_ANALYST")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user-123"
    assert payload["role"] == "CRIME_ANALYST"
    assert payload["type"] == "access"


def test_invalid_token_returns_none():
    assert decode_token("not-a-real-token") is None
