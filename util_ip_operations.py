import socket
import sys

import netaddr


class IPOperations:
    def __init__(self, targets):
        self.ipscope = None
        self.targets = targets

    def sort_ip(self):
        ip_addresses = []
        if ',' in self.targets:
            self.ipscope = self.targets.split(',')
        else:
            self.ipscope = [self.targets]
        for scope in self.ipscope:
            # cannot mix CIDR and iprange notation
            if '/' in scope and '-' in scope:
                msg = '[!] Mailformed target IP %s ' % scope
                print msg
                sys.exit()

            # CIDR
            if '/' in scope:
                try:
                    mask = int(scope.split('/')[1])
                except:
                    msg = '[!] Illegal CIDR mask.'
                    print msg
                    sys.exit()
                if mask not in range(1, 32):
                    msg = '[!] Illegal CIDR mask.'
                    print msg
                    sys.exit()
                valid = self.check_valid_ip(scope.split('/')[0])
                if valid:
                    for ip in netaddr.IPNetwork(scope).iter_hosts():
                        ip_addresses.append(str(ip))
                else:
                    msg = '[!] Mailformed target IP.'
                    print msg
                    sys.exit()

            # iprange
            elif '-' in scope:
                iprange = scope.split('-')
                if len(iprange) != 2:
                    msg = '[!] Mailformed target IP.'
                    print msg
                    sys.exit()
                else:
                    for ip in iprange:
                        valid = self.check_valid_ip(ip)
                        if not valid:
                            msg = '[!] Mailformed target IP.'
                            print msg
                            sys.exit()
                    start, end = iprange
                    ip_list = list(netaddr.iter_iprange(start, end))
                    for ip in ip_list:
                        ip_addresses.append(str(ip))

            # SINGLE IP
            else:
                valid = self.check_valid_ip(scope)
                if not valid:
                    msg = '[!] Mailformed target IP.'
                    print msg
                    sys.exit()
                else:
                    ip_addresses.append(scope)

        return ip_addresses

    @staticmethod
    def check_valid_ip(ip):
        try:
            socket.inet_aton(ip)
            return 1
        except:
            return 0
