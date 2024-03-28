# Roadmap

Scripts developed by HES-SO Valais-Wallis as part of the HES-SO project in collaboration with HEPIA. 
Main objective: Model and simulate the behavior of a CO2 network.

## Information

This project is composed of different scripts: 
 - main_reader_v2.py: Main script reading the input parameters and creating data output of the simulation
 - main_functions.py: Function that are required to run the main_reader_v2.py
 - schema_painter.py: Script generating simplified image of the network simulated
 - values_storage.py: Database of import values used in multiple scripts 
 - exchanger.py, pipeline.py, tank_central.py, tank_substation.py: Scripts of each element 

## Remarks

The tank model used in the tank_central.py and tank_substation.py scripts is different from each other.
Changing the data_path and results_path variables inside the values_storage.py is required to run your test case. 