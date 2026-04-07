def grade_easy(actions):
    return 1.0 if "restart_service" in actions else 0.0

def grade_medium(actions):
    if "scale_up" in actions and "restart_service" in actions:
        return 1.0
    return 0.5 if "scale_up" in actions else 0.0

def grade_hard(actions):
    if actions and actions[-1] == "patch_config":
        return 1.0
    return 0.2