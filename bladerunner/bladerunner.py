#!usr/bin/python3
import os
import stat
import subprocess
import sys

import inquirer


def make_scripts_dict(base_dir):
    scripts_dict = {}
    for dirname, _, files in os.walk(base_dir):
        scripts = list(filter(lambda filename: filename.endswith('.sh'), files))
        if scripts:
            scripts_dict[dirname] = scripts
    return scripts_dict


def choose_dir(scripts_dict, base_dir):
    choices = list(map(lambda directory: directory[len(base_dir):], scripts_dict.keys()))
    prompt = 'Service'
    questions = [
        inquirer.List(
            prompt,
            message="Choose service:",
            choices=choices,
        ),
    ]
    return inquirer.prompt(questions)[prompt]


def choose_script(scripts):
    prompt = 'Script'
    questions = [
        inquirer.List(
            prompt,
            message="Choose script:",
            choices=scripts,
        ),
    ]
    return inquirer.prompt(questions)[prompt]


def run_script(script):
    print('Running script: ', script)
    print()
    try:
        subprocess.call(script)
    except PermissionError:
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC)
        subprocess.call(script)


def main(base_dir):
    scripts_dict = make_scripts_dict(base_dir)
    # os.path.join won't work, because base_dir ends with '/' and dir starts with it
    directory = base_dir + choose_dir(scripts_dict, base_dir)
    scripts = scripts_dict[directory]
    script = os.path.join(directory, choose_script(scripts))
    run_script(script)


if __name__ == '__main__':
    print('Welcome to script runner!')
    print()
    if len(sys.argv) == 1:
        base_dir = os.getcwd()
    elif len(sys.argv) == 2:
        base_dir = os.path.abspath(sys.argv[1])
    else:
        print("You can provide 1 argument - base work directory, or non to use current working directory")
        exit(1)
    main(base_dir)
