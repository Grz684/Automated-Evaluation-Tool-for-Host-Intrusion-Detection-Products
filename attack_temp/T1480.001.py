import sys
import ipaddress
import os
import socket


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        sys.exit(1)


def generate_key(ip):
    key = int(ipaddress.IPv4Address(ip)) % 256
    return key


def xor_encrypt_decrypt(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted_data = bytearray([b ^ key for b in data])

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python encrypt_decrypt.py <encrypt/decrypt> <input_file> <output_file> [target_ip]")
        print("Note: If target_ip is not provided, the local IP will be used.")
        sys.exit(1)

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if len(sys.argv) == 5:
        target_ip = sys.argv[4]
    else:
        target_ip = get_local_ip()
    key = generate_key(target_ip)

    if operation not in ['encrypt', 'decrypt']:
        print("Invalid operation. Please use 'encrypt' or 'decrypt'.")
        sys.exit(1)

    xor_encrypt_decrypt(input_file, output_file, key)
    print(f"{'Encryption' if operation == 'encrypt' else 'Decryption'} completed. Check {output_file} for the result.")
