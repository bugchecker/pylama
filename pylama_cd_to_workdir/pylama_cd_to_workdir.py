"""Pylama's shell support."""

from __future__ import absolute_import, with_statement

from copy import deepcopy
from os import chdir, path as op
import sys

from . import main
from .main import process_paths, parse_options, setup_logger, LOGGER
from pylint.config import find_pylintrc

# TODO: support dirs


def shell(args=None, error=True):
    args = sys.argv[1:]
    options = parse_options(args)
    setup_logger(options)
    LOGGER.info(options)

    dirnames = {}
    for path in options.paths:
        dirname, basename = op.split(path)
        if dirname in dirnames:
            dirnames[dirname].add(basename)
        else:
            dirnames[dirname] = {basename}
    ORIG_CURDIR = main.CURDIR
    orig_linter_params = deepcopy(options.linters_params)
    errors = []
    for dirname, files in dirnames.items():
        main.CURDIR = op.abspath(dirname)
        chdir(main.CURDIR)
        options.linters_params = deepcopy(orig_linter_params)
        if 'pylint' not in options.linters_params:
            options.linters_params['pylint'] = {}
        options.linters_params['pylint']['rcfile'] = find_pylintrc()
        options.paths = files
        errors += process_paths(options, error=error)
    main.CURDIR = ORIG_CURDIR
    chdir(main.CURDIR)
    return errors


if __name__ == '__main__':
    shell()

# pylama:ignore=F0001
