import pytest

from .utils import (
    ip2int,
    int2ip,
    pair,
    unpair
)


@pytest.fixture
def ips():
    src_ip = "10.20.5.1"
    dest_ip = "10.20.5.19"

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
