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
def description(id):
    description = read_cmd("{t} _get {id}.description".format(
        t=TASK, id=id))
    print("Description (blank for '{description}'):"
          .format(description=description))
    return input(PROMPT)
def bucket(name):
    @unique_field
    def inner(id):
        return 'bucket:{name}'.format(name=name)
    return inner
@unique_field
def project(id):
    print("Project:")
    return "project:{project}".format(project=input(PROMPT))
@unique_field
def context(id):
    print("Context:")
    return "+{context}".format(context=input(PROMPT).upper())
def estimation(id):
    print("Priority, energy, duration:")
    yield from ["{name}:{val}".format(name=name, val=val)
                for name, val in zip(['priority', 'energy', 'duration'],
                                     input(PROMPT).split())]
@unique_field
def priority(id):
    print("Priority:")
    return "priority:{priority}".format(priority=input(PROMPT))
@unique_field
def aim(id):
    print("Aim:")
    return "aim:\'{aim}\'".format(aim=input(PROMPT))
def persons(id):
    print("Persons:")
    yield from ["+{person}".format(person=person)]
def tags(id):
    print("Tags:")
    yield from ["+{tag}".format(tag=tag) for tag in input(PROMPT).split()]
@unique_field
def delay(id):
    print('When should I tickle?')
    return "wait:{delay}".format(delay=input(PROMPT))


def duplicate(inbox_id):
    left_trim, right_trim = (13, 1)
    confirm = read_cmd([TASK, inbox_id, "duplicate", "rc.verbose=new-id"],
                       shell=False)
    return confirm[left_trim:-right_trim]


def modify(id, arguments):
    command = list(itertools.chain(
        [TASK, id, "modify"],
        *[action(id) for action in arguments]))
    subprocess.call(command)


def process(inbox_id, arguments):
    new_id = duplicate(inbox_id)
    modify(new_id, arguments)
    done(inbox_id, arguments)


def done(id, arguments):
    subprocess.call([TASK, id, "done"])


def remove(id, arguments):
    subprocess.call([TASK, id, "rm"])


OPERATIONS = {
    'N': {'command': process,
          'arguments': [description, bucket('Next'), project,
                        context, estimation, aim, tags]},
    'W': {'command': process,
          'arguments': [description, bucket('Waiting'), project,
                        aim, persons, priority, tags]},
    'S': {'command': process,
          'arguments': [description, bucket('Someday'), project,
                        context, tags]},
    'T': {'command': modify, 'arguments': [delay]},
    'D': {'command': done, 'arguments': []},
    'R': {'command': remove, 'arguments': []}}


def main():
    answer = ''
    while True:
        try:
            inbox = read_cmd("{t} in rc.verbose=nothing".format(t=TASK))
            inbox_id = inbox.split()[0]
            description = read_cmd("{t} _get {id}.description".format(
                t=TASK, id=inbox_id))

            print("Inbox ID: {id}".format(id=inbox_id))
            print("Description: {desc}".format(desc=description))
            while answer not in OPERATIONS.keys():
                print("Action:")
                print("\tNext(N), Someday/Maybe(S), WaitingFor(W)")
                print("\tDone(D), Remove(R), Tickle(T)")
                answer = input(PROMPT)

            operation = OPERATIONS[answer]
            command = operation['command']
            command(inbox_id, operation['arguments'])
        except Exception:
            print("Congratulations, your inbox is empty")
            return


def read_cmd(cmd, shell=True):
    return subprocess.check_output(cmd, shell=shell).decode('utf-8').rstrip()


if __name__ == '__main__':
    main()
