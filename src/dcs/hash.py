import hashlib

MOD_H = 2 ** 64
MOD_G = 128
MASK_INIT = 1 << 63


def h(src_ip: int, dest_ip: int) -> int:
    """First-level bucket hash
    """
    src_dst = (str(src_ip) + "-" + str(dest_ip)).encode()
    hashed = int(hashlib.md5(src_dst).hexdigest(), 16) % MOD_H
    mask = MASK_INIT
    i = 0

    # "and i < 63" just to ensure that the loop ends for a very unlikely edge case of hashed = 0
    while hashed & mask == 0 and i < 63:
        mask = mask >> 1
        i += 1

    return i


# TODO: MOD_G as input? to fit the required number of buckets of the sketch?
def g(j: int, src_ip: int, dest_ip: int) -> int:
    """Second-level bucket hash
    """
    src_dst = (str(src_ip) + "-" + str(dest_ip) + "-" + str(j)).encode()
    i = int(hashlib.md5(src_dst).hexdigest(), 16) % MOD_G
    return i
