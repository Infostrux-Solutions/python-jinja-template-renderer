# Template Generator
The template generator is a generation script that is designed to import user-created functions and variables and generate templates in Jinja with those functions in use. The codebase can be used standalone as a command-line script or as importable modules that can be imported into another program.

The template generator is especially useful for generating code, such as creating dbt SQL models from metadata, but it can also be used to generate text, semistructured data such as JSON, and code in any other language.
#
## Quick Demo
> **Note** - All of the demo files can be found in the test/templates folder.

Normally, when using Jinja templates, we would pass in some variables to be used in the template. In addition, if we wanted to use non-Jinja functions, you would need to add them to the scope of the template. This script intends to streamline this process by automatically importing the Python files with the functions and custom variables and making them available to the template.

We first start with the configuration file [config.yml](../test/config.yml):

```
config:
  output_path: './target/'
  output_name: 'sample.txt'
  custom_functions_file: ['./test/templates/main_functions.py', './test/templates/formatters.py']
  custom_variables:
    apple: 'Apples are red,'
    company: 'ACME Company'
    revision: 0.0.0.0.1
    score: 90
    target_env: {
      dev: development,
      qa: qa,
      stg: stage,
      prd: production
    }
  template_path: './test/templates/'
  template_name: 'test.txt'
```

This file specifies all of the project parameters for the job. In particular, we define custom variables for our run, and also include a list of files that contain our functions. We also specify the template file that will be used: [test.txt](../test/templates/test.txt):

```
Company Name: {{ company }}
Revision No.: {{ revision }}
Appended Add No.: {{ main_functions__addition(1, 1) }}
Case No.: {{ main_functions__division(45, 2) }}
Target Environment: {{ formatters__uppercase(target_env['dev']) }}

{{ main_functions__current_date() }}

Dear Some Random Person,

{{ formatters__uppercase(apple) }}

You wrote the following essay for the test:

{{ main_functions__hello_world() }}

After careful review, we have scored it out of 120 points. Your final percentage is shown below.

Your total score: {{ main_functions__calc_score(score) }}%

Sincerely,

Some_Random_Person
```
Note how for function calls, we follow the notation of
```
[file_name]__[function_name]
```
This allows functions with the same name in different files to co-exist with each other. Once the configuration is set up, we call the script via [main.py](./main.py):  and pass in the configuration file as an argument. The script will automatically import all of the custom variables and functions to produce the following output:

```
Company Name: ACME Company
Revision No.: 0.0.0.0.1
Appended Add No.: 2
Case No.: 22.5
Target Environment: development

2023-06-02

Dear Some Random Person,

Apples are red,

You wrote the following essay for the test:

Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
    officia deserunt mollit anim id est laborum.



After careful review, we have scored it out of 120 points. Your final percentage is shown below.

Your total score: 0.75%

Sincerely,

Some_Random_Person
```

#

## Initial setup

1. Create a virtual environment (Requires Python 3.8 or higher)
2. Run ```pip install -r requirements.txt```
3. Copy ```.env.sample``` to a new file called ```.env ```(you can comment out the variables you don't need)
4. Set variables in ```.env``` as required

## How to use

The command-line entry point script is  ```main.py```. You can find the input arguments by passing in the ```--help``` or `-h` argument, as such:

```
python main.py --help
python main.py -h
```

You can define arguments either as command-line arguments, set as environment variables, or in a configuration file. See the following section **"Passing Arguments"** for more information on how to pass the arguments.

> **NOTE**: You can always use normal Jinja functions in addition to the Python functions you have passed.

During execution, the script will read all arguments provided and do the following:

1. Scan the configuration file
2. Load all variables
3. Load the custom function file(s)
4. Load the custom variable(s)
5. Pass the information into the Jinja template renderer
6. Render the template with the provided information
7. Output the rendered file at the indicated target path

A sample configuration, template and custom functions files can be found in the `test/template` folder for reference.

> **NOTE**: Custom functions can use other built-in Python modules. However, custom module imports are not currently supported.

## Passing Arguments

There are **three ways** to pass arguments into the program. The following list describes each loading method.

> **NOTE**: The higher the loading method on the list the higher priority it will have.
1. Arguments are loaded from the `command-line`. You cannot pass in custom_variables using this method, and custom function files are limited to one file.
2. Arguments are loaded from the system `environment variables`, either through setting using the `.env` file or some other method
3. Arguments are loaded from the `configuration file` that was specified. This is the only place that allows for the definition of custom variables, and accepts a list of files for the custom functions.

The following charts describe each argument.

### Command-Line Arguments
The command-line arguments are passed into the program using the command-line flags at runtime. These variables have the highest precedence and will override same-name variables found as environment variables or configuration file variables. You can only specify a single file for the custom functions file via this method. Custom variables cannot be set using this method.

|  Argument  | Descripton  |
|------------|-------------|
| `-c <configuration_path>` <br /> `--config <configuration_path>`  | The path to the configuration file. Can be relative or absolute.  |
| `-op <output_path>` <br /> `--output_path <output_path>`  | The path to the folder where you want the output to be dumped. |
| `-o <output_name>` <br /> `--output_name <output_name>`  | The name of the output filename. |
| `-cf <custom_functions_file>` <br /> `--custom_functions_file <custom_functions_file>`  | The path to the custom functions file. You can only specify one file on the command line. |
| `-tp <template_path>` <br /> `--template_path <template_path>`  | The path to the folder of where the template resides |
| `-tn <template_name>` <br /> `--template_name <template_name>`  | The name of the template to be used for generation. |

### Environment Variables
The environment variables are system session variables that can be set manually or via the `.env.sample` sample file. The variables here have higher precedence than the ones in the configuration file, but can be overwritten by the command-line arguments. You can only specify a single file for the custom functions file.

|  Variable Name  | Descripton  |
|------------|-------------|
| `CONFIGURATION_FILE`  | The path to the configuration file. The path can be relative or absolute.  |
| `OUTPUT_PATH`  | The path to the folder where you want the output to be dumped. |
| `OUTPUT_LOCATION`  | The name of the output filename. |
| `CUSTOM_FUNCTIONS_FILE`  | The path to the custom functions file. The path can only specify one file. |
| `TEMPLATE_PATH`  | The path to the folder of where the template resides |
| `TEMPLATE_NAME`  | The name of the template to be used for generation. |

### Configuration File
The configuration file is a yaml file that contains the baseline arguments for the program. If environment variables or command-line arguments are passed in then those respective arguments will be overwritten.

To see a sample configuration file, see `config.yml` in the `test\templates` folder.

> **NOTE**: This is the only place where you can specify custom variables and provide a *list* of files containing custom functions.

|  Variable Name  | Descripton  |
|------------|-------------|
| `output_path`  | The path to the configuration file. The path can be relative or absolute.  |
| `output_name`  | The path to the folder where you want the output to be dumped. |
| `custom_functions_file`  |  The path to the custom functions file. You can either pass in a single filepath or a list of filepaths. |
| `custom_variables`  | A dictionary of custom variables that will be used within the template. Variables can be strings, numerics, lists and dictionaries.
| `template_path`  | The path to the folder where the template resides |
| `template_name`  | The name of the template to be used for generation. |
