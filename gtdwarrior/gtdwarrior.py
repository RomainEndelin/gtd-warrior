#!/usr/bin/env python

import sys
import subprocess
import itertools


TASK = "task"
PROMPT = "> "

def unique_field(func):
    def inner(*args, **kwargs):
        return [func(*args, **kwargs)]
    return inner

@unique_field
def description():
    print("Description:")
    return input(PROMPT)
def bucket(name):
    @unique_field
    def inner():
        return 'bucket:{name}'.format(name=name)
    return inner
@unique_field
def project():
    print("Project:")
    return "project:{project}".format(project=input(PROMPT))
@unique_field
def context():
    print("Context:")
    return "+{context}".format(context=input(PROMPT).upper())
def estimation():
    print("Priority, energy, duration:")
    yield from ["{name}:{val}".format(name=name, val=val)
                for name, val in zip(['priority', 'energy', 'duration'],
                                     input(PROMPT).split())]
@unique_field
def priority():
    print("Priority:")
    return "priority:{priority}".format(priority=input(PROMPT))
@unique_field
def aim():
    print("Aim:")
    return "aim:\'{aim}\'".format(aim=input(PROMPT))
def tags():
    print("Persons:")
    yield from ["+{person}".format(person=person)
                for person in input(PROMPT).split()]
def persons():
    print("Tags:")
    yield from ["+{tag}".format(tag=tag) for tag in input(PROMPT).split()]



ACTIONS = {'N': [description, bucket('Next'), project,
                 context, estimation, aim, tags],
           'W': [description, bucket('Waiting'), project,
                 aim, persons, priority, tags],
           'S': [description, bucket('Someday'), project,
                 context, tags],
           'T': None,
           'D': None,
           'R': None}


def main():
    command = ''
    if len(sys.argv) > 0:
        inbox_id = sys.argv[1]
        description = read_cmd("{t} _get {id}.description".format(
            t=TASK, id=inbox_id))

        print("Inbox ID: {id}".format(id=inbox_id))
        print("Description: {desc}".format(desc=description))
        while command not in ACTIONS.keys():
            print("Action:")
            print("\tNext(N), Someday/Maybe(S), WaitingFor(W)")
            print("\tDone(D), Remove(R), Tickle(T)")
            command = input(PROMPT)

        new_id = duplicate(inbox_id)
        command = list(itertools.chain([TASK, new_id, "modify"],
                                       *[action()
                                         for action in ACTIONS[command]]))
        subprocess.call(command)
        subprocess.call([TASK, inbox_id, "done"])
        # if action == 'N':
        #     add_to_next(inbox_id, description)
        # elif action == 'S':
        #     pass
        # elif action == 'W':
        #     pass
        # elif action == 'T':
        #     pass
        # elif action == 'D':
        #     subprocess.call([TASK, inbox_id, "done"])
        # elif action == 'R':
        #     subprocess.call([TASK, inbox_id, "rm"])
    else:
        print("Please provide the Inbox ID")


def add_to_next(inbox_id, description):
    print('Description (blank for "{desc}"):'.format(desc=description))
    new_description = input(PROMPT)
    if not new_description:
        new_description = description

    print("Project:")
    project = input(PROMPT)

    print("Context:")
    context = input(PROMPT)

    print("Priority, energy, duration:")
    priority, energy, duration = input(PROMPT).split()

    print("Aim:")
    aim = input(PROMPT)

    print("Tags")
    tags = input(PROMPT).split()

    new_id = duplicate(inbox_id)
    command = [TASK, new_id, "modify",
               new_description,
               "bucket:Next",
               "project:{project}".format(project=project),
               "+{context}".format(context=context.upper()),
               "priority:{pri}".format(pri=priority),
               "energy:{ene}".format(ene=energy),
               "duration:{dur}".format(dur=duration),
               "aim:\\'{aim}\\'".format(aim=aim)]
    command += ["+{tag}".format(tag=tag) for tag in tags]
    subprocess.call(command)
    subprocess.call([TASK, inbox_id, "done"])


def duplicate(inbox_id):
    left_trim, right_trim = (13, 1)
    confirm = read_cmd([TASK, inbox_id, "duplicate", "rc.verbose=new-id"],
                       shell=False)
    return confirm[left_trim:-right_trim]


def read_cmd(cmd, shell=True):
    return subprocess.check_output(cmd, shell=shell).decode('utf-8').rstrip()


if __name__ == '__main__':
    main()
