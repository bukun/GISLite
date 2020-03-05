'''
Deploy GISLite on server side.
'''
from fabric import Connection

from cfg import mach


def main():
    print("{}@{}".format(mach['u'], mach['h']))
    c = Connection(
        "{}@{}".format(mach['u'], mach['h']),
        port=11022,
        connect_kwargs={"password": mach['p']}
    )

    with c.cd(mach['ws']):
        c.run('git reset --hard')
        c.run('git pull')
        c.run('python3 deploy.py')


if __name__ == '__main__':
    main()
