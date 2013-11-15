

def expand_ipv6_zeroes(ipv6_address):
    splits = ipv6_address.split(':')
    if len(splits) == 0:
        return ipv6_address
    new_addr = ''
    for split in splits:
        length = len(split)
        if length == 4:
            new_addr = '%s:%s' % (new_addr, split)
            continue
        num_zeroes = 4 - length
        new_addr = '%s:%s%s' % (new_addr, '0' * num_zeroes, split)
    return new_addr
