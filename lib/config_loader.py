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
    configuration_file:     str
    output:                 str = None
    custom_functions_file:  str = None
    custom_functions:       str = None
    custom_variables:       str = None

    # Loads the configuration file
    def load(self):

        if self.configuration_file is None:
            sys.exit(msg.error('No configuration file specified.'))


        elif not os.path.isfile(self.configuration_file):
            sys.exit(msg.error(f'The configuration file "{self.configuration_file}" cannot be found. Check your paths and filenames.'))

        with open (self.configuration_file, 'r') as datastream:
            try:
                config = yaml.safe_load(datastream)
                
            except yaml.YAMLError as err:
                print(err)

        data = config['config']

        if 'output' in data.keys():
            self.output = data['custom_variables'] 

        if 'custom_variables' in data.keys():
            print(msg.info('Found custom variables. Loading...'))
            self.custom_variables = data['custom_variables']
        
        if 'custom_functions' in data.keys():
            print(msg.info('Found custom functions. Loading...'))
            self.custom_functions_file = data['custom_functions']
            self.load_custom_functions()

    # Attempts to load the functions in the custom function python file
    def load_custom_functions(self):

        try:
            module_name = 'custom_functions'
            spec = importlib.util.spec_from_file_location(module_name, self.custom_functions_file)
            custom_functions = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = custom_functions
            spec.loader.exec_module(custom_functions)
      
            self.custom_functions = getmembers(custom_functions, isfunction)

        except Exception as e:
            print(msg.error(e))