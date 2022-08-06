import socket
from PIL import Image

img_size = (1000, 1000)

addr = 'localhost'
port = '5050'


def resize_img_prop(image, new_size=(100, 100)):
    """
    Возвращает картинку, пропорционально изменив ее размер до заданных значений
    """
    k_w, k_h = new_size[0] / image.size[0], new_size[1] / image.size[1]
    if k_w > k_h:
        new_size = (int(image.size[0] * k_h), new_size[1])
    elif k_w < k_h:
        new_size = (new_size[0], int(image.size[1] * k_w))
    return image.resize(new_size)


def run_service(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        conn, client_address = sock.accept()
        try:
            while True:
                img = conn.recv(1024)
                if img:
                    img = resize_img_prop(img, img_size)
                    conn.sendall(img)
                else:
                    break
        finally:
            conn.close()


if __name__ == '__main__':
    run_service((addr, port))
