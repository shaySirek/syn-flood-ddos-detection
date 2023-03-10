import ipaddress
import numpy as np


LOG_M = 32


def ip2int(ip): return int(ipaddress.IPv4Address(ip))
def int2ip(ip): return str(ipaddress.IPv4Address(ip))


def pair(src_ip: int, dest_ip: int) -> int:
    src_dest = (dest_ip << LOG_M) + src_ip
    return src_dest


def unpair(src_dest_pair: int) -> tuple[int, int]:
    src_ip = src_dest_pair & ((1 << LOG_M) - 1)
    dest_ip = src_dest_pair >> LOG_M

    return src_ip, dest_ip


def bit_array(src_ip: int, dest_ip: int):
    """ output.shape = (2*log_m + 1) = 65
    """
    src_dest = pair(src_ip, dest_ip)

    src_dest_arr = np.array([src_dest]).astype(int)
    src_dest_bits = (
        ((src_dest_arr[:, None] & (1 << np.arange(2*LOG_M)))) > 0).astype(int)[0]
    one_src_dest_bits = np.concatenate(
        (np.ones((1), dtype=int), src_dest_bits), axis=0)

    return one_src_dest_bits
