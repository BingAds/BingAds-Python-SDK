import os
from subprocess import call

dependent_graph = {}
tasks = {}


def dependent_on(*dependent_funcs):
    """ Describe the dependencies of a specific functions.

    :param dependent_funcs: dependent functions
    :return: decorated function
    """

    def dependencies_wrapper(func):
        dependent_graph[func.__name__] = [dependent_func.__name__ for dependent_func in dependent_funcs]
        return func

    return dependencies_wrapper


def task(description=None):
    """ Describe the function be decorated by this task function.

    :param description: the description of decorated function
    :return: decorated function
    """

    if description is None:
        description = ''

    def task_wrapper(func):
        tasks[func.__name__] = description
        return func

    return task_wrapper


def delete_file(file_path):
    """ Delete file specified by path.

    :param file_path: the file path
    :type file_path: str
    :return: None
    """

    try:
        os.remove(file_path)
    except OSError:
        pass


def delete_folder(folder_path):
    """ Delete folder specified by path and all the files under it recursively.

    :param folder_path: the folder path
    :type folder_path: the folder path
    :return: None
    """

    import shutil

    shutil.rmtree(folder_path, ignore_errors=True)


def run_cmd(command):
    """ Run os command.

    :param command: the concrete content of command
    :type command: str
    :return: None
    """

    print(command)
    call(command, shell=True)


def make_execution_plan(func_name):
    """ Make the execution plan for a specific function, consider the dependencies.

    After analyze the dependency graph, use topological sort to give a proper execution order

    :param func_name: the function name to be executed
    :type func_name: str
    :return: the iterable function names, by execution order
    :rtype: iter(str)
    """

    in_degree = {}
    next_tasks = {}

    remaining = [func_name]
    while len(remaining) != 0:
        current = remaining.pop()
        if current not in dependent_graph:
            if current not in in_degree:
                in_degree[current] = 0
            if current not in next_tasks:
                next_tasks[current] = []
            continue
        if current not in in_degree:
            in_degree[current] = 0
        in_degree[current] += len(dependent_graph[current])
        if current not in next_tasks:
            next_tasks[current] = []
        for dependent_func in dependent_graph[current]:
            if dependent_func not in in_degree:
                in_degree[dependent_func] = 0
            if dependent_func not in next_tasks:
                next_tasks[dependent_func] = []
            next_tasks[dependent_func].append(current)
    while len(in_degree) != 0:
        for t in in_degree.keys():
            # can be optimized here, use linear search for easy to implemented and no performance concern currently
            if in_degree[t] == 0:
                t_selected = t
                break
        for t_next in next_tasks[t_selected]:
            in_degree[t_next] -= 1
        in_degree.pop(t_selected)
        next_tasks.pop(t_selected)
        yield t_selected


##########################
# Define Tasks From Here #
##########################


@task('clean the temporary output file')
def clean():
    delete_folder('.tox')
    delete_folder('bingads.egg-info')
    delete_folder('docs/_build')
    delete_folder('dist')
    delete_file('.coverage')


@task('code style check by flake8')
def lint():
    run_cmd('flake8 bingads tests')


@task('run all tests under current interpreter, and print coverage report')
def test():
    run_cmd('coverage run --source bingads -m py.test -v --strict')
    run_cmd('coverage report')


@task('run all unit tests under current interpreter, and print coverage report')
def ut():
    run_cmd('coverage run --source bingads -m py.test -k "not functional" -v --strict')
    run_cmd('coverage report')
	
@task('run all functional tests under current interpreter.')
def ft():
    run_cmd('py.test -k "functional" -v --strict')

@task('run all v13 unit tests under current interpreter, and print coverage report')
def v13_ut():
    run_cmd('coverage run --source bingads -m py.test v13tests/ -k "not functional" -v --strict')
    run_cmd('coverage report')
	
@task('run all v13 functional tests under current interpreter.')
def v13_ft():
    run_cmd('py.test v13tests/ -k "functional" -v --strict')

@task('run tests on all supported interpreters (check tox.ini)')
@dependent_on(clean)
def test_all():
    run_cmd('tox')


@task('generate static html documents, by sphinx, under docs/_build/html')
@dependent_on(clean)
def docs():
    run_cmd('sphinx-apidoc -F -o docs bingads')  # generate API rst file, may need to check-in
    run_cmd('sphinx-build -b html docs docs/_build/html')  # generate html file


@task('make compressed installation package')
@dependent_on(clean)
def dist():
    run_cmd('python setup.py sdist --formats=gztar,zip')


if __name__ == '__main__':
    from sys import argv, exit, modules

    if len(argv) == 1:
        if len(tasks) == 0:
            print('No task defined yet.')
            exit(0)
        max_length = 0
        for key in tasks.keys():
            if len(key) > max_length:
                max_length = len(key)
        format_str = '{0:<' + str(max_length) + '}  --  {1}'
        for key in tasks.keys():
            print(format_str.format(key, tasks[key]))
    elif len(argv) > 2:
        print('Only support one task at a time')
        exit(-1)
    else:
        task_name = argv[1]
        if task_name not in tasks:
            print(str.format("Task: '{0}' not defined", task_name))
            exit(-1)
        task_names = make_execution_plan(task_name)
        for task_name in task_names:
            task = getattr(modules[__name__], task_name)
            task()
