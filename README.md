# Template Generator
The template generator is a generation script that is designed to import user-created functions and variables and generate templates in Jinja with those functions in use. The code base can be used standalone as a command-line script, or as importable modules that can be imported into another program.

## Initial setup

1. Create a virtual environment (Requires Python 3.8 or higher)
2. Run ```pip install -r requirements.txt```
3. Copy ```.env.sample``` to a new file called ```.env ```(you can comment out the variables you don't need)
4. Set variables in ```.env``` as required

## How to use

The command-line entrypoint script is  ```main.py``` . You can find the input arguments by passing in the ```--help``` or `-h` argument, as such:

```
python main.py --help
python main.py -h
```

You can define arguments either as command-line arguments, set as environment variables, or in a configuration file. See the following section **"Passing Arguments"** for more information on how to pass the arguments.

During execution, the script will read all arguments provided and do the following:

1. Scan the configuration file
2. Load all variables
3. Load the custom function file(s)
4. Load the custom variable(s)
5. Pass the information into the Jinja template renderer
6. Render the template with the provided information
7. Output the rendered file at the indicated target path

A sample configuration, template and custom functions files can be found in the `test/template` folder for reference.

> **NOTE**: Custom functions can use other built-in python modules. However, custom module imports are not currently supported.

## Passing Arguments

There are **three ways** to pass arguments into the program. The following list describes each loading method.

> **NOTE**: The higher the loading method on the list the higher priority it will have.
1. Arguments are loaded from the `command-line`. You cannot pass in custom_variables using this method, and custom function files are limited to one file.
2. Arguments are loaded from the system `environment variables`, either through setting using the `.env` file or some other method
3. Arguments are loaded from the `configuration file` that was specified. This is the only place that allows for the definition of custom variables, and accepts a list of files for the custom functions.

The following charts describes each argument.

### Command-Line Arguments
The command-line arguments are passed into the program using the command-line flags at runtime. These variables have the highest precendence and will override same-name varaibles found as environment variables or configuration file variables. You can only specify a single file for the custom functions file via this method. Custom variables cannot be set using this method.

|  Argument  | Descripton  |
|------------|-------------|
| `-c <configuration_path>` <br /> `--config <configuration_path>`  | The path to the configuration file. Can be relative or absolute.  |
| `-op <output_path>` <br /> `--output_path <output_path>`  | The path to the folder where you want the output to be dumped. |
| `-o <output_name>` <br /> `--output_name <output_name>`  | The name of the output filename. |
| `-cf <custom_functions_file>` <br /> `--custom_functions_file <custom_functions_file>`  | The path to the custom functions file. Can only specify one file on command-line. |
| `-tp <template_path>` <br /> `--template_path <template_path>`  | The path to the folder of where the template resides |
| `-tn <template_name>` <br /> `--template_name <template_name>`  | The name of the template to be used for generation. |

### Environment Variables
The environment variables are system session variables at can be set manually or via the `.env.sample` sample file. The variables here have higher precedence than the ones in the condiguration file, but can be overwritten by the command-line arguments. You can only specify a single file for the custom functions file.

|  Variable Name  | Descripton  |
|------------|-------------|
| `CONFIGURATION_FILE`  | The path to the configuration file. Can be relative or absolute.  |
| `OUTPUT_PATH`  | The path to the folder where you want the output to be dumped. |
| `OUTPUT_LOCATION`  | The name of the output filename. |
| `CUSTOM_FUNCTIONS_FILE`  | The path to the custom functions file. Can only specify one file. |
| `TEMPLATE_PATH`  | The path to the folder of where the template resides |
| `TEMPLATE_NAME`  | The name of the template to be used for generation. |

### Configuration File
The configuration file is a yaml file that contains the baseline arguments for the program. If environment variables or command-line arguments are passed in then those respective arguments will be overwritten.

To see a sample configuration file, see `config.yml` in the `test\templates` folder.

> **NOTE**: This is the only place where you can specify custom variables and provide a *list* of files containing custom functions.

|  Variable Name  | Descripton  |
|------------|-------------|
| `output_path`  | The path to the configuration file. Can be relative or absolute.  |
| `output_name`  | The path to the folder where you want the output to be dumped. |
| `custom_functions_file`  |  The path to the custom functions file. You can either pass in a single filepath or a list of filepaths. |
| `custom_variables`  | A dictionary of custom variables that will be used within the template. Variables can be strings, numerics, lists and dictionaries.
| `template_path`  | The path to the folder of where the template resides |
| `template_name`  | The name of the template to be used for generation. |
