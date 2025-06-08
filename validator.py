def coerce(value, expected_type):
    if expected_type == "string":
        return str(value)
    if expected_type == "int":
        return int(value)
    if expected_type == "float":
        return float(value)
    raise ValueError(f"Unsupported type: {expected_type}")

def validate_row(row: dict, schema: dict) -> tuple:
    errors = []

    for key, rule in schema.items():
        if isinstance(rule, dict):
            expected_type = rule.get("type")
            required = rule.get("required", True)
        else:
            expected_type = rule
            required = True

        value = row.get(key)

        if value is None or value == "":
            if required:
                errors.append(f"{key} is required")
            continue

        try:
            coerce(value, expected_type)
        except Exception as e:
            errors.append(f"{key}: {e}")

    return len(errors) == 0, errors
