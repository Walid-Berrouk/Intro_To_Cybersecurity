import random
from string import ascii_lowercase, digits

flag = ""

chars = ascii_lowercase + digits

random.seed(2 ** 1337 - 1)

shuffled_chars = [i for i in chars]
random.shuffle(shuffled_chars)
shuffled_chars = "".join(shuffled_chars)
# print(f"{chars}\n{''.join(shuffled_chars)}");input()

enc = ""
for i in flag:
    if i.isalnum():
        try:
            enc += shuffled_chars[chars.index(i)]
        except:
            enc += i
    else:
        enc += i

print(enc)
#  ydv90d2n{cnn2_vecu_ro_xms21v_dx_9Oe_2go}