# -*- coding: utf-8 -*-
"""
Version 1.0 (Report)

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons

Classes :
-classPipes

Functions :
__init__()
- Initialization of the exchanger parameters

compute_output_evap()
- Calculate the output temperate for the evaporation

compute_output_cond()
- Calculate the output temperate for the condensation

setQdot()
- Function to modify the Qdot of each exchanger at each timestep

update()
- update function using new parameters
"""

import CoolProp.CoolProp as CP


class classExchanger:

    Qdot = 0

    def __init__(self, Qdot):

       self.Qdot = Qdot

    # Method that is used when we have liquid that need to be evaporated
    def compute_output_evap(self, m_dot_in, p_in, T_in, x_in):

        T_out = T_in

        if m_dot_in > 0:

            # Add 100 Pa to be sure that we are not in the saturation pressure
            H_in = CP.PropsSI('H', 'T', T_in, 'P', p_in+100, 'R744')

            H = self.Qdot / m_dot_in + H_in

            T_out = CP.PropsSI('T', 'H', H, 'P', p_in, 'R744')

        return m_dot_in, p_in, T_out, 1

    # Method that is used when we have gas that need to be condensate
    def compute_output_cond(self, m_dot_in, p_in, T_in, x_in):

        T_out = T_in
        if m_dot_in > 0:

            H_out = CP.PropsSI('H', 'T', T_in, 'P', p_in, 'R744')
            H = -self.Qdot / m_dot_in + H_out

            # Add 100 Pa to be sure that we are not in the saturation pressure
            T_out = CP.PropsSI('T', 'H', H, 'P', p_in+100, 'R744')
        return m_dot_in, p_in, T_out, 0

    # Method that can be used while reading power for a file
    def setQdot(self,Qdot):
        self.Qdot = Qdot

    # Function that is called every time we need to recalculate values;
    # it decides to call evaporation or condensation methods depending on 'x';
    def update(self, m_dot, p, T, x):  # 1e-4
        result = None
        if 0.0 - 1e-4 < x < 0.0 + 1e-4:
            result = list(classExchanger.compute_output_evap(self, m_dot, p, T, x))
        elif 1.0 - 1e-4 < x < 1.0 + 1e-4:
            result = list(classExchanger.compute_output_cond(self, m_dot, p, T, x))
        elif x == -1.0:
            phase = CP.PhaseSI('P', p, 'T', T, 'R744')
            if phase == 'liquid':
                result = list(classExchanger.compute_output_evap(self, m_dot, p, T, x))
            elif phase == 'gas':
                result = list(classExchanger.compute_output_cond(self, m_dot, p, T, x))

        return result