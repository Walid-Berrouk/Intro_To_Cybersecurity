# Unrecoverable

## Write-up

One property of the random generated seeds, taken from Random generators, is that given the same initial value, it generate same results.

So, as we give it same value, and using same algorithm, we get the flag:



```python
import random 
from string import ascii_lowercase,digits

enc = "ydv90d2n{cnn2_vecu_ro_xms21v_dx_9Oe_2go}"

random.seed(2**1337 - 1)

chars = ascii_lowercase + digits 

shuffled_chars=[i for i in chars]
random.shuffle(shuffled_chars)
shuffled_chars = ''.join(shuffled_chars)


flag = ''
for i in enc:
    if i.isalnum():
        try:
            flag += chars[shuffled_chars.index(i)]
        except: 
            flag += i
    else:
        flag += i

print(flag)
```

## Flag

`gomycode{seed_must_b3_rand0m_or_yOu_d13}`
