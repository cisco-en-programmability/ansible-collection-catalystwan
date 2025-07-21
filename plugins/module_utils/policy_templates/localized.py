policy_localized_definition = {
    "localized": {
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
