# -*- coding: utf-8 -*-
# type: ignore
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
"""Test Task-Runner."""

from typing import TYPE_CHECKING, Optional

from invoke import task

if TYPE_CHECKING:
    from invoke import Context


@task
def style(ctx, check=True):  # type: (Context, bool) -> None
    """Format project source code to PEP-8 standard."""
    args = ['--skip-string-normalization']
    if check:
        args.append('--check')
    ctx.run('isort --atomic **/*.py')
    ctx.run(f"black **/*.py {' '.join(args)}")


@task
def lint(ctx):  # type: (Context) -> None
    """Check project source code for linting errors."""
    ctx.run('flake8')


@task
def type_check(ctx, path='.'):  # type: (Context, str) -> None
    """Check project source types."""
    ctx.run(f"mypy {path}")


@task
def unit_test(ctx, capture=None):  # type: (Context, Optional[str]) -> None
    """Perform unit tests."""
    args = []
    if capture:
        args.append(f"--capture={capture}")
    ctx.run(f"pytest {' '.join(args)}")


@task
def static_analysis(ctx):  # type: (Context) -> None
    """Perform static code analysis on imports."""
    ctx.run('safety check')
    ctx.run('bandit -r proman_common')


@task
def coverage(ctx, report=None):  # type: (Context, Optional[str]) -> None
    """Perform coverage checks for tests."""
    args = ['--cov=proman_common']
    if report:
        args.append(f"--cov-report={report}")
    ctx.run(f"pytest {' '.join(args)} ./tests/")


@task(pre=[style, lint, unit_test, static_analysis, coverage])
def test(ctx):
    """Run all tests."""
    pass
