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
    args = parser.parse_args()

    # Set the main config location
    configuration_file = None
    if os.getenv('CONFIGURATION_FILE'):
        configuration_file = os.getenv('CONFIGURATION_FILE')

    if args.config:
        configuration_file = args.config

    print(" configuration file: ", configuration_file)

    config = ConfigLoader(configuration_file = configuration_file)
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