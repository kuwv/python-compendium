from invoke import call, task  # type: ignore


from compendium import __version__


if 'dev' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def format(ctx, check=False):
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run("black **/*.py {}".format(' '.join(args)))


@task
def lint(ctx):
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):
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
def version(ctx, part=part, tag=False, sign=False, confirm=False):
    args = [part]
    if tag:
        args.append('--tag')
        if sign:
            args.append('--sign-tags')
    if confirm:
        ctx.run("bumpversion {}".format(' '.join(args)))
    else:
        ctx.run(
            """bumpversion \
            --dry-run \
            --allow-dirty \
            --verbose \
            {}""".format(' '.join(args))
        )
        print('Add "--confirm" to actually bump the version.')


@task
def publish(ctx, symlink=False):
    ctx.run('flit publish')


@task
def clean(ctx):
    paths = ['dist', 'logs']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('compendium.egg-info')
    for path in paths:
        ctx.run("rm -rf {}".format(path))
