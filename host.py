#!/usr/bin/env python3

import os
import sys
import subprocess
import socket
import requests

if __name__ != "__main__":
    print(f"{os.path.basename(__file__)} is not meant to be used as a module")
    sys.exit(1)

def main():
    # Generate or retrieve encryption key
    crypt_path = 'crypt.exe'
    if os.path.isfile(crypt_path):
        result = subprocess.run(
            [crypt_path, 'generate_key'],
            capture_output=True,
            text=True
        )
        key = result.stdout.strip()
        print(f"Generated key: {key}")
    else:
        print(f'"{crypt_path}" not found')
        sys.exit(1)

    # Create TCP server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8000

    # Get public IP
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        public_ip = response.text
    except requests.RequestException as e:
        print(f"Failed to get public IP: {e}")
        sys.exit(1)

    print(f"Your IP Address:   {public_ip}")
    print(f"Your Port Number:  {port}")
    print(f"Hostname:          {host}\n")

    # Bind and listen
    try:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected User:    {addr}")

            data = client_socket.recv(1024)
            print(f"Received data:     {data.decode(errors='replace')}")
            client_socket.close()

    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
