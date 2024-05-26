import time
import socket
import os

def wait_for_db(host, port, timeout=60):
    start_time = time.time()
    while True:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            print("Postgres is up - executing command")
            return
        except socket.error:
            if time.time() - start_time >= timeout:
                raise Exception("Timed out waiting for database to become available")
            print("Postgres is unavailable - sleeping")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db(os.getenv('POSTGRES_HOST', 'db'), int(os.getenv('POSTGRES_PORT', '5432')))
