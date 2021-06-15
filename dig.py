#!python
# -*- coding: utf-8 -*-

import pygame
import random
import sys
from _sqlite3 import Row

WALL,ROOM, WAY, ENTER =0, 1, 2, 3


class DgRect:
    
    def __init__(self, left = 0, top = 0, right = 0, bottom = 0):
        self.set(left, top, right, bottom)
        self.width = abs(right - left) + 1
        self.height = abs(bottom - top) + 1
        self.area = self.width * self.height
        
  
    def set(self, left, top, right, bottom):
        self.left = left
        self.top  = top
        self.right = right
        self.bottom = bottom
        self.width = right - left + 1
        self.height = bottom - top + 1
        self.area = self.width * self.height
    
    
class DgDivision:
    def __init__(self, left = 0, top = 0, right = 0, bottom = 0):
        self.outer = DgRect(left, top, right, bottom)
        self.room  = DgRect(left, top, right, bottom)
        self.enter_list = []
        
        
class PanelInfo:
    
    def __init__(self):
        self.status = WALL
        self.enter_point_list = []
        self.relay_point_list = []
        
    def set_panel(self,panel_info):
        self.status = panel_info
        
    def add_enter_point(self, coord):
        self.enter_point_list.append(coord)
        
    def add_relay_point(self, coord):
        self.relay_point_list.append(coord)
        
    def get_panel(self):
        return self.status
   
    def get_enter_point(self):
        return self.enter_point_list
   
    def get_relay_point(self):
        return self.relay_point_list
        
        
        
        

class DgGenerator:
    
    min_room = 5
    mergin = 3
    min_rect = min_room + mergin * 2
    
    def __init__(self, row, col, wall, floor):
        self.row = row
        self.col = col
        self.wall = wall
        self.floor = floor
        self.divList = []
        self.coupleList = []
        self.pairList = []
        self.mapdata = [[wall for i in range (col)] for j in range(row)]
        self.mapinfo  = [[PanelInfo() for i in range (col)] for j in range(row)]
        
    
    def start(self):
        self.divList.append(DgDivision(0, 0, self.col - 1, self.row - 1))
        self.split_division()
        self.create_room()
        self.connect_rooms()
        self.dig()
        self.remove_dup()
        return self.mapdata, self.mapinfo
        
    
    def remove_dup(self):
        for i in range(self.col):
            for j in range(self.row):
                li = self.mapinfo[j][i].enter_point_list
                self.mapinfo[j][i].enter_point_list = list(set(li))
        
    def dig(self):
        for div in self.divList:
            for i in range(div.room.left, div.room.right + 1):
                for j in range(div.room.top, div.room.bottom + 1):
                    self.mapdata[j][i] = self.floor
                    if self.mapinfo[j][i].get_panel() != ENTER:
                        self.mapinfo[j][i].set_panel(ROOM)
                       
                    
                    
        
    def split_division(self):
        parent = self.divList[random.randint(0, len(self.divList)) -1]
        
        if self.check_division_size(parent):
            return
        
        self.divList.remove(parent)       
        child = DgDivision()
        
        if (random.randint(0,1) == 0):
            split_x = parent.outer.width / 2 + parent.outer.left
            old_right = parent.outer.right
            parent.outer.set(parent.outer.left, parent.outer.top, split_x, parent.outer.bottom)
            child.outer.set(split_x, parent.outer.top, old_right, parent.outer.bottom)
        else:
            split_y = parent.outer.height / 2 + parent.outer.top
            old_bottom = parent.outer.bottom
            parent.outer.set(parent.outer.left, parent.outer.top, parent.outer.right, split_y)
            child.outer.set(parent.outer.left, split_y, parent.outer.right, old_bottom)
            
            
        self.divList.append(parent)
        self.divList.append(child)  
        self.split_division()
       
    def check_division_size(self, div):
        return div.outer.right - div.outer.left <= self.min_rect * 2 or \
               div.outer.bottom - div.outer.top <= self.min_rect * 2
        
    
    def create_room(self):
        for div in self.divList:
            rw = random.randint(self.min_room, div.outer.width - self.mergin  * 2)   
            rh = random.randint(self.min_room, div.outer.height - self.mergin  * 2)
            
            sw = random.randint(self.mergin, div.outer.width  - self.mergin - rw)
            sh = random.randint(self.mergin, div.outer.height - self.mergin - rh)
             
            left = div.outer.left + sw
            right = left + rw
            top = div.outer.top + sh 
            bottom = top + rh
            div.room.set(left, top, right, bottom)
            
            
        
           
    def connect_rooms(self):
        for divA in self.divList:
            for divB in self.divList:
                self.add_couple_list(divA, divB)
        
        for isver, divA, divB in self.coupleList:
            if isver:
                ax = divA.room.right
                ay = random.randint(divA.room.top + 1, divA.room.bottom - 1)
                bx = divB.room.left
                by = random.randint(divB.room.top + 1, divB.room.bottom - 1)
                c = divA.outer.right
                self.line(ax, ay, c, ay, (ax, ay),(bx, by))
                self.line(c, by, bx, by, (ax, ay),(bx, by))
                self.line(c, ay, c, by, (ax, ay),(bx, by))
                self.mapinfo[ay][ax].add_relay_point(((c,ay),(c,by)))
                self.mapinfo[by][bx].add_relay_point(((c,by),(c,ay)))
            else:
                ax = random.randint(divA.room.left + 1, divA.room.right - 1) 
                ay = divA.room.bottom
                bx = random.randint(divB.room.left + 1, divB.room.right - 1)
                by = divB.room.top 
                c  = divA.outer.bottom
                self.line(ax, ay, ax, c, (ax, ay),(bx, by))
                self.line(ax, c, bx, c, (ax, ay),(bx, by))
                self.line(bx, c, bx, by, (ax, ay),(bx, by))
                self.mapinfo[ay][ax].add_relay_point(((ax,c),(bx,c)))
                self.mapinfo[by][bx].add_relay_point(((bx,c),(ax,c)))

                
            
            self.update_room_info(divA.room.left, divA.room.top, divA.room.right, divA.room.bottom, ax, ay)
            self.update_room_info(divB.room.left, divB.room.top, divB.room.right, divB.room.bottom, bx, by)
            self.mapinfo[ay][ax].set_panel(ENTER)
            self.mapinfo[ay][ax].add_enter_point((bx, by))
            self.mapinfo[by][bx].set_panel(ENTER) 
            self.mapinfo[ay][ax].add_enter_point((ax, ay))
            

          
            
            
            
                
                            
    def line(self, x1, y1, x2, y2, coord_A, coord_B):
        if x1 == x2: 
            if y1 < y2:
                for i in range(y1, y2 + 1):
                    self.mapdata[i][x1] = self.floor
                    self.mapinfo[i][x1].set_panel(WAY)
                    self.mapinfo[i][x1].add_enter_point(coord_A)
                    self.mapinfo[i][x1].add_enter_point(coord_B)
            else:
                for i in range(y2, y1 + 1):
                    self.mapdata[i][x1] = self.floor
                    self.mapinfo[i][x1].set_panel(WAY)
                    self.mapinfo[i][x1].add_enter_point(coord_A)
                    self.mapinfo[i][x1].add_enter_point(coord_B)
        elif y1 == y2:
            if x2 > x1:
                for i in range(x1, x2 + 1):
                    self.mapdata[y1][i] = self.floor
                    self.mapinfo[y1][i].set_panel(WAY)
                    self.mapinfo[y1][i].add_enter_point(coord_A)
                    self.mapinfo[y1][i].add_enter_point(coord_B)
            else:
                for i in range(x2, x1):
                    self.mapdata[y1][i] = self.floor
                    self.mapinfo[y1][i].set_panel(WAY)
                    self.mapinfo[y1][i].add_enter_point(coord_A)
                    self.mapinfo[y1][i].add_enter_point(coord_B)
                    
                    
 
    def add_couple_list(self, divA, divB):
        if divA == divB:
            return
        if divA.outer.left == divB.outer.right:
            if (True, divB, divA) in self.coupleList:
                return
            self.coupleList.append((True, divB, divA))
        elif divA.outer.right == divB.outer.left:
            if (True, divA, divB) in self.coupleList:
                return
            self.coupleList.append((True, divA, divB))
        elif divA.outer.top == divB.outer.bottom:
            if (False, divB, divA) in self.coupleList:
                return
            self.coupleList.append((False, divB, divA))
        elif divA.outer.bottom == divB.outer.top:
            if (False, divA, divB) in self.coupleList:
                return
            self.coupleList.append((False, divA, divB))
            

           
            
    def update_room_info(self, left, top, right, bottom, x, y):
        for i in range(left , right + 1):
                for j in range(top, bottom + 1):
                    self.mapinfo[j][i].add_enter_point((x, y))
                    

        
                
 
            
        
    
        