import subprocess
import itertools
from gtdwarrior.utils import read_cmd, TASK


def duplicate(inbox_id):
    left_trim, right_trim = (13, 1)
    confirm = read_cmd([TASK, inbox_id, "duplicate",
                        "rc.verbose=new-id",
                        "rc.confirmation=no"],
                       shell=False)
    return confirm[left_trim:-right_trim]


def modify(id, arguments):
    command = list(itertools.chain(
        [TASK, id, "modify",
         "rc.verbose=nothing",
         "rc.confirmation=no"],
        *[action(id) for action in arguments]))
    subprocess.call(command)


def done(id, arguments):
    subprocess.call([TASK, id, "done",
                     "rc.verbose=nothing",
                     "rc.confirmation=no"])


def remove(id, arguments):
    subprocess.call([TASK, id, "rm",
                     "rc.verbose=nothing",
                     "rc.confirmation=no"])


def process(inbox_id, arguments):
    new_id = duplicate(inbox_id)
    modify(new_id, arguments)
    done(inbox_id, arguments)
