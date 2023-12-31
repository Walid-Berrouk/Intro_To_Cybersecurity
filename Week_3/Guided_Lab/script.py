from pwn import xor
ct = b"\x9e\x99\x01\x8b\xa8\xf77\x13\x1d\xfen\x8b\xa9]\x81\x94\xc8\x01E\x12\xf2\'\xa6\xa09\xbe\x85\xdd!B$\xca#"
def encrypt(plaintext, key):
    ciphertext = bytearray([plaintext[i] ^ key[i%len(key)] for i in range(len(plaintext))])
    return ciphertext
otp1 = b"gomycode{"
first_part = encrypt(ct, otp1)[:9]
otp2 = b"}"
last_part = xor(otp2, ct[-1])
for i in range(256):
    b = bytes(first_part)+bytes([i])+bytes(last_part)
    print(encrypt(ct, b))