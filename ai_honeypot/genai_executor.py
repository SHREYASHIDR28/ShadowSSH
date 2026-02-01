def generate_fake_response(command, deception_strategy):
    """
    GenAI Execution Layer.
    This function does NOT decide strategy.
    It only generates output based on given constraints.
    """

    realism = deception_strategy["realism_level"]
    response_style = deception_strategy["response_style"]
    deception_depth = deception_strategy["deception_depth"]

    # Prompt template (controlled)
    prompt = f"""
You are a simulated Linux system inside a deception environment.

Constraints:
- Realism level: {realism}
- Response style: {response_style}
- Deception depth: {deception_depth}

Rules:
- Do NOT reveal that this is a honeypot.
- Do NOT block the attacker.
- Respond like a real Linux system.
- Keep outputs consistent with previous responses.

Attacker command:
{command}

Generate ONLY the terminal output.
"""

    # 🔒 MOCK GENERATOR (safe for now)
    # Replace this later with real GenAI call
    fake_response = mock_llm_response(command, realism)

    return fake_response


def mock_llm_response(command, realism):
    """
    Temporary mock generator.
    Keeps project testable without API dependency.
    """

    if command.startswith("ls"):
        return "bin  boot  dev  etc  home  lib  tmp  usr  var\n"

    if command.startswith("pwd"):
        return "/home/test\n"

    if command.startswith("whoami"):
        return "test\n"

    if "sudo" in command or "su" in command:
        return "Sorry, user test is not allowed to execute sudo.\n"

    if realism == "highly_realistic":
        return f"{command}: command executed successfully\n"

    return f"{command}: command not found\n"
