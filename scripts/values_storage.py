"""
Version 1.0

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons
"""

data_path ="../Tests/Tank/"
results_path = "../Tests/Tank/results"

# List of most of the elements/instances inside the simulation
created_instances = [] # Used in : main_reader_v2.py, main_functions.py, tank_central.py
elements = [] # Used in : main_reader_v2.py
elements_with_no_extension = [] # Used in : main_reader_v2.py, main_functions.py

# Simulation values of m_dot, p, T and x. Changing each simulation step
parameters = {} # Used in : main_reader_v2.py, main_functions.py

# Graphics parameters
m_dot_pipe1 = []
m_dot_pipe2 = []
m_dot_tank_c = []
m_dot_tank_s = []
p_pipe1 = []
p_pipe2 = []
p_tank_c = []
p_tank_s = []
T_pipe1 = []
T_pipe2 = []
T_tank1 = []
T_tank2 = []
x_pipe1 = []
x_pipe2 = []
x_tank_c = []
x_tank_s = []
