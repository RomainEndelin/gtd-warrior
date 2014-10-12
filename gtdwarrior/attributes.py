from gtdwarrior.utils import PROMPT, read_cmd


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
