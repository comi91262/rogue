# -*- coding: utf-8 -*-

import sys
import os
import struct
import codecs
import pygame
import random
from pygame.locals import *
from dig import *
from main import *

class MoveEvent():
    def __init__(self, pos, mapchip, dest_map, dest_pos, parent):
        self.x, self.y = pos[0], pos[1]  
        self.mapchip = mapchip  
        self.dest_map = dest_map 
        self.dest_x, self.dest_y = dest_pos[0], dest_pos[1]  
        self.image = parent.parent.items[self.name]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        
    def draw(self, screen, offset):
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
        
class DungeonEvent():
    def __init__(self, pos, name, dest_map, wall, floor, parent):
        self.x, self.y = pos[0], pos[1]  
        self.name = name
        self.dest_map = dest_map
        self.wall = wall
        self.floor = floor
        self.image = parent.parent.items[3]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        
    def draw(self, screen, offset):
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
        
        
class ItemEvent():
    def __init__(self, pos, sort, name, parent):
        self.x, self.y = pos[0], pos[1]  
        self.sort = sort
        self.name = name
        self.count = len(name)
        self.order = 0
        self.image = parent.parent.items[self.sort]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))

    def draw(self, screen, offset):
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
        