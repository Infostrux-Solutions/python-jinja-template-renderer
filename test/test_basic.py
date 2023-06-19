# A list of configuration loader tests
from lib.config_loader import ConfigLoader
from lib.template_renderer import JinjaRenderer
import pytest

def test_coalesce():

    none         = None
    empty_string = ''
    empty_spaces = '      '
    string_data  = '   0   '

    empty_list   = []
    list_data    = ['sample']

    config = ConfigLoader()

    # Test 1, first variable is set
    assert(config.coalesce(string_data, none, 'Test') == string_data)
    assert(config.coalesce(string_data, empty_string, 'Test') == string_data)
    assert(config.coalesce(string_data, empty_spaces, 'Test') == string_data)
    assert(config.coalesce(list_data, empty_list, 'Test') == list_data)

    # Test 2, second variable is set
    assert(config.coalesce(none, string_data, 'Test') == string_data)
    assert(config.coalesce(empty_string, string_data, 'Test') == string_data)
    assert(config.coalesce(empty_spaces, string_data, 'Test') == string_data)
    assert(config.coalesce(empty_list, list_data, 'Test') == list_data)

# Test no config
def test_empty_load():
    with pytest.raises(SystemExit) as e:
        config = ConfigLoader(configuration_file = None)
        config.load()
    assert e.type == SystemExit
    assert 'No configuration file specified.' in e.value.code

# Test missing config
def test_missing_config():
    with pytest.raises(SystemExit) as e:
        config = ConfigLoader(configuration_file = 'nothing')
        config.load()
    assert e.type == SystemExit
    assert 'The configuration file "nothing" cannot be found. Check your paths and filenames.' in e.value.code

# Test normal load
def test_load():
    config = ConfigLoader(configuration_file = 'test/templates/config.yml')
    config.load()
    assert 'template_path' in config.data
    assert 'template_name' in config.data
    assert 'output_path' in config.data
    assert 'output_name' in config.data
    assert 'custom_functions' in config.data
    assert 'custom_variables' in config.data

    # Check custom variable contents
    assert ('apple', 'Apples are red,') in config.data['custom_variables'].items()
    assert ('company', 'ACME Company') in config.data['custom_variables'].items()
    assert ('revision', '0.0.0.0.1') in config.data['custom_variables'].items()
    assert ('score', 90) in config.data['custom_variables'].items()

    assert ('target_env') in config.data['custom_variables'].keys()
    assert ('dev', 'development') in config.data['custom_variables']['target_env'].items()
    assert ('qa', 'qa') in config.data['custom_variables']['target_env'].items()
    assert ('stg', 'stage') in config.data['custom_variables']['target_env'].items()
    assert ('prd', 'production') in config.data['custom_variables']['target_env'].items()

def test_output():
    config = ConfigLoader(configuration_file = 'test/templates/config.yml')
    config.load()
    template = JinjaRenderer(   templates_path = config.data['template_path'],
                                template_name = config.data['template_name'],
                                output_path = config.data['output_path'],
                                output_name = config.data['output_name'],
                                custom_functions = config.data['custom_functions'],
                                custom_variables = config.data['custom_variables']
                            )
    template.load_template()
    template.render_template()
    test_data = template.return_output()
    ref = ''
    with open('test/templates/sample.txt') as f:
        ref = f.read()

    assert(test_data == ref.rstrip())
