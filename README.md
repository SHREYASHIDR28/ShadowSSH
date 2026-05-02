# ShadowSSH

## A Real-Time AI System That Engages and Deceives Attackers

ShadowSSH is an autonomous cyber deception system designed to simulate a realistic SSH environment and dynamically respond to attacker behavior.

Unlike traditional honeypots that passively log activity, ShadowSSH actively engages attackers through adaptive deception strategies and controlled generative response mechanisms.

---

## Overview

The system operates as a closed-loop intelligence pipeline:

Attacker → SSH Honeypot → Logging → Behavior Extraction →  
Attacker Profiling → Decision Engine → GenAI Execution → Response

Each attacker interaction is analyzed in real time to extract behavioral signals, which are then used to infer intent and guide deception strategies.

---

## Key Features

- SSH-based deception interface using Paramiko  
- Real-time behavioral feature extraction (command patterns, timing, intent signals)  
- Dynamic attacker profiling (automation detection, reconnaissance, privilege escalation attempts)  
- Autonomous decision engine for adaptive deception strategies  
- Controlled generative execution layer for realistic system responses  
- Session-based architecture enabling continuous behavioral analysis  

---

## System Architecture

1. Attacker connects via SSH  
2. Commands are logged and timestamped  
3. Behavioral features are extracted per session  
4. Attacker intent and characteristics are profiled  
5. A deception strategy is selected dynamically  
6. The system generates a controlled, realistic response  
7. The loop continues with updated context  

---

## Design Principles

- Separation of decision-making and response generation  
- Controlled use of generative models under strict constraints  
- Explainable, rule-based core with extensibility toward ML-based profiling  
- Real-time adaptability based on attacker behavior  

---

## Technologies Used

- Python  
- Paramiko (SSH server simulation)  
- Behavioral feature engineering  
- Rule-based decision systems  
- Generative AI (API-agnostic design)  

---

## Status

The core system is fully implemented and operational, including:

- SSH interaction layer  
- Behavioral analysis pipeline  
- Attacker profiling logic  
- Autonomous decision engine  
- Mock-based generative execution layer  

Planned enhancements include:

- Advanced adaptive memory and session evolution  
- ML-based attacker classification  
- Evaluation metrics for deception effectiveness  
- Integration with production-grade LLM APIs  

---

## Usage Restriction

This project is proprietary.

Unauthorized copying, modification, or use of this code for academic, commercial, or personal purposes is not permitted.

The repository is made public for demonstration and educational viewing only.  
Core components and advanced logic have been intentionally withheld to protect the originality and integrity of the system.

For collaboration or access requests, please contact the author.

---

## Author

Shreyashi Deb Roy
