from invoke import call, task  # type: ignore


from compendium import __version__


if 'dev' in __version__ or 'rc' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def format(ctx, check=False):
    '''Format project source code to PEP-8 standard

    Parameters
    ----------
    check: bool, optional
        Check project source code without modification
    '''
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run("black **/*.py {}".format(' '.join(args)))


@task
def lint(ctx):
    '''Check project source code for linting errors'''
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):
    '''Check project source types

    Parameters
    ----------
    path: str, optional
        Include the path to check for type-hints
    '''
    ctx.run("mypy {}".format(path))


@task
def unit_test(ctx, capture=None):
    args = []
    if capture:
        args.append('--capture=' + capture)
    ctx.run("pytest {}".format(' '.join(args)))


@task
def safety(ctx):
    ctx.run('safety check')


@task
def coverage(ctx, report=None):
    args = ['--cov=compendium']
    if report:
        args.append('--cov-report={}'.format(report))
    ctx.run("pytest {} ./tests/".format(' '.join(args)))


@task(pre=[format, lint, unit_test, safety, coverage])
def test(ctx):
    pass


@task
def build(ctx, format=None):
    if format:
        ctx.run("flit build --format={}".format(format))
    else:
        ctx.run('flit build')


@task(pre=[call(build, format='wheel')])
def dev(ctx):
    ctx.run('flit install --symlink --python python3')


@task
def install(ctx, symlink=True):
    ctx.run('flit install -s')


@task
def version(ctx, part=part, tag=False, commit=False, message=None):
    '''Update project version and apply tags

    Parameters
    ----------
    tag: bool, optional
        Apply tag to branch using version

    commit: bool, optional
        Commit version to branch

    message: str, optional
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
    '''Publish project distribution'''
    ctx.run('flit publish')


@task
def clean(ctx):
    '''Clean project dependencies and build'''
    paths = ['dist', 'logs']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('compendium.egg-info')
    for path in paths:
        ctx.run("rm -rf {}".format(path))
