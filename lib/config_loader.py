from dataclasses import dataclass, field
from typing import List, Dict
from inspect import getmembers, isfunction

import os
import sys
import yaml
import lib.formatter as msg
import importlib.util

@dataclass
class ConfigLoader:
    
    """
    A config loading class. 
    Reads a yaml file as the input parameters to the program.
    """

    # Main vars
    configuration_file:     str = None
    output_path:            str = None
    output_name:            str = None
    custom_functions_file:  str = None
    custom_variables:       str = None
    template_path:          str = None
    template_name:          str = None

    # Determine if path supplied is relative or absolute
    # Returns the absolute path assuming that the path is relative to the config file
    def get_abs_path(self, config_path, path):
        print(os.path.abspath(path))
        return os.path.abspath(path)

    # Determine which variable takes priority
    # Currently var1 is the variable that returns the data
    # If both are empty error and exit
    def set_var(self, var1, var2, var_name):
        value = None
        if var1 is not None and var1.strip() != '':
            value = var1
        elif var2 is not None and var2.strip() != '':
            value = var2
        else:
            sys.exit(msg.error(f'No value specifed for {var_name}. Check your configuration files!'))

        print(msg.info(f'Found {var_name}. Loading...'))
        return value

    # Loads the configuration file
    def load(self):

        if self.configuration_file is None:
            sys.exit(msg.error('No configuration file specified.'))

        elif not os.path.isfile(self.configuration_file):
            sys.exit(msg.error(f'The configuration file "{self.configuration_file}" cannot be found. Check your paths and filenames.'))

        with open(self.configuration_file, 'r') as datastream:
            try:
                config = yaml.safe_load(datastream)
                
            except yaml.YAMLError as err:
                print(err)

        data_raw = config['config']

        # Construct override array
        vars = {}
        vars['output_path']           = self.output_path
        vars['output_name']           = self.output_name
        vars['custom_functions_file'] = self.custom_functions_file
        vars['template_path']         = self.template_path
        vars['template_name']         = self.template_name
                
        # If there are any passed in variables then it takes priority.
        # Else then the config value takes over
        configuration_headers = [   'output_path',
                                    'output_name',
                                    'custom_functions_file',
                                    'template_path',
                                    'template_name'
                                ]
        self.data = {}
        for header in configuration_headers:
            if header not in data_raw.keys():
                data_raw[header] = None

            self.data[header] = self.set_var(vars[header] , data_raw[header] , header)

            if header in ['output_path', 'custom_functions_file', 'template_path']:
                self.data[header] = os.path.abspath(self.data[header])

        # Load the custom functions and variables
        self.load_custom_functions()
        self.data['custom_variables'] = data_raw['custom_variables']

    # Attempts to load the functions in the custom function python file
    def load_custom_functions(self):

        try:
            module_name = 'custom_functions'
            spec = importlib.util.spec_from_file_location(module_name, self.data['custom_functions_file'])
            custom_functions = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = custom_functions
            spec.loader.exec_module(custom_functions)
      
            self.custom_functions = getmembers(custom_functions, isfunction)
            self.data['custom_functions'] = self.custom_functions
            print(self.custom_functions)

        except Exception as e:
            print(msg.error(e))