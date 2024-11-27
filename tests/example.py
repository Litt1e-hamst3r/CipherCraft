import hashlib

def md5_checksum(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()

# 发送方
data = "hello world"
checksum = md5_checksum(data)
print("发送的数据：", data)
print("校验值：", checksum)

# 接收方
received_data = "hello world"
received_checksum = md5_checksum(received_data)
print("接收的数据：", received_data)
print("接收到的校验值：", received_checksum)

if received_checksum == checksum:
    print("数据没有被篡改")
else:
    print("数据可能已被篡改")
