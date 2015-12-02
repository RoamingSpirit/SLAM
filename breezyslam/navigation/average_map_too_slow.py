'''
Too slow way to make the map.
             
author: Nils Bernhardt 
'''
import numpy as np


class Map():

    def __init__(self, mapsize_pixel, mapsize_meter, robot_size):
        self.meter_to_pixel = float(mapsize_pixel)/mapsize_meter
        self.mapsize_pixel = mapsize_pixel
        self.mapsize_meter = mapsize_meter
        self.robot_size = robot_size
        self.grid_width = int(mapsize_meter/robot_size)
        self.cell_width = float(mapsize_pixel)/self.grid_width
        self.grid = bytearray(self.grid_width * self.grid_width)
        for i in range(0, len(self.grid)): self.grid[i] = 127

    
    def update(self, data, position, scan_range):
        scan_range_pixel = self.meter_to_pixel*scan_range
        x_pos = self.meter_to_pixel * position[0]
        y_pos = self.meter_to_pixel * position[1]
        startX = (x_pos-scan_range_pixel)/self.cell_width
        endX = (x_pos+scan_range_pixel)/self.cell_width
        startY = (y_pos-scan_range_pixel)/self.cell_width
        endY = (y_pos+scan_range_pixel)/self.cell_width
        for x in range(0, self.getWidth()):
            for y in range(0, self.getWidth()):
                self.setValue(x, y, self.getAverage(x, y, data))

    def getAverage(self, x_grid, y_grid, data):
        startX = x_grid*self.cell_width
        endX = int(startX + self.cell_width)
        startX = int(startX)

        startY = y_grid*self.cell_width
        endY = int(startY + self.cell_width)
        startY = int(startY)
        
        value = 0
        
        for x in range(startX, endX):
            for y in range(startY, endY):
                value += data[y*self.mapsize_pixel + x]

        width = (endX-startX) * (endY-startY)
        return int(value/width)
            
        
    def getWidth(self):
        return self.grid_width

    def getValue(self, x, y):
        return self.grid[y*self.getWidth()+x]

    def setValue(self, x, y, value):
        self.grid[y*self.getWidth()+x] = value 

    def getValues(self):
        return self.grid

    def __str__(self):
        return "grid size: %d ; grid values: %d ; cell_width: %f" % (self.getWidth(), len(self.grid), self.cell_width)
