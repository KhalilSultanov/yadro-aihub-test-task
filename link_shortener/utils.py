import secrets


def generate_short_code():
    return secrets.token_urlsafe(5)
