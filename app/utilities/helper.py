import secrets
from datetime import timezone, datetime


def get_utc_now():
    return datetime.now(timezone.utc)


def generate_token():
    app_secret_key = secrets.token_urlsafe(32)
    print(app_secret_key)
    jwt_secret_key = secrets.token_hex(32)
    print(jwt_secret_key)


if __name__ == "__main__":
    generate_token()
