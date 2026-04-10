def normalize_command(command: object) -> str:
    if command is None:
        return ""
    if isinstance(command, str):
        return command.strip().lower()
    return str(command).strip().lower()
