PLAYER_ACTION = {
    "action": {
        "type": "string",
        "required": True,
        "oneof": [
            {"allowed": ["fold", "check", "call"]},
            {"allowed": ["bet", "raise"], "dependencies": "amount"},
        ],
    },
    "amount": {
        "type": "integer",
        "min": 0,
        "coerce": int,
    },
}
