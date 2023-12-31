# Rotate !T

## Write-up

From the title of the challenge, we can see that it is about a rotation in the enc text, so we might think about **Caesar Code**.

Here is the code for encryption/decryption (with brute force):

```py
import sys
from string import *

ENCRYPTED_TEXT = ""

n = 26
flag = ''

for KEY in range(26):
    for i in ENCRYPTED_TEXT:
        if i.isalpha():
            if i.islower():
                shift = 97
            else:
                shift = 65

            j = ord(i)-int(KEY)-shift
            flag += chr(j % n + shift)
        else:
            flag += i

    print(flag)
```

## Flag

gomycode{ca3$4r_i$_$o_OlD}
