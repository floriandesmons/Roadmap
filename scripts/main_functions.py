# -*- coding: utf-8 -*-
"""
Version 1.0 (Report)

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons

Functions :
read_main(path: str)
- Reads main.txt and gets name of element's .txt file and class that should be used along with .txt file
and creates two lists of elements: one without extension that will be used for error_writer script;
and the second list is used to give data to schema_painter to draw an image of schema

create_class_instance(params_file, class_name)
- Based on name of element's .txt file and class that should be used along with .txt file, it creates an element of
Class named after .txt file and uses values inside it to initialize new Class of type from main.txt

main_reader_script()
- Main script that starts both function described above and shows result with values in console

split_float(number: float, sep: str = ".", number_of_digits: int = 6)
- Modifies float values, leaving only {number_of_digits} after the coma

get_default_parameters()
- Reads file default_parameters.txt to get initial values to start the simulation
"""

# Importing classes for elements
from exchanger import classExchanger
from pipeline import classPipes
from tank_central import classTankC
from tank_substation import classTankS

# Important data of the simulation
import values_storage

# Libraries to read files
import re
import os



# Dictionary to map class names to their corresponding class objects
known_classes = {
    "classPipes": classPipes,
    "classTankC": classTankC,
    "classExchanger": classExchanger,
    "classTankS": classTankS,
}

# Create results directory if it doesn't exist
if not os.path.exists(values_storage.results_path):
    os.makedirs(values_storage.results_path)


# Read and parse the main.txt file to get file names and class names
def read_main(path: str) -> dict[str, str]:
    file_and_class_data = {}

    # Read the contents of main.txt file
    with open(path, "r") as mf:
        raw_data = mf.read()

    # Split the raw data into lines
    lines = raw_data.split("\n")

    # Extract file names and corresponding class names from each line
    for line in lines:
        file_name, class_name = line.split()
        file_and_class_data[file_name] = class_name
        values_storage.elements_with_no_extension.append(''.join(re.sub(r'.txt$', '', file_name)))
        values_storage.elements.append(''.join(re.sub(r'_\d\.txt$', '', file_name)))  # Remove index from file name

    return file_and_class_data


# Create instances of classes mentioned in main.txt
def create_class_instance(params_file, class_name):
    params_list = []

    # Read parameters from file
    with open(params_file, "r") as pf:
        raw_data = pf.read()

    lines = raw_data.split('\n')

    # Extract parameter values
    for line in lines:
        _, param_value = line.split()
        params_list.append(float(param_value))

    try:
        # Create instance of the class using parameter values
        instance = known_classes[class_name](*params_list)
        return instance
    except Exception as e:
        print(f"Error creating class {class_name} with parameters {params_list}: {repr(e)}")


def main_reader_script():
    # Path to main.txt file
    main_file_path = values_storage.data_path + "main.txt"

    # Read main.txt and get file names and class names
    param_files_and_classes = read_main(main_file_path)

    # Create instances of classes mentioned in main.txt
    for params_file, class_name in param_files_and_classes.items():
        path = values_storage.data_path + params_file
        result = create_class_instance(path, class_name)
        values_storage.created_instances.append(result)

    # Print information about created instances
    for ci in values_storage.created_instances:
        print(f"Instance type: {type(ci)}\nInstance parameters: {vars(ci)}")


# Function to split float number and limit number of decimal digits
def split_float(number: float, sep: str = ".", number_of_digits: int = 6) -> float:
    before, after = str(number).split(sep)
    result = before + "." + after[:number_of_digits]
    return float(result)


# Function to get default parameters from default_parameters.txt file
def get_default_parameters():
    # Importing the CoolProp for calculation
    import CoolProp.CoolProp as CP

    with open(values_storage.data_path+'\default_parameters.txt') as dp:
        lines = dp.read().split('\n')
        for line in lines:
            temp1, temp2 = line.split()
            values_storage.parameters[temp1] = float(temp2)

        print("************* ",values_storage.parameters['T_in'])
        values_storage.parameters['T_in'] += 273.15 # From Celsius to Kelvin
        print("************* ",values_storage.parameters['T_in'])
        values_storage.parameters['p_in'] *= 1e5 # From Bar to Pascal

        values_storage.parameters['x_in'] = CP.PropsSI('Q', 'T', values_storage.parameters['T_in'], 'P',
                                                       values_storage.parameters['p_in'], 'R744')
        print('Default parameters:', values_storage.parameters)
