from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server

record = {}


class DynamicResolver(object):
    def _doDynamicResponse(self, query):
        name = query.name.name

        if name not in record or record[name] < 1:
            ip = "104.160.43.154"
        else:
            ip = "171.18.0.2"

        if name not in record:
            record[name] = 0
        record[name] += 1

        print name + " ===> " + ip

        answer = dns.RRHeader(name=name,
                              type=dns.A,
                              cls=dns.IN,
                              ttl=0,
                              payload=dns.Record_A(address=b'%s' % ip, ttl=0))
        answers = [answer]
        authority = []
        additional = []
        return answers, authority, additional

    def query(self, query, timeout=None):
        return defer.succeed(self._doDynamicResponse(query))


def main():
    factory = server.DNSServerFactory(clients=[
        DynamicResolver(),
        client.Resolver(resolv='/etc/resolv.conf')
    ])

    protocol = dns.DNSDatagramProtocol(controller=factory)
    reactor.listenUDP(53, protocol)
    reactor.run()


if __name__ == '__main__':
    raise SystemExit(main())