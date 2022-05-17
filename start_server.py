from argparse import ArgumentParser

from r2_facial_recognition.server.app import create_app

parser = ArgumentParser()
parser.add_argument('-ip', '--host', action='store')
parser.add_argument('-p', '--port', action='store', type=int)
parser.add_argument('-d', '--debug', action='store_true', default=False)

args, _ = parser.parse_known_args()
host = getattr(args, 'host')
port = getattr(args, 'port')
debug = getattr(args, 'debug')

if __name__ == '__main__':
    create_app().run(debug=debug, host=host, port=port)
