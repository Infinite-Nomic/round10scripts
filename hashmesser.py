#########################################################################
# A hashmesser for generating meme sha256 hashes.                       #
# Currently supports something around 94^4 attempts before timing out.  #
# I might add arbitrary nesting with a timeout sometime later idk       #
#                                                                       #
# Nyhilo                                                                #
#########################################################################

import hashlib


def get_sha_256(string):
    encoded = string.encode()
    result = hashlib.sha256(encoded)

    return result.hexdigest()


def mess(msg, placeholder, check):
    '''Msg should include the placeholder string'''

    if placeholder not in msg:
        return "No placeholder string."

    left, right = msg.split(placeholder)

    for i in range(33, 127):
        for j in range(33, 127):
            for k in range(33, 127):
                for l in range(33, 127):
                    salt = f'{chr(i)}{chr(j)}{chr(k)}{chr(l)}'

                    hash = get_sha_256(left + salt + right)
                    if check in hash:
                        return (salt, hash)

    return("None found :(")
