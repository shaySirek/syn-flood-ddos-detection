from .utils import pair


def h(src_ip: int, dest_ip: int) -> int:
    """First-level bucket hash
    """
    #TODO: 
    return 0


def g(j: int, src_ip: int, dest_ip: int) -> int:
    """Second-level bucket hash
    """
    #TODO:
    src_dest = pair(src_ip, dest_ip)
    return (src_dest + j) % 128
