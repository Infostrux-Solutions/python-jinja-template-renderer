import os
import sys
import argparse

from lib.config_loader import ConfigLoader
from lib.template_renderer import JinjaRenderer

def main(*args):

    print("------------------------------")
    print("Python environment:")
    print(" executable: ", sys.executable)
    print(" version: ", sys.version.replace("\n", ""))

    parser = argparse.ArgumentParser(prog='autodbt')
    parser.add_argument('-c','--config', help='The configuration file to load')
    parser.add_argument('-op','--output_path', help='The output path')
    parser.add_argument('-o','--output_name', help='The output filename')
    parser.add_argument('-cf','--custom_functions_file', help='The custom functions file')
    parser.add_argument('-tp','--template_path', help='The templates path')
    parser.add_argument('-tn','--template_name', help='The template name')
    args = parser.parse_args()

    # Parse the args
    # Priority is as follows:
    # Args >>> Environment Variable >>> Configuration File

    variables = {
        'config': None,
        'output_path': None,
        'output_name': None,
        'custom_functions_file': None,
        'template_path': None,
        'template_name': None,
    }

    arguments = {}
    for arg in vars(args):
        arguments[arg] = getattr(args, arg)

    for param in variables.keys():
        if param in arguments.keys():
            variables[param] = arguments[param]
        elif os.getenv(param.upper()):
            variables[param] = os.getenv(param.upper())

    print(" Configuration file: ", variables['config'])

    config = ConfigLoader(  configuration_file = variables['config'],
                            output_path             = variables['output_path'],
                            output_name             = variables['output_name'],
                            custom_functions_file   = variables['custom_functions_file'],
                            template_path         = variables['template_path'],
                            template_name          = variables['template_name'],
                        )
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
    template.write_output()

if __name__ == '__main__':
    main(*sys.argv[1:])