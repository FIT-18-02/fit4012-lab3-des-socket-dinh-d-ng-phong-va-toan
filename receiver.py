import os
import socket
from des_socket_utils import HEADER_SIZE, parse_header, recv_exact, decrypt_des_cbc

HOST = os.getenv('RECEIVER_HOST', '0.0.0.0')
PORT = int(os.getenv('RECEIVER_PORT', '6000'))
TIMEOUT = float(os.getenv('SOCKET_TIMEOUT', '10'))
OUTPUT_FILE = os.getenv('RECEIVER_OUTPUT_FILE', '')
LOG_FILE = os.getenv('RECEIVER_LOG_FILE', '')


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        s.settimeout(TIMEOUT)
        print(f"Đang lắng nghe {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print(f"Kết nối từ {addr}")

    try:
        header = recv_exact(conn, HEADER_SIZE)
        key, iv, length = parse_header(header)

        # kiểm tra độ dài
        if length <= 0 or length > 10**6:
            raise ValueError("Độ dài ciphertext không hợp lệ")

        cipher_bytes = recv_exact(conn, length)

        plaintext = decrypt_des_cbc(key, iv, cipher_bytes)
        message = plaintext.decode('utf-8', errors='ignore')

        line = f"[+] Bản tin gốc: {message}"
        print(line)

        if OUTPUT_FILE:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(message)

        if LOG_FILE:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(line + '\n')

    except Exception as e:
        error_line = f"[!] Lỗi: {str(e)}"
        print(error_line)

        if LOG_FILE:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(error_line + '\n')


if __name__ == '__main__':
    main()
