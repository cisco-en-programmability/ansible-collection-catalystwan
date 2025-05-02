policy_centralized_definition = {
    "centralized": {
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
