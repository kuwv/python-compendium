# import os
from invoke import call, task


@task
def format(ctx):
    ctx.run('black -S **/*.py')


@task
def lint(ctx):
    ctx.run('flake8')


@task
def coverage(ctx):
    ctx.run('pytest --cov=compendium ./tests/')


@task
def unit_test(ctx):
    ctx.run('pytest')


@task(pre=[format, lint, unit_test, coverage])
def test(ctx):
    ctx.run('compend')


@task
def build(ctx, format=None):
    if format is not None:
        ctx.run("flit build --format={f}".format(f=format))
    else:
        ctx.run('flit build')


@task(pre=[call(build, format='wheel')])
def dev(ctx):
    ctx.run('flit install --symlink --python python3')


@task
def install(ctx, symlink=True):
    ctx.run('flit install -s')


@task
def version(ctx, part, confirm=False):
    if confirm:
        ctx.run("bumpversion {}".format(part))
    else:
        ctx.run(
            """bumpversion \
            --dry-run \
            --allow-dirty \
            --verbose \
            {}""".format(part)
        )
        print('Add "confirm" to actually bump the version.')


@task
def publish(ctx, symlink=False):
    ctx.run('flit publish')


@task
def clean(ctx):
    patterns = ['dist', 'logs']
    patterns.append('**/__pycache__')
    patterns.append('**/*.pyc')
    patterns.append('compendium.egg-info')
    for pattern in patterns:
        ctx.run("rm -rf {}".format(pattern))
