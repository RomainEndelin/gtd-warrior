#!/usr/bin/env python

from gtdwarrior import commands as c
from gtdwarrior import attributes as a
from gtdwarrior.utils import PROMPT, TASK, read_cmd


OPERATIONS = {
    'N': {'command': c.process,
          'arguments': [a.description, a.bucket('Next'), a.project,
                        a.context, a.estimation, a.aim, a.tags]},
    'W': {'command': c.process,
          'arguments': [a.description, a.bucket('Waiting'), a.project,
                        a.aim, a.persons, a.priority, a.tags]},
    'S': {'command': c.process,
          'arguments': [a.description, a.bucket('Someday'), a.project,
                        a.context, a.tags]},
    'T': {'command': c.modify, 'arguments': [a.delay]},
    'D': {'command': c.done, 'arguments': []},
    'R': {'command': c.remove, 'arguments': []}}


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
                print("\tDone(D), Remove(R), Tickle(T), Exit(Q)")
                answer = input(PROMPT)

                if answer == 'Q':
                    return

            operation = OPERATIONS[answer]
            command = operation['command']
            command(inbox_id, operation['arguments'])
        except Exception:
            print("Congratulations, your inbox is empty")
            return


if __name__ == '__main__':
    main()
