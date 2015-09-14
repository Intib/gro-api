#!/usr/bin/env python3
import os
import shelve
import argparse

def configure():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dev', '-d', dest='development', action='store_true', default=False,
        help='Run in development mode'
    )
    parser.add_argument(
        '--root', '-r', dest='root', action='store_true', default=False,
        help='Run a root server'
    )
    args = parser.parse_args()

    base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    env_vars_path = os.path.join(base_path, 'env_vars')

    env_vars = shelve.open(env_vars_path)
    try:
        env_vars['GRO_API_ROOT'] = base_path

        if args.development:
            env_vars['GRO_API_SERVER_MODE'] = 'development'
        else:
            env_vars['GRO_API_SERVER_MODE'] = 'production'

        if args.root:
            env_vars['GRO_API_SERVER_TYPE'] = 'root'
        else:
            env_vars['GRO_API_SERVER_TYPE'] = 'leaf'
    finally:
        env_vars.close()

if __name__ == '__main__':
    configure()
