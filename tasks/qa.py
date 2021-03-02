# type: ignore
# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Test Task-Runner.'''

from invoke import task  # type: ignore


@task
def style(ctx, check=True):  # type: ignore
    '''Format project source code to PEP-8 standard.'''
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run("black **/*.py {}".format(' '.join(args)))


@task
def lint(ctx):  # type: ignore
    '''Check project source code for linting errors.'''
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):  # type: ignore
    '''Check project source types.'''
    ctx.run("mypy {}".format(path))


@task
def unit_test(ctx, capture=None):  # type: ignore
    '''Perform unit tests.'''
    args = []
    if capture:
        args.append('--capture=' + capture)
    ctx.run("pytest {}".format(' '.join(args)))


@task
def static_analysis(ctx):  # type: ignore
    '''Perform static code analysis on imports.'''
    safety_args = []
    safety_ignore = [
        '39606',
        '39252',
        '38932',
    ]
    for x in safety_ignore:
        safety_args.append("--ignore={}".format(x))
    ctx.run("safety check {}".format(' '.join(safety_args)))
    ctx.run('bandit -r compendium')


@task
def coverage(ctx, report=None):  # type: ignore
    '''Perform coverage checks for tests.'''
    args = ['--cov=compendium']
    if report:
        args.append('--cov-report={}'.format(report))
    ctx.run("pytest {} ./tests/".format(' '.join(args)))


@task(pre=[style, lint, unit_test, static_analysis, coverage])
def test(ctx):  # type: ignore
    '''Run all tests.'''
    pass
