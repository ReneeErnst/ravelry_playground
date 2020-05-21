import os
import subprocess
import argparse

ENV_IMAGE_NAME = 'ravelry_playground:latest'


def parse():
    """
    Arguments to be passed as needed for running the model
    :return: parser for needed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--container')
    parser.add_argument('--remote', action='store_true')

    return parser.parse_args()


def run_cauldron(remote=True):
    """Start ravelry playground container running Cauldron"""

    current_directory = os.path.realpath(os.curdir)
    if remote:
        entry = '--entrypoint=/bin/bash'
    else:
        entry = ''

    cmd = [
        'docker', 'run',
        '-it', '--rm',
        '--workdir=/project',
        f'--volume={current_directory}:/project',
        '-p=5010:8000',
        entry,
        ENV_IMAGE_NAME
    ]

    print('[EXECUTING]: {}\n'.format(' '.join(cmd).replace(' --', '\n   --')))

    result = subprocess.run(cmd)
    return result.returncode


def run_command_line():
    """Start ravelry playground container"""

    current_directory = os.path.realpath(os.curdir)

    cmd = [
        'docker', 'run',
        '-it', '--rm',
        '--workdir=/project',
        f'--volume={current_directory}:/project',
        ENV_IMAGE_NAME,
        '/bin/bash'
    ]

    print('[EXECUTING]: {}\n'.format(' '.join(cmd).replace(' --', '\n   --')))

    result = subprocess.run(cmd)
    return result.returncode


def main():
    """
    Run associated function based on action input
    :return: run action
    """
    args = parse()
    if args.container == 'cauldron':
        return run_cauldron(remote=args.remote)
    elif args.action == 'command_line':
        return run_command_line()
    raise ValueError(f'Unknown action "{args.container}"')


if __name__ == '__main__':
    main()
