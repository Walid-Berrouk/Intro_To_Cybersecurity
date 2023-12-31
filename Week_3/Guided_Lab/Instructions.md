# Guided Lab: XOR Encryption

## Introduction

Welcome to this First guided lab, today we will be talking about **XOR Encryption System** and how can be used in order to encrypt/decrypt some data. We will also pratice some basic python instructions and libraries used for this purpose.

Follow along and try to hack the system !

## Description

In this lab, we will be encrypting, decrypting some data using the **XOR Operation**. This helps us, using a simple cryptosystem understand the cryptography mechanisms and visualize the changes in our data.

The Lab will be devided in two parts:

- **XOR Algorithm:** Where we will be writing the encryption/decryption code using python
- **XOR Limitations:** Where we will explore one or two attacks than can help us break this cryptosystem.

## Instructions

### Write your first XOR cryptosystem

There are several ways to write a xor code for data encryption/decryption.

#### 1. From scratch

In python, there is a simple operation that can operate a xor on numbers:

```python
xor_num = num1 ^ num2
```

Where `num1` and `num2` are numbers. From, we can start writing our code.

As we know, we will be manipulating messages, which in the context of python will be `string`. But in order to apply the `xor` operatore, we will need to transform them into series of `bytes` using the `b""` prefix or the `bytearray()` function.

From there, the algorithm we will be to apply for a specific key, a xor, character by character, on each of the plaintext bytes:

```python
def encrypt(plaintext, key):
    ciphertext = bytearray([plaintext[i] ^ key[ i % len(key)] for i in range(len(plaintext))])
    return ciphertext
```

Note that the length of the key is less than the plaintext, so we will need to repeat it after each end. The return of the function will be a `bytearray` as well.

Now, we should in the main program declare each of the variables:

```python
plaintext = b"Hello, My name is Walid, and I'm here to introduce to you the xor operator"
key = b"rebustKey"
```

From there, apply the encryption function and see the result.

For the decryption part, lucky you ! the same process is used for the decryption.

**Task:** Tranform the previous function so it can do decryption as well (change variable names where necessary).

#### 2. Using a predefined function

There are few libraries in python that helps make xor usage easier, here is an example for `xor()` function implimented in python from `Crypto.util` library.

```python
from Crypto.Util.strxor import 

plaintext = b"Hello, My name is Walid, and I'm here to introduce to you the xor operator"
key = b"rebustKey"

print(strxor(plaintext, key)
```

### Known Plaintext Vulnerability

XOR algorithms for data encryption are not used nowadays due to several vulnerabilities. One of them is called the **Known Plaintext**.

**Idea:** the idea of this attack is that, when a part of the plaintext is know, as the xor is a symmetric operation, it can be used to retreive the data.

Observe the following code:

```python
from random import randint as ri

def encrypt(plaintext, key):
    ciphertext = bytearray([plaintext[i] ^ key[i%len(key)] for i in range(len(plaintext))])
    return ciphertext

flag = b"gomycode{redacted}"
assert len(flag)%11==0
mykey = bytearray([ri(0, 255) for _ in range(11)])  
enc = encrypt(flag, mykey)
print(enc)
```

In this example, even if the key is random at each execution. For a specific execution, we can still retreive the flag as we know its first part `gomycode{`.

Let's see how that works.

First, here is the encrypted flag:

```python
enc = b"\x9e\x99\x01\x8b\xa8\xf77\x13\x1d\xfen\x8b\xa9]\x81\x94\xc8\x01E\x12\xf2\'\xa6\xa09\xbe\x85\xdd!B$\xca#"
```

From there, let's use the known part, and apply it on the ciphertext. Use the following code:

```python
from pwn import xor
ct = b"\x9e\x99\x01\x8b\xa8\xf77\x13\x1d\xfen\x8b\xa9]\x81\x94\xc8\x01E\x12\xf2\'\xa6\xa09\xbe\x85\xdd!B$\xca#"
def encrypt(plaintext, key):
    ciphertext = bytearray([plaintext[i] ^ key[i%len(key)] for i in range(len(plaintext))])
    return ciphertext
otp1 = b"gomycode{"
first_part = encrypt(ct, otp1)[:9]
print(first_part)
```

This code helps us indeed recover the first part of the key, but as you can see in the previous code, the key has a `11` length long, so the final product should be in `11` bytes. For that, we will need to use brute force. here is the full code:

```python
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
```

## Flag

gomycode{X0r_1s_PR3tTy_VULNEr4Bl}
