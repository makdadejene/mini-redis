import threading
import time
from src.server import MiniRedis  
import socket


class RedisClient:
    def __init__(self, host='localhost', port=6379):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def ping(self, count=1):
        for _ in range(count):
            self.sock.sendall(b'PING\r\n')
            response = self.sock.recv(1024)
            if response != b'+PONG\r\n':
                raise Exception(f"Unexpected response: {response}")

    def close(self):
        self.sock.close()


def run_test():
    print("Starting concurrency test...")

    server = MiniRedis('localhost', 6379)
    server_thread = threading.Thread(target=server.multi_pong, daemon=True)
    server_thread.start()

    time.sleep(0.5)  

    client1 = RedisClient()
    client1.ping(1)

    client2 = RedisClient()
    client2.ping(2)

    client1.ping(2)
    client2.ping(1)

    print("Client 1 success, closing...")
    client1.close()

    client3 = RedisClient()
    client3.ping(3)

    print("Client 2 success, closing...")
    client2.close()
    print("Client 3 success, closing...")
    client3.close()

    print("Concurrency test finished successfully!")


if __name__ == "__main__":
    run_test()
