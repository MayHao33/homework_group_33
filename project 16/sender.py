import socket

def establish_connection():
    host = '127.0.0.1'  # 接收者主机的IP地址
    port = 1234  # 接收者监听的端口号

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    return s

# 建立与接收者的连接
conn = establish_connection()
ciphertext = b'Some ciphertext data'  # 替换为实际的密文数据
conn.send(ciphertext)
conn.close()
