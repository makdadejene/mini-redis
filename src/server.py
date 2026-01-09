import socket 
import threading


class MiniRedis:
    def __init__(self, host, port):
        self.socket = socket.create_server((host, port), reuse_port=True)

    def ping_pong(self, sock, raddr):
        pong_encode = "+PONG\r\n".encode("utf-8")
        while(True):
            data = sock.recv(1024)
            if not data:
                print(f"Client {raddr} disconnected.")
                break
            sock.sendall(pong_encode)
        
    def echo(self, sock, raddr):
        pass

    def multi_client(self, method):
        if method == 'ping_pong':
            target = self.ping_pong
        elif method == 'echo':
            target = self.echo
        while True:
            client_sock, client_addr = self.socket.accept()
            thread = threading.Thread(target=target, args = (client_sock, client_addr))
            thread.start()


def main():
    redis = MiniRedis('localhost', 6379)
    redis.multi_client('echo')


if __name__ == "__main__":
    main()
