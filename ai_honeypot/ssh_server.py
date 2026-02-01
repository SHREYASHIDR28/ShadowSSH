import socket
import threading
from click import command
import paramiko
import uuid
import time
from logger import log_event
from genai_executor import generate_fake_response
from behavior_extractor import extract_behavior_features
from attacker_profile import classify_attacker
from decision_engine import decide_deception_strategy


HOST_KEY = paramiko.RSAKey.generate(2048)

class HoneypotServer(paramiko.ServerInterface):
    def __init__(self):
        self.session_id = str(uuid.uuid4())

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
    
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED



    def check_channel_shell_request(self, channel):
        return True


def handle_connection(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = HoneypotServer()

    transport.start_server(server=server)
    channel = transport.accept(20)

    if channel is None:
        return

    channel.send("Welcome to Ubuntu 20.04 LTS\n$ ")

    # 🔹 Per-session state (VERY IMPORTANT)
    session_commands = []
    current_strategy = None

    while True:
        try:
            command = channel.recv(1024).decode("utf-8").strip()
            if not command:
                break

            # 1️⃣ Log raw command
            log_event(server.session_id, "command", {
                "cmd": command,
                "time": time.time()
            })

            # 2️⃣ Store command for behavior analysis
            session_commands.append({
                "session_id": server.session_id,
                "event_type": "command",
                "data": {"cmd": command},
                "time": time.time()
            })

            # 3️⃣ Run behavior analysis once we have enough data
            if len(session_commands) >= 2:
                behavior_profiles = extract_behavior_features(session_commands)
                features = behavior_profiles.get(server.session_id)

                if features:
                    attacker_profile = classify_attacker(features)

                    # 🔥 Autonomous decision engine
                    current_strategy = decide_deception_strategy(
                        features, attacker_profile
                    )

            # Fallback strategy (early commands)
            if not current_strategy:
                current_strategy = {
                    "deception_depth": "low",
                    "realism_level": "basic",
                    "response_style": "generic",
                    "engagement_goal": "observe",
                    "environment_change": False
                }

            # 5️⃣ Controlled GenAI execution
            response = generate_fake_response(command, current_strategy)

            channel.send(response + "\n$ ")

        except Exception as e:
            print("Session error:", e)
            break

    channel.close()
    transport.close()



def start_honeypot(host="0.0.0.0", port=2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(100)

    print(f"[+] SSH Honeypot listening on port {port}")

    while True:
        client, addr = sock.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()


if __name__ == "__main__":
    start_honeypot()
