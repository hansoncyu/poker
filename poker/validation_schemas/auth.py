REGISTER_USER = {
    "username": {"type": "string", "required": True, "empty": False},
    "password": {"type": "string", "required": True, "empty": False},
    "display_name": {"type": "string", "required": True},
}

ANONYMOUS_LOGIN = {
    "display_name": {"type": "string", "required": True},
}
