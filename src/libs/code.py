import re
from multiprocessing import Process, Queue
from io import StringIO

disabled_functions = []
with open('disabled.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    disabled_functions = [line.strip('\n') for line in lines]


def render(variables, code):
    with open('template.py', 'r', encoding='utf-8') as f:
        source = f.read()
    codelines = code.split('\n')
    codelines = ["    " + line for line in codelines]
    code = '\n'.join(codelines)
    source = source.replace('#VARS#', variables).replace('#CODE#', code)
    return source


def save(code, name):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(code)


def read(name):
    with open(name, 'r', encoding='utf-8') as f:
        source = f.read()
    return source


def is_safe(code):
    for df in disabled_functions:
        check = re.findall(df, code, re.MULTILINE | re.IGNORECASE)
        if len(check) > 0:
            return False
    return True


def _exec(code):
    str = StringIO()
    str.write(code)
    str.seek(0)
    namespace = {}
    exec(str.read(), namespace)
    return namespace['run']()


def run(code):
    try:
        res = _exec(code)
        return True, res
    except Exception as inst:
        return False, inst.args[0]


def run_safe(code, timeout=2):
    try:
        def async_runner(queue, code):
            ret = _exec(code)
            queue.put(ret)

        result_queue = Queue()
        th = Process(target=async_runner, args=(result_queue, code,))
        th.start()
        th.join(timeout=timeout)
        if th.is_alive():
            th.terminate()
            raise Exception('execution timeout')
        
        return True, result_queue.get()
    except Exception as inst:
        return False, inst.args[0]
