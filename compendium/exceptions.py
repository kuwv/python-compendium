# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Provide exceptions for Compendium.'''


class CompendiumException(Exception):
    '''Provide base errors in Compendium.'''


class CompendiumConfigManagerError(CompendiumException):
    '''Provide exceptions for ConfigManager errors.'''


class CompendiumSettingsError(CompendiumException):
    '''Provide exceptions for Settings errors.'''
