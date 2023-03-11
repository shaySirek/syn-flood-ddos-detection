import pytest

from .utils import (
    ip2int,
    int2ip,
    pair,
    unpair,
    bit_array,
    bit_array_to_pair
)


@pytest.fixture
def ips():
    src_ip = "192.168.10.1"
    dest_ip = "120.100.200.25"

    return src_ip, dest_ip


def test_convert(ips):
    src_ip, dest_ip = ips
    int_src_ip = ip2int(src_ip)
    int_dest_ip = ip2int(dest_ip)

    back_src_ip = int2ip(int_src_ip)
    back_dest_ip = int2ip(int_dest_ip)

    assert src_ip == back_src_ip
    assert dest_ip == back_dest_ip


def test_pairing(ips):
    src_ip, dest_ip = ips
    original_ips_int = ip2int(src_ip), ip2int(dest_ip)

    src_dest_pair = pair(*original_ips_int)
    unpaired_ips = unpair(src_dest_pair)

    assert unpaired_ips == original_ips_int


def test_bitarray(ips):
    src_ip, dest_ip = ips
    original_ips_int = ip2int(src_ip), ip2int(dest_ip)

    bits = bit_array(*original_ips_int)
    unpaired_ips = bit_array_to_pair(bits)

    assert unpaired_ips == original_ips_int


def test_bitarray_multiple(ips):
    src_ip, dest_ip = ips
    original_ips_int = ip2int(src_ip), ip2int(dest_ip)

    bits = bit_array(*original_ips_int)
    bits = 10 * bits
    
    unpaired_ips = bit_array_to_pair(bits)

    assert unpaired_ips == original_ips_int
    

def test_bitarray_none(ips):
    src_ip, dest_ip = ips
    original_ips_int = ip2int(src_ip), ip2int(dest_ip)

    bits = bit_array(*original_ips_int)
    bits = 10 * bits
    bits[5] += 1
    
    unpaired_ips = bit_array_to_pair(bits)

    assert unpaired_ips is None
