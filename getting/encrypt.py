from Crypto.Cipher import AES

# AES加密
def aes_encrypt(data, key, iv):
    """
    AES加密

    data: 待加密数据

    key: 密钥

    iv: 偏移量
    """
    key = key.encode('utf-8') if isinstance(key, str) else key
    iv = iv.encode('utf-8') if isinstance(iv, str) else iv
    aes = AES.new(key,AES.MODE_CBC,iv)
    return aes.encrypt(data)

# AES解密
def aes_decrypt(rData, key, iv):
    """
    AES解密

    rData: 加密数据
    
    key: 密钥
    
    iv: 偏移量
    """
    key = key.encode('utf-8') if isinstance(key, str) else key
    iv = iv.encode('utf-8') if isinstance(iv, str) else iv
    aes = AES.new(key,AES.MODE_CBC,iv)
    decoded_data = base64.b64decode(rData)
    # 解密
    decrypted_data = aes.decrypt(decoded_data)
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]
    return decrypted_data.decode('utf-8') 

import rsa
import os
import base64
import json

# 当前脚本路径
path = os.path.dirname(os.path.abspath(__file__))
# 拼接公钥、私钥文件路径
pub_key_path = os.path.join(path, "pub.pem")
pri_key_path = os.path.join(path, "pri.pem")

# 从 PEM 格式公钥文件中读取公钥
with open(pub_key_path, "rb") as f:
    PUB_KEY = rsa.PublicKey.load_pkcs1(f.read(), format="PEM")
# 从 PEM 格式私钥文件中读取私钥
with open(pri_key_path, "rb") as f:
    PRI_KEY = rsa.PrivateKey.load_pkcs1(f.read(), format="PEM")

# RSA加密
def rsa_encrypt(data):
    """
    RSA加密

    data: 待加密数据
    """
    # 使用公钥加密
    encrypted_data = rsa.encrypt(data.encode(), PUB_KEY)
    # 将加密后的数据进行 Base64 编码以便传输
    return base64.b64encode(encrypted_data).decode()

# RSA解密
def rsa_decrypt(rData):
    """
    RSA解密

    rData: 加密数据
    """
    decoded_data = base64.b64decode(rData)
    decrypted_data = rsa.decrypt(decoded_data, PRI_KEY)
    return decrypted_data.decode()

# 解密ARS加密数据再解密AES加密数据
def decrypt_data(data):
    """
    解密 ARS 加密数据再解密 AES 加密数据

    data: RSA 加密数据
    """
    # 将 Base64 编码的数据解码
    data = base64.b64decode(data).decode()
    # 将 JSON 字符串解析为字典
    jsonData = json.loads(data)
    # 解密 RSA 加密数据，得到包含 AES 加密数据的 JSON 字符串
    arsData = rsa_decrypt(jsonData.get('v'))
    # 将 RSA 解密后的 JSON 字符串解析为字典
    arsData = json.loads(arsData)
    # 使用 AES 解密数据
    aesData = aes_decrypt(jsonData.get('data') , arsData.get('key'), arsData.get('iv'))
    return aesData

# 测试使用
if __name__ == "__main__":
    data = "hello"
    print("原始数据：", data)
    # AES加密
    key = "1234567890123456"
    iv = "1234567890123456"
    rData = aes_encrypt(data, key, iv)
    print("AES加密后：", type(rData))
    # AES解密
    dData = aes_decrypt(rData, key, iv)
    print("AES解密后：", dData)