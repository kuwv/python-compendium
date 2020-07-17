'''Test environment variables.'''
import os

from compendium.settings import Settings


def test_environment(fs):
    '''Test environment variables.'''
    os.environ['TESTS_KEY'] = 'test' 
    env = Settings(application='tests')
    env.load_environment()
    assert env.get('/env/**/key') == 'test'
