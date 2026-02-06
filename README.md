
SSH Honeypot in Python

Overview
This project is a Python-based SSH honeypot built using the Paramiko library.
It simulates an SSH server to attract and monitor unauthorized access attempts for security research and educational purposes.

The honeypot captures and logs:
- Username and password attempts
- Attacker IP addresses
- Commands executed during sessions

Features
- Simulates an SSH server on a configurable port (default: 2222)
- Uses RSA key for SSH handshake and encryption
- Logs both successful and failed authentication attempts
- Provides a fake interactive shell with limited commands
- Supports multiple concurrent attacker connections using multithreading
- Stores logs in structured JSON format
- Includes a visualization script for attack analysis

Project Structure

.
├── honeypot.py
├── logger.py
├── visualize.py
├── README.md


Requirements
- Python 3.x
- Paramiko
- Matplotlib (optional, for visualization)

Install required packages:
```bash
pip install paramiko matplotlib
````

Files Not Included in Repository
The following files and folders are not included and are generated locally:

* venv/ – Virtual environment
* logs/ – Runtime log files
* test_rsa.key – Private SSH key

Generate SSH Server Key
Before running the honeypot, generate an RSA key locally:

```bash
ssh-keygen -t rsa -b 2048 -f test_rsa.key
```


Running the Honeypot
Start the SSH honeypot server:

```bash
python honeypot.py
```

The server listens on port 2222 by default.

Connect to the Honeypot

```bash
ssh -p 2222 admin@<server-ip>
```


Logs and Data
At runtime, the project automatically creates a logs directory:

* logs/attempts.json
* logs/commands.json
* logs/honeypot.log

Visualization
To visualize attacker login attempts by IP address:

```bash
python visualize.py
```

Extending the Project



# Security Notice
This project is intended for educational and controlled environments only.
Do not deploy on production systems without proper isolation.

License
MIT License

Acknowledgments
Built using the Paramiko library and inspired by common SSH honeypot implementations.

