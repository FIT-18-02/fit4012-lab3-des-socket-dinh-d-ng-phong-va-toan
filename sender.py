import os
import socket
from des_socket_utils import encrypt_des_cbc, build_packet

SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', '6000'))
MESSAGE_ENV = os.getenv('MESSAGE')
LOG_FILE = os.getenv('SENDER_LOG_FILE', '')


def get_message() -> bytes:
    if MESSAGE_ENV is not None:
        return MESSAGE_ENV.encode('utf-8')
    plain = input("Nhập bản tin: ")
    return plain.encode('utf-8')


def main() -> None:
    plain = get_message()
    key, iv, cipher_bytes = encrypt_des_cbc(plain)
    overall = build_packet(key, iv, cipher_bytes)

    mode = os.getenv('TEST_MODE', '')

if mode == 'truncate':
    overall = overall[:10]  # gửi thiếu dữ liệu
elif mode == 'bad_length':
    overall = overall[:-5]  # phá header
elif mode == 'bad_padding':
    cipher_bytes = cipher_bytes[:-1] + b'\x00'
    overall = build_packet(key, iv, cipher_bytes)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(overall)
    except Exception as e:
        print(f"[!] Lỗi gửi: {e}")

    lines = [
        "[+] Đã gửi bản mã.",
        f"Key: {key.hex()}",
        f"IV: {iv.hex()}",
        f"Ciphertext: {cipher_bytes.hex()}",
    ]
    for line in lines:
        print(line)

    if LOG_FILE:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
