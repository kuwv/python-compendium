# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test Task-Runner.'''

from invoke import task  # type: ignore

from compendium.__version__ import __version__

if 'dev' in __version__ or 'rc' in __version__:
    part = 'build'
else:
    part = 'patch'


@task
def build(ctx, format=None):  # type: ignore
    '''Build wheel package.'''
    if format:
        ctx.run("flit build --format={}".format(format))
    else:
        ctx.run('flit build')


@task
def install(ctx, symlink=True, dev=False):  # type: ignore
    '''Install within environment.'''
    args = []
    if symlink:
        args.append('--symlink')
    if dev:
        args.append('--python=python3')
    ctx.run("flit install {}".format(' '.join(args)))


@task
def version(  # type: ignore
    ctx, part=part, tag=False, commit=False, message=None
):
    '''Update project version and apply tags.'''
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
def publish(ctx):  # type: ignore
    '''Publish project distribution.'''
    ctx.run('flit publish')


@task
def clean(ctx):  # type: ignore
    '''Clean project dependencies and build.'''
    paths = ['dist', 'logs', 'site']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('compendium.egg-info')
    for path in paths:
        ctx.run("rm -rf {}".format(path))
