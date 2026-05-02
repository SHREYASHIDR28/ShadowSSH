# ShadowSSH
# Author: Shreyashi Deb Roy
# NOTE: Core logic partially withheld to protect intellectual property



def generate_fake_response(command, deception_strategy):
    """
    GenAI Execution Layer (Public Version)

    NOTE:
    Real LLM integration and advanced prompt engineering 
    have been intentionally removed for security and originality.
    """

    realism = deception_strategy["realism_level"]
    response_style = deception_strategy["response_style"]
    deception_depth = deception_strategy["deception_depth"]

    # Simplified prompt (no sensitive logic)
    prompt = f"""
Simulated Linux system.

Command: {command}
Mode: {realism}
"""

    # Using mock instead of real GenAI
    return mock_llm_response(command, realism)


def mock_llm_response(command, realism):
    """
    Mock response generator for demonstration purposes.
    """

    if command.startswith("ls"):
        return "bin  boot  dev  etc  home  lib  tmp  usr  var\n"

    if command.startswith("pwd"):
        return "/home/test\n"

    if command.startswith("whoami"):
        return "test\n"

    if "sudo" in command or "su" in command:
        return "Permission denied\n"

    if realism == "highly_realistic":
        return f"{command}: command executed successfully\n"

    return f"{command}: command not found\n"
