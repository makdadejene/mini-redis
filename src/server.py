import socket 
import threading


class MiniRedis:
    def __init__(self, host, port):
        self.socket = socket.create_server((host, port), reuse_port=True)
            
    def ping_pong(self, sock):
        pong_encode = "+PONG\r\n".encode("utf-8")
        sock.sendall(pong_encode)
        
    def echo(self, sock, msg):
        complete_msg = "+" + msg + "\r\n"
        echo_msg_encode = complete_msg.encode("utf-8")
        sock.sendall(echo_msg_encode)
        
    def process_data(self, sock, raddr):
        buffer = b""
        while(True):
            data = sock.recv(1024)
            if not data:
                print(f"Client {raddr} disconnected.")
                break
            buffer += data
            
            while(True):
                items, buffer = self.parse_array(buffer)
                if items is None:
                    break
                self.match_command(sock, items)
                print(f"Received command from {raddr}: {items}")

    
    def match_command(self, sock, items):
        if items[0] == 'PING':
            self.ping_pong(sock)
        elif items[0] == 'ECHO':
            if len(items) < 2:
                print(f"No echo message recieved")
            else:
                self.echo(sock, items[1])

    def parse_bulk_string(self, data_type, line_end, buffer):
        bulk_string_len = int(data_type[1:]) 
        buffer = buffer[line_end + 2:]  

        if len(buffer) < bulk_string_len + 2:
            return None, buffer  

        value = buffer[:bulk_string_len]
        buffer = buffer[bulk_string_len + 2:]  

        return value.decode('utf-8'), buffer

  
    def parse_array(self, buffer):

        items = []
        if not buffer.startswith(b'*'):
            return None, buffer
        
        # incomplete header
        line_end = buffer.find(b'\r\n')
        if line_end == -1:
            return None, buffer
        
        array_len = int(buffer[1:line_end])
        print(array_len)

        # remove header
        buffer = buffer[line_end+2:]

        for _ in range(array_len):
            line_end = buffer.find(b'\r\n')
            if line_end == -1:
                return None, buffer
            data_type = buffer[:line_end]

            if data_type.startswith(b'$'):
                value, buffer = self.parse_bulk_string(data_type, line_end, buffer)
                if value is None:
                    return None, buffer
                items.append(value)
            else:
                return None, buffer
            
        return items, buffer

        
    def handle_client(self):
        while True:
            client_sock, client_addr = self.socket.accept()
            thread = threading.Thread(target=self.process_data, args = (client_sock, client_addr))
            thread.start()


def main():
    redis = MiniRedis('localhost', 6379)
    redis.handle_client()


if __name__ == "__main__":
    main()
