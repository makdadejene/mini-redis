import socket 
import threading


class MiniRedis:
    def __init__(self, host, port):
        self.socket = socket.create_server((host, port), reuse_port=True)

    def ping_pong(self):
        pong_encode = "+PONG\r\n".encode("utf-8")
        while(True):
            sock, raddr = self.socket.accept() 
            while(True):
                data = sock.recv(1024)
                if not data:
                    print(f"Client {raddr} disconnected.")
                    break
                sock.sendall(pong_encode)


def main():
    redis = MiniRedis('localhost', 6379)
    redis.ping_pong()


if __name__ == "__main__":
    main()
