import socket
import threading
import paramiko
import uuid
import time

from logger import log_event
from behavior_extractor import extract_behavior_features
from attacker_profile import classify_attacker
from decision_engine import decide_deception_strategy
from genai_executor import generate_fake_response


# ---------------- FAKE FILESYSTEM ----------------
FAKE_FS = {
    "pwd": "/home/test",
    "user": "test",
    "files": ["bin", "boot", "dev", "etc", "home", "lib", "tmp", "usr", "var"]
}

HOST_KEY = paramiko.RSAKey.generate(2048)


# ================= SSH SERVER =================
class HoneypotServer(paramiko.ServerInterface):
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        log_event(self.session_id, "auth", {
            "username": username,
            "password": password
        })
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, *args):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


# ================= CONNECTION HANDLER =================
def handle_connection(client):
    command_buffer = ""

    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)

    server = HoneypotServer()
    transport.start_server(server=server)

    channel = transport.accept(20)
    if channel is None:
        return

    server.event.wait(10)
    channel.send("Welcome to Ubuntu 20.04 LTS\n$ ")

    while True:
        try:
            data = channel.recv(1024)
            if not data:
                break

            for ch in data.decode():
                if ch in ("\r", "\n"):
                    command = command_buffer.strip()
                    command_buffer = ""

                    if not command:
                        channel.send("\n$ ")
                        continue

                    # -------- LOG COMMAND --------
                    log_event(server.session_id, "command", {
    "cmd": command
})


                    # -------- BEHAVIOR ANALYSIS --------
                    features = extract_behavior_features(server.session_id)
                    if not features:
                        channel.send("\n$ ")
                        continue

                    attacker_profile = classify_attacker(features)
                    deception_strategy = decide_deception_strategy(features, attacker_profile)


                    # -------- SERVER INTELLIGENCE OUTPUT --------
                    print("\n================ SESSION INTELLIGENCE ================")
                    print("Session ID:", server.session_id)

                    print("\nBehavior Features:")
                    for k, v in features.items():
                        print(f"  {k}: {v}")

                    print("\nAttacker Profile:")
                    for k, v in attacker_profile.items():
                        print(f"  {k}: {v}")

                    print("\nDeception Strategy:")
                    for k, v in deception_strategy.items():
                        print(f"  {k}: {v}")
                    print("======================================================\n")

                    # -------- RESPONSE GENERATION --------
                    if command == "ls":
                        response = "  ".join(FAKE_FS["files"])

                    elif command == "pwd":
                        response = FAKE_FS["pwd"]

                    elif command == "whoami":
                        response = FAKE_FS["user"]

                    elif command.startswith("cd"):
                        response = ""

                    else:
                        # Controlled GenAI execution
                        response = generate_fake_response(
                            command,
                            deception_strategy
                        )

                    channel.send("\n" + response + "\n$ ")

                else:
                    command_buffer += ch

        except Exception as e:
            print("Session error:", e)
            break

    channel.close()
    transport.close()


# ================= START SERVER =================
def start_honeypot(host="0.0.0.0", port=2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(100)

    print(f"[+] SSH Honeypot listening on port {port}")

    while True:
        client, _ = sock.accept()
        threading.Thread(
            target=handle_connection,
            args=(client,),
            daemon=True
        ).start()


if __name__ == "__main__":
    start_honeypot()
