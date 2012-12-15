#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module provides a class that controls a Laser Scanner
# manufactured by HOKUYO AUTOMATIC CO,LTD
# HOKUYO AUTOMATIC CO,LTD(http://www.hokuyo-aut.co.jp/index.html)
#
# This module has been tested on python ver.2.6.6
# Please install the following modules
# numpy(http://numpy.scipy.org/)
# matplotlib(http://matplotlib.org/index.html)
#
# ver1.21206
# (C) 2012 Matsuda Hiroaki 

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

import ConfigParser as Conf

class Viewer(object):

    def __init__(self):
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        self.conf = Conf.SafeConfigParser()
        self.conf.read('ini/view.ini')
		
        self.x_min = float(self.conf.get('VIEW', 'x_min'))
	self.x_max = float(self.conf.get('VIEW', 'x_max'))
	self.y_min = float(self.conf.get('VIEW', 'y_min'))
	self.y_max = float(self.conf.get('VIEW', 'x_max'))
	self.z_min = float(self.conf.get('VIEW', 'z_min'))
	self.z_max = float(self.conf.get('VIEW', 'z_max'))

	self.mode = self.conf.get('VIEW', 'mode')
	self.color = self.conf.get('VIEW', 'color')
	self.title = self.conf.get('VIEW', 'title')

	self.angle_min = int(self.conf.get('URG', 'angle_min'))
	self.angle_max = int(self.conf.get('URG', 'angle_max'))
	self.step = float(self.conf.get('URG', 'step'))

    def plot(self):
        x = [0 for i in range(1080)]
        y = [0 for i in range(1080)]
        z = [0 for i in range(1080)]

        if self.mode == 'hold':
            self.ax.hold(True)
            point = self.ax.plot(x, y, z, 'o', markersize = 2.0, color = self.color, alpha = 0.02)

        else:
            point = self.ax.plot(x, y, z, 'o', markersize = 2.0, color = self.color, alpha = 0.5)

        self.ax.set_xlim3d([self.x_min, self.x_max])
        self.ax.set_xlabel('X')

        self.ax.set_ylim3d([self.y_min, self.y_max])
        self.ax.set_ylabel('Y')

        self.ax.set_zlim3d([self.z_min, self.z_max])
        self.ax.set_zlabel('Z')

        self.ax.set_title(self.title)

        # Creating the Animation object
        self.ani = animation.FuncAnimation(self.fig, self.update, 25, fargs=(self.fig, point),
                              interval = 50, blit = False)# blit = False

    def show(self):
        plt.show()

    def update(self, num, fig, point):
        try:
            x, y, z = self.get_data()
            
            if self.mode == 'HOLD':
                self.ax.plot(x, y, z, 'o', markersize = 2.0, color = self.color, alpha = 0.02)
                self.ax.set_xlim3d([-5000.0, 5000.0])
                self.ax.set_xlabel('X')

                self.ax.set_ylim3d([-5000.0, 5000.0])
                self.ax.set_ylabel('Y')

                self.ax.set_zlim3d([-5000.0, 5000.0])
                self.ax.set_zlabel('Z')

            else:
                point[0].set_data(x, y)
                point[0].set_3d_properties(z, zdir='z')
        except:
            pass
        

    def get_data(self):
        data = self.in_port()
        
        timestamp = data[0]
        angle = data[1] - 245
        length = data[2]
        dist_length = data[3]
        
        if length == 1:
            dist = data[4:]

        elif length == 2:
            dist = data[4:4 + dist_length]
            
        x, y, z = self.convert_to_x_y_z(dist, angle)

        return x, y, z
        

    def get_in_port(self, func):
        self.in_port = func

    def convert_to_x_y_z(self, data, angle):
        x = []
        y = []
        z = []
        
        #step = self._calc_one_step()
        #step = 0.25
        rad = np.pi / 180.0
                
        for i, dist in enumerate(data):
            if dist < 20:
                dist = 0
            theta = self.angle_min +  i * self.step
            #theta = -135 +  i * step

            temp_x = dist * np.sin(theta * rad)

            x.append(temp_x * -np.sin(angle / 10.0 * rad))
            y.append(temp_x * np.cos(angle / 10.0 * rad))
            z.append(dist * np.cos(theta * rad))
        
        return x, y, z
