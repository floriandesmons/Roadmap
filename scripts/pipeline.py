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
- Initialization of the pipe parameters

compute_fd_colebrook_white()
- compute the colebrook white model to calculate the fd parameter

compute_output_pipe()
- Compute a step of the pipeline instance with the input values

get_pipe_parameters()
- Return the pipe parameters needed into the tank central class

update()
- update function using new parameters
"""


import CoolProp.CoolProp as CP


class classPipes():

    # Pipes variables
    L = 0
    d = 0
    r = 0
    k = 0
    rho = 0
    fd = 0

    # Simulation variables
    m_dot_in = 0
    p_in = 0
    T_in = 0
    x_in = 0

    def __init__(self, L, d, k):  # [m], [m], [m]
        self.L = L    # pipe length [m]
        self.d = d    # pipe diameter [m]
        self.r = d/2  # pipe radius [m]
        self.k = k    # pipe roughness [m]

    def compute_fd_colebrook_white(self, k, Re):
        from math import log10

        lamda_n = 0.0
        lamda_np1 = 0.05

        count = 0
        while abs(lamda_n - lamda_np1) / lamda_np1 > 1e-9 and count < 1000:
            count += 1
            lamda_n = lamda_np1
            lamda_np1 = -2 * log10(2.51 / Re / lamda_n ** 0.5 + k / 3.71 / self.d)
            lamda_np1 = lamda_np1 ** 2
            lamda_np1 = 1.0 / lamda_np1

        return lamda_np1

    def compute_output_pipe(self, m_dot_in, p_in, T_in, x_in):
        from math import pi

        # variables
        self.m_dot_in = m_dot_in
        self.p_in = p_in
        self.T_in = T_in
        self.x_in = x_in

        self.rho = CP.PropsSI('D', 'T', T_in, 'Q', x_in, 'R744')
        mu = CP.PropsSI('V', 'T', T_in, 'Q', x_in, 'R744')

        # Pressure loss in the pipe
        # Loop to converge to the real result of fd
        for step in range(10):

            if m_dot_in < 1e-10 and step == 0:
                Re = 1000
            elif step == 0:
                V = m_dot_in / self.rho / (pi * self.r ** 2)
                Re = self.rho * V * self.d / mu
            else:
                V = m_dot_in / self.rho / (pi * self.r ** 2)
                Re = self.rho * V * self.d / mu

            self.fd = self.compute_fd_colebrook_white(self.k, Re)

        # Calculation of the pressure loss inside the pipe
        deltaP = m_dot_in ** 2 * (self.fd * self.L) / (4 * pi * self.rho * self.r ** 5)
        p_out = p_in - deltaP

        return m_dot_in, p_out , T_in , self.x_in

    def get_pipe_parameters(self):

        return {'r': self.r,
                'L': self.L}

    def update(self, m_dot, p, T, x):
        result = None

        if 0.0 - 1e-4 < x < 0.0 + 1e-4:
            result = list(self.compute_output_pipe(m_dot, p, T, 0.0))

        elif 1.0 - 1e-4 < x < 1.0 + 1e-4:
            result = list(self.compute_output_pipe(m_dot, p, T, 1.0))

        elif x == -1.0:
            phase = CP.PhaseSI('P', p, 'T', T, 'R744')
            if phase == 'liquid':
                result = list(self.compute_output_pipe(m_dot, p, T, 0.0))

            elif phase == 'gas':
                result = list(self.compute_output_pipe(m_dot, p, T, 1.0))

        return result
