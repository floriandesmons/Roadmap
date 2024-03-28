# -*- coding: utf-8 -*-
"""
Version 1.0 (Report)

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons

Classes :
-classTankS

Functions :
__init__()
- Initialization of the tank substation parameters

dichotomous_method()
- Calculate the temperature corresponding to the system while using a dichotomous method

state_change()
- Change the simulation values inside the tank for 1 step

set_m_dot_out()
- Change the output mass flow rate at each step (can be used for data stored in datafile)

update()
- update function using new parameters
"""


import CoolProp.CoolProp as CP
import values_storage



class classTankS:

    m = 0
    m_dot_out = 0.5
    p = 0
    Q_dot = 0
    T = 0
    ts = 0
    U = 0
    V = 0
    x = 0

    # Pipe Parameters
    pipe_parameters = [] # Dictionary of pipe parameters

    def __init__(self, x, T, V, ts, Q_dot):   # [-], [K], [m3], [s], [W]

        self.m = CP.PropsSI('D', 'T', T, 'Q', x, 'R744') * V  # [kg] total mass of refrigerant in tank
        self.p = CP.PropsSI('P', 'T', T, 'Q', x, 'R744')
        self.Q_dot = Q_dot # [W] power exchanged inside the tank
        self.T = T  # [K] temperature of refrigerant
        self.ts = ts  # [s] time-step
        self.U = (CP.PropsSI('U', 'T', T, 'Q', x,'R744')) * self.m  # [J] internal energy of refrigerant in tank
        self.V = V  # [m3] total volume of the tank
        self.x = x  # [-] quality (ratio between mass of gas over total mass) of refrigerant


    def dichotomous_method(self):
        T_left = self.T - 5
        T_right = self.T + 5

        while abs(T_left - T_right) > 1e-12:  # 273.15 * 10 ** -2:
            T = (T_left + T_right) / 2

            UL = (CP.PropsSI('U', 'T', T, 'Q', 0, 'R744'))
            UG = (CP.PropsSI('U', 'T', T, 'Q', 1, 'R744'))
            DL = (CP.PropsSI('D', 'T', T, 'Q', 0, 'R744'))
            DG = (CP.PropsSI('D', 'T', T, 'Q', 1, 'R744'))

            Q = (self.U / self.m - UL) / (UG - UL)

            Volume = 1 / DL * self.m * (1 - Q) + 1 / DG * self.m * Q

            if Volume > self.V:
                T_left = T
            else:
                T_right = T

        self.T = T
        self.p = CP.PropsSI('P', 'T', T, 'Q', 0, 'R744')
        self.x = Q

    def state_change(self, m_dot_in, p_in, T_in, x_in):

        mass = self.m
        internalEnergy = self.U

        for i in range(5):

            self.m = mass + (m_dot_in - self.m_dot_out) * self.ts  # [kg]
            self.U = (internalEnergy
                      - self.Q_dot * self.ts
                      + m_dot_in * self.ts * CP.PropsSI('U', 'T', T_in, 'Q', x_in, 'R744')
                      - self.m_dot_out * self.ts * CP.PropsSI('U', 'T', self.T, 'Q', 0, 'R744'))  # [J]
            self.dichotomous_method()

        return self.m_dot_out, self.p, self.T, 0

    def set_m_dot_out(self, value):
        self.m_dot_out = value

    def update(self, m_dot, p, T, x):  # 1e-4

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

        values_storage.x_tank_s.append(self.x)
        values_storage.p_tank_s.append(self.p / 10 ** 5)
        values_storage.T_tank2.append(self.T - 273.15)
        values_storage.m_dot_tank_s.append(m_dot)

        return result

    def get_pressure(self):
        return self.p