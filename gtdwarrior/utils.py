import subprocess


TASK = "task"
PROMPT = "> "


def read_cmd(cmd, shell=True):
    return subprocess.check_output(cmd, shell=shell).decode('utf-8').rstrip()
