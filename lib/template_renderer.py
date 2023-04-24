from dataclasses import dataclass, field
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
import os, sys

@dataclass
class JinjaRenderer:

    """
    Base Jinja renderer. 
    """ 
    custom_variables:   Dict[str, Any]   = None
    custom_functions:   List[Any] = None
    templates_path:     str = None
    template_name:      str = None
    output_path:        str = None
    output_name:        str = None


    def load_template(self):
        loader = FileSystemLoader(searchpath = self.templates_path, encoding = 'utf-8')
        env = Environment(loader = loader, autoescape = True)
        self.template = env.get_template(self.template_name)

    def render_template(self):
        
        # Add all of the vars seen in the dictionary as debug
        # Make a copy
        if self.custom_variables is not None:
            custom_vars = self.custom_variables
            custom_vars['all_vars'] = dict(self.custom_variables)

        # Add the custom functions if present
        if self.custom_functions is not None:
            custom_funcs = {}
            for func in self.custom_functions:
                custom_funcs[func[0]] = func[1]
            self.template.globals.update(custom_funcs)

        self.output = self.template.render(custom_vars)

    def write_output(self):

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        full_filepath = os.path.join(self.output_path, self.output_name)
        
        with open(full_filepath, 'w') as f:
            f.write(self.output)   
        
    def return_output(self):
        return self.output