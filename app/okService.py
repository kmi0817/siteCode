import okKey

def twoChannelEncrytion(key1, key2, iv, body):
    # import os
    # key1 = os.urandom(32)
    # iv = os.urandom(16)
    # key2 = os.urandom(32)  
    split = [bytearray(), bytearray()]
    for i in range(len(body)):
        split[i%2].append(body[i])
    body1 = okKey.encrypt(key1, iv, split[0])
    body2 = okKey.encrypt(key2, iv, split[1])
    # return key1, key2, iv, body1, body2
    return body1, body2

def twoChannelDecrytion(key1, key2, iv, body1, body2):
    split1 = okKey.decrypt(key1, iv, body1)
    split2 = okKey.decrypt(key2, iv, body2)
    body = bytearray()
    for i in range(len(split1)):
        body.append(split1[i])
        body.append(split2[i])
    return body

def twoChannelStore(body1, body2):
    hash1 = "sCDC0109267107"
    file1 = open(hash1, 'w')
    file1.write(body1)
    file1.close()
    hash2 = "secM0803220193"
    file2 = open(hash2, 'w')
    file2.write(body2)
    file2.close()
    return hash1, hash2
    
def twoChannelLoad(hash1, hash2):
    file1 = open(hash1, 'r')
    body1 = file1.read()
    file1.close()
    file2 = open(hash2, 'r')
    body2 = file2.read()
    file2.close()
    return body1, body2

# def twoChannelStore(body1, body2):
#     import ipfshttpclient
#     file1 = open('stopGap/temp1.txt', 'w')
#     file1.write(body1.decode())
#     file1.close()
#     # file2 = open('stopGap/temp2.txt', 'w')
#     # file2.write(body2.decode())
#     # file2.close()
#     with ipfshttpclient.connect() as client:
# 	    hash1 = client.add('stopGap/temp1.txt')['Hash']
# 	    print(client.stat(hash))

#     # try:
#     #     client = ipfshttpclient.connect()
#     # except Exception as e:
#     #     print('ipfs: ', e)
#     # hash1 = client.add('stopGap/temp1.txt')['hash']
#     # # hash2 = client.add('stopGap/temp2.txt')['hash']
#     return hash1 #, hash2

# def twoChannelLoad(hash1, hash2):
#     import ipfshttpclient
#     try:
#         client = ipfshttpclient.connect()
#     except Exception as e:
#         print('ipfs: ', e)
#     body1 = client.cat(hash1)
#     body2 = client.cat(hash2)
#     return body1, body2
