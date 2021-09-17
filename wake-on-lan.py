import argparse
import re
import binascii
import socket


def parse_mac_addr(mac_addr: str):
    result = re.findall(r'(?: |^)([0-9a-fA-F]{2}(?:[:\.-][0-9a-fA-F]{2}){5})(?: |$)', mac_addr)
    if len(result) > 0:
        mac_str = re.sub(r'[:\.-]', '', result[0].lower())
        mac = binascii.unhexlify(mac_str)
        return mac
    return None


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        default='255.255.255.255',
        metavar='IPADDR',
        help='IPv4 address of relay (default 255.255.255.255)',
    )
    parser.add_argument(
        '-p',
        default=9,
        metavar='PORT',
        type=int,
        help='Port to send the packet to (default 9)'
    )
    parser.add_argument(
        'MAC',
        help='MAC address of device to wake up'
    )
    args = parser.parse_args()

    # Arguments validation
    if not 0 <= args.p <= 65535:
        print(f'Incorrect port in -p parameter: {args.p}')
        exit(1)

    mac = parse_mac_addr(args.MAC)
    if mac is None:
        print(f'Incorrect MAC address: {args.MAC}')
        exit(1)

    return args.d, args.p, mac


def make_magic_packet(mac_addr: bytes):
    return b'\xff' * 6 + mac_addr * 16


def send_wake_on_lan(ip: str, port: int, mac: bytes):
    packet = make_magic_packet(mac)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        print(f'Sending wake-on-LAN packet...')
        if ip == '255.255.255.255':
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            ip = '<broadcast>'

        try:
            sock.sendto(packet, (ip, port))
            print('Done')
        except Exception as err:
            print(f'Error has occurred: {err}')


def main():
    ipaddr, port, mac = get_args()
    send_wake_on_lan(ipaddr, port, mac)


if __name__ == '__main__':
    main()
