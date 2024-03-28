# -*- coding: utf-8 -*-
"""
Version 1.0 (Report)

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons

Classes :
-classTankC

Functions :
__init__()
- Initialization of the tank central parameters

dichotomous_method()
- Calculate the temperature corresponding to the system while using a dichotomous method

findMassFlowRate()
- Compute the output mass flow rate

compute_fd_colebrook_white()
- Compute the fd coefficient used in findMassFlowRate function by solving the Colebrook white equation

state_change()
- Change the simulation values inside the tank for 1 step

set_delta_pressure()
- Change the delta pressure value stored in the tank (should be used with tank substation instance)

update()
- update function using new parameters
"""


import CoolProp.CoolProp as CP
import values_storage


class classTankC:

    delta_p = 0
    m = 0
    p = 0
    p_tankS = 0
    T = 0
    ts = 0
    U = 0
    V = 0
    x = 0

    # Pipe Parameters
    pipe_parameters = [] # Dictionary of pipe parameters

    def __init__(self, x, T, V, ts):  # [], [K], [m3], [s]

        self.m = CP.PropsSI('D', 'T', T, 'Q', x, 'R744') * V  # [kg] total mass of refrigerant in tank
        self.p = CP.PropsSI('P', 'T', T, 'Q', x, 'R744')
        self.T = T  # [K] temperature of refrigerant
        self.ts = ts  # [s] time-step
        self.U = (CP.PropsSI('U', 'T', T, 'Q', x,'R744')) * self.m  # [J] internal energy of refrigerant in tank
        self.V = V  # [m3] total volume of the tank
        self.x = x  # [-] quality (ratio between mass of gas over total mass) of refrigerant

    def dichotomous_method(self):
        T_left = self.T - 5
        T_right = self.T + 5

        while abs(T_left - T_right) > 1e-12:

            T = (T_left + T_right) / 2

            UL = (CP.PropsSI('U', 'T', T, 'Q', 0, 'R744'))
            UG = (CP.PropsSI('U', 'T', T, 'Q', 1, 'R744'))
            DL = (CP.PropsSI('D', 'T', T, 'Q', 0, 'R744'))
            DG = (CP.PropsSI('D', 'T', T, 'Q', 1, 'R744'))

            Q = (self.U / self.m - UL) / (UG - UL)

            Volume = 1.0 / DL * self.m * (1.0 - Q) + 1.0 / DG * self.m * Q

            if Volume > self.V:
                T_left = T
            else:
                T_right = T

        self.T = T
        self.p = CP.PropsSI('P', 'T', T, 'Q', Q, 'R744')
        self.x = Q

    def findMassFlowRate(self, Q, mDotIn):
        import math
        rho = CP.PropsSI('D', 'T', self.T, 'Q', Q, 'R744')
        mu = CP.PropsSI('V', 'T', self.T, 'Q', Q, 'R744')

        mDotOut = 0.0

        for step in range(10):

            if mDotIn < 1e-10 and step == 0:
                Re = 1000
            elif step == 0:
                V = mDotIn / rho / (math.pi * self.pipe_parameters['r'] ** 2)
                Re = rho * V * self.pipe_parameters['r'] * 2 / mu
            else:
                V = mDotOut / rho / (math.pi * self.pipe_parameters['r'] ** 2)
                Re = rho * V * self.pipe_parameters['r'] * 2 / mu

            fd = self.compute_fd_colebrook_white(0.00001, Re)
            if (self.delta_p > 0.0):
                mDotOut = self.delta_p ** 0.5 * 2 * math.pi * self.pipe_parameters['r'] ** 2 * (rho * self.pipe_parameters['r'] / fd / self.pipe_parameters['L']) ** 0.5
            else:
                mDotOut = 0.0
                break

        return mDotOut

    def compute_fd_colebrook_white(self, k, Re):
        from math import log10

        lamda_n = 0.0
        lamda_np1 = 0.05
        count = 0
        while abs(lamda_n - lamda_np1) / lamda_np1 > 1e-9 and count < 1000:
            count += 1
            lamda_n = lamda_np1
            lamda_np1 = -2 * log10(2.51 / Re / lamda_n ** 0.5 + k / 3.71 / (self.pipe_parameters['r'] * 2))
            lamda_np1 = lamda_np1 ** 2
            lamda_np1 = 1.0 / lamda_np1

        return lamda_np1

    def state_change(self, m_dot_in, p_in, T_in, x_in):
        from pipeline import classPipes
        from tank_substation import classTankS

        for element in values_storage.created_instances:
            if isinstance(element, classPipes):
                self.pipe_parameters = element.get_pipe_parameters()
            else:
                continue

        for element in values_storage.created_instances:
            if isinstance(element, classTankS):
                self.set_delta_pressure(element.get_pressure())
            else:
                continue

        mass = self.m
        internalEnergy = self.U

        for i in range(5):
            m_dot_out = self.findMassFlowRate(1, m_dot_in)

            self.m = mass + (m_dot_in - m_dot_out) * self.ts  # [kg]
            self.U = (internalEnergy
                    + m_dot_in * self.ts * CP.PropsSI('U', 'T', T_in, 'Q', x_in, 'R744')
                    - m_dot_out * self.ts * CP.PropsSI('U', 'T', self.T, 'Q', 1, 'R744'))  # [J]
            self.dichotomous_method()

        self.U = (internalEnergy
                + m_dot_in * self.ts * CP.PropsSI('U', 'T', T_in, 'Q', x_in, 'R744')
                - m_dot_out * self.ts * CP.PropsSI('U', 'T', self.T, 'Q', 1, 'R744'))

        return m_dot_out, self.p, self.T, 1

    def set_delta_pressure(self, p_tank_substation):
        self.p_tankS = p_tank_substation
        self.delta_p = self.p - p_tank_substation


    def update(self, m_dot, p, T, x):

        result = None
        if 0.0 - 1e-4 < x < 0.0 + 1e-4:
            result = list(self.state_change(m_dot, p, T, 0.0))
        elif 1.0 - 1e-4 < x < 1.0 + 1e-4:
            result = list(self.state_change(m_dot, p, T, 1.0))
        elif x == -1.0:
            phase = CP.PhaseSI('P', p, 'T', T, 'R744')
            if phase == 'liquid':
                result = list(self.state_change(m_dot, p, T, 0.0))
            elif phase == 'gas':
                result = list(self.state_change(m_dot, p, T, 1.0))

        values_storage.x_tank_c.append(self.x)
        values_storage.p_tank_c.append(self.p / 10 ** 5)
        values_storage.m_dot_tank_c.append(m_dot)
        values_storage.T_tank1.append(self.T - 273.15)

        return result
