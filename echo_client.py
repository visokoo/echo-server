import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    sock.connect(server_address)
    received_message = ''
    buffer_size = 16
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf8'))

        chunk = ''
        while True:
            tiny_chunk = sock.recv(buffer_size)
            chunk += tiny_chunk.decode('utf8')
            if len(tiny_chunk) < buffer_size:
                break
            print('received "{0}"'.format(tiny_chunk.decode('utf8')), file=log_buffer)
        received_message = chunk
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        sock.close()
        print('closing socket', file=log_buffer)
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
