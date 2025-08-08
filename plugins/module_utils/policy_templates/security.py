policy_security_definition = {
    "security": {
        "default": None,
        "required": False,
        "type": "dict",
        "options": {
            "type": {
                "type": "str",
                "choices": ["feature", "cli"],
                "default": "feature",
            },
            "definition": {"type": "dict"},
        },
    }
}
