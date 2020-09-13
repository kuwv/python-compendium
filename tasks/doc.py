# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide documentation tasks.'''

from invoke import task


@task
def lint(ctx):
    '''Check code for documentation errors.'''
    ctx.run('pydocstyle')


@task
def coverage(ctx):
    '''Ensure all code is documented.'''
    ctx.run('docstr-coverage **/*.py')


@task(pre=[lint], post=[coverage])
def test(ctx):
    '''Test documentation build.'''
    ctx.run('mkdocs build')


@task
def build(ctx):
    '''Build documentation site.'''
    ctx.run('mkdocs build')


@task
def publish(ctx):
    '''Publish project documentation.'''
    ctx.run('mkdocs gh-deploy')
