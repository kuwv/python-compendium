import os
import pytest

from compendium.cache import NestedSettingsCache


@pytest.mark.parametrize('fs', [[['pkgutil']]], indirect=True)
def test_nested(fs):
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Nested paths
    fs.add_real_file(
        source_path=base_path + '/fruit.toml',
        target_path='/opt/test/fruit.toml'
    )
    fs.add_real_file(
        source_path=base_path + '/fruit1.toml',
        target_path='/opt/test/example1/fruit.toml'
    )
    fs.add_real_file(
        source_path=base_path + '/fruit2.toml',
        target_path='/opt/test/example2/fruit.toml'
    )

    cfg = NestedSettingsCache(
        application='test',
        filename='fruit.toml',
        merge_strategy='partition'
    )
    cfg.load('/opt/test/fruit.toml')

    assert ('/opt/test/fruit.toml') in cfg.filepaths
    assert ('/opt/test/example1/fruit.toml') in cfg.filepaths
    assert ('/opt/test/example2/fruit.toml') in cfg.filepaths
    assert cfg.get('/settings/[0]/filepath') == '/opt/test/fruit.toml'
    assert cfg.get('/settings/[1]/filepath') == '/opt/test/example1/fruit.toml'
    assert cfg.get('/settings/[2]/filepath') == '/opt/test/example2/fruit.toml'

    print(cfg.get('/settings/**/fruit/drupe'))
    print(cfg.get('/**/name', cfg.get('/settings/**/fruit/drupe')))
    assert cfg.get('/**/name', cfg.get('/settings/**/fruit/drupe')) == 'peach'

    # Ensure vegatable is not in fruits
    # NOTE: Added defaults
    # with pytest.raises(KeyError):
    #     cfg.get('/settings/**/vegetable')
