'''Test Task-Runner.'''
from invoke import call, task  # type: ignore


from compendium import __version__


if 'dev' in __version__ or 'rc' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def format(ctx, check=False):
    '''Format project source code to PEP-8 standard.

    :param check: bool, optional
        Check project source code without modification
    '''
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run("black **/*.py {}".format(' '.join(args)))


@task
def lint(ctx):
    '''Check project source code for linting errors.'''
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):
    '''Check project source types.

    :param path: str, optional
        Include the path to check for type-hints
    '''
    ctx.run("mypy {}".format(path))


@task
def unit_test(ctx, capture=None):
    '''Perform unit tests.'''
    args = []
    if capture:
        args.append('--capture=' + capture)
    ctx.run("pytest {}".format(' '.join(args)))


@task
def static_analysis(ctx):
    '''Perform static code analysis on imports.'''
    ctx.run('safety check')
    ctx.run('bandit -r compendium')


@task
def coverage(ctx, report=None):
    '''Perform coverage checks for tests.'''
    args = ['--cov=compendium']
    if report:
        args.append('--cov-report={}'.format(report))
    ctx.run("pytest {} ./tests/".format(' '.join(args)))


@task(pre=[format, lint, unit_test, static_analysis, coverage])
def test(ctx):
    '''Run all tests.'''
    pass


@task
def build(ctx, format=None):
    '''Build wheel package.'''
    if format:
        ctx.run("flit build --format={}".format(format))
    else:
        ctx.run('flit build')


@task(pre=[call(build, format='wheel')])
def dev(ctx):
    '''Perform development runtime environment setup.'''
    ctx.run('flit install --symlink --python python3')


@task
def install(ctx, symlink=True):
    '''Install in development environment.'''
    ctx.run('flit install -s')


@task
def version(ctx, part=part, tag=False, commit=False, message=None):
    '''Update project version and apply tags.

    :param tag: bool, optional
        Apply tag to branch using version

    :param commit: bool, optional
        Commit version to branch

    :param message: str, optional
        Add commit message with annotated tag
    '''
    args = [part]
    if tag:
        args.append('--tag')
    if commit:
        args.append('--commit')
    else:
        args.append('--dry-run')
        args.append('--allow-dirty')
        args.append('--verbose')
        print('Add "--commit" to actually bump the version.')
    if message:
        args.append("--tag-message '{}'".format(message))
    ctx.run("bumpversion {}".format(' '.join(args)))


@task
def publish(ctx):
    '''Publish project distribution.'''
    ctx.run('flit publish')


@task
def clean(ctx):
    '''Clean project dependencies and build.'''
    paths = ['dist', 'logs']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('compendium.egg-info')
    for path in paths:
        ctx.run("rm -rf {}".format(path))
