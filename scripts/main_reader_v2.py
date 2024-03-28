# -*- coding: utf-8 -*-
"""
Version 1.0 (Report)

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons
"""

# Import datetime to compute the simulation time
from datetime import datetime
# Importing classes for elements
from tank_central import classTankC
from tank_substation import classTankS
# Importing the main function from schema_painter module
from schema_painter import draw_schema

# Important data of the simulation
import values_storage
import main_functions

# Library for graphics outputs
import plotly.graph_objects as go

# Get the launching time
start_time = datetime.now()

# Number of time step
nb_steps = 50

# Execute main function if the script is run directly
if __name__ == "__main__":
    main_functions.main_reader_script()


    main_functions.get_default_parameters()
    for step in range(nb_steps):
        print('#' * 50)
        # Update parameters using data from created_instances
        for element in range(len(values_storage.elements)):
            values_storage.parameters['m_dot_in'], values_storage.parameters['p_in'], values_storage.parameters['T_in'], values_storage.parameters['x_in'] = \
                values_storage.created_instances[element].update(main_functions.split_float(values_storage.parameters['m_dot_in']),
                                                                 main_functions.split_float(values_storage.parameters['p_in']),
                                                                 main_functions.split_float(values_storage.parameters['T_in']),
                                                                 values_storage.parameters['x_in'])

            # Print updated parameters
            print(
                f'Step: {step + 1} Element: {values_storage.elements_with_no_extension[element]} | Output result:',
                (main_functions.split_float(values_storage.parameters['m_dot_in'])), main_functions.split_float(values_storage.parameters['p_in']),
                main_functions.split_float(values_storage.parameters['T_in']),
                values_storage.parameters['x_in'])

        pressure_tank_substation = 0
        for element in range(len(values_storage.created_instances)):
            if isinstance(values_storage.created_instances[element], classTankS):
                pressure_tank_substation = values_storage.created_instances[element].p

        for element in range(len(values_storage.created_instances)):
            # Pressure for central tank and substation tank
            if isinstance(values_storage.created_instances[element], classTankC):
                values_storage.created_instances[element].set_delta_pressure(pressure_tank_substation)


print('#' * 50)
print('Time required for simulation: ', datetime.now() - start_time)


# Call the main function of schema_painter module with the list of elements
draw_schema(values_storage.elements)

fig = go.Figure()
# Exemple of drawing graphics
fig.add_trace(go.Scatter(y=values_storage.T_tank1, mode='lines', name='T_c'))
fig.add_trace(go.Scatter(y=values_storage.T_tank2, mode='lines', name='T_s'))
fig.add_trace(go.Scatter(y=values_storage.m_dot_tank_c, mode='lines', name='m_c'))
fig.add_trace(go.Scatter(y=values_storage.p_tank_c, mode='lines', name='p_c'))
fig.add_trace(go.Scatter(y=values_storage.x_tank_c, mode='lines', name='x_c'))
fig.add_trace(go.Scatter(y=values_storage.m_dot_tank_s, mode='lines', name='m_s'))
fig.add_trace(go.Scatter(y=values_storage.p_tank_s, mode='lines', name='p_s'))
fig.add_trace(go.Scatter(y=values_storage.x_tank_s, mode='lines', name='x_s'))

fig.add_trace(go.Scatter(y=values_storage.m_dot_pipe1, mode='lines', name='m_dot_pipe1'))
fig.add_trace(go.Scatter(y=values_storage.p_pipe1, mode='lines', name='p_pipe1'))
fig.add_trace(go.Scatter(y=values_storage.T_pipe1, mode='lines', name='T_pipe1'))
fig.add_trace(go.Scatter(y=values_storage.x_pipe1, mode='lines', name='x_pipe1'))

fig.add_trace(go.Scatter(y=values_storage.m_dot_pipe2, mode='lines', name='m_dot_pipe2'))
fig.add_trace(go.Scatter(y=values_storage.p_pipe2, mode='lines', name='p_pipe2'))
fig.add_trace(go.Scatter(y=values_storage.T_pipe2, mode='lines', name='T_pipe2'))
fig.add_trace(go.Scatter(y=values_storage.x_pipe2, mode='lines', name='x_pipe2'))

fig.update_layout(xaxis_title='Step №',
                  yaxis_title='Value')

fig.show()
