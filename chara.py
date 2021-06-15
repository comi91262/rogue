# -*- coding: utf-8 -*-

import pygame
import random
from pygame.locals import *
from dig import *
from map import *
from math import atan2, degrees, pi

GS = 32
DOWN,LEFT,RIGHT,UP = 0,1,2,3
FRIEND, MOVE, ENEMY= 0,1,2

class Character:
    speed = 4  
    animcycle = 24  
    frame = 0
    direction_list = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    
    def __init__(self, name, pos, dir, movetype, parent, max_hp, cur_hp, attack, guard, exp):
        self.name = name 
        self.parent = parent
        self.split_images = parent.split_images
        self.image = self.split_images[name][0] 
        self.trun_number = 0
        self.x, self.y = pos[0], pos[1]
        self.next_x, self.next_y = 0, 0
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.vx, self.vy = 0, 0 
        self.moving = False  
        self.direction = dir  
        self.movetype = movetype 
        self.max_hp = max_hp
        self.cur_hp = cur_hp
        self.attack_point = attack
        self.guard_point = guard
        self.exp = exp
        
        
    def update(self, map):
        self.frame += 1
        self.image = self.split_images[self.name][self.direction*3+self.frame/self.animcycle%3]
        if self.moving == True:
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  
                self.moving = False
                self.x = self.rect.left / GS
                self.y = self.rect.top / GS
        
        elif self.movetype == FRIEND:
            if self.parent.cur_turn != self.turn_number:
                return
            rand = random.randint(0, 9)
            if rand == 0:
                map.statuswnd.message_list.append(u"%sはこちらを見ている。"  %self.name)
            map.cur_turn +=  1
            
        elif self.movetype == MOVE:
            if self.parent.cur_turn != self.turn_number:
                return

            rand_x = random.randint(0, 2) - 1
            rand_y = random.randint(0, 2) - 1
            if rand_x == -1 and rand_y == -1:
                self.direction = LEFT
            elif rand_x == 0 and rand_y == -1:
                self.direction = UP
            elif rand_x == 1 and rand_y == -1:
                self.direction = RIGHT
            elif rand_x == -1 and rand_y == 0:
                self.direction = LEFT
            elif rand_x == 1 and rand_y == 0:
                self.direction = RIGHT
            elif rand_x == -1 and rand_y == 1:
                self.direction = LEFT
            elif rand_x == 0 and rand_y == 1:
                self.direction = DOWN
            elif rand_x == 1 and rand_y == 1:
                self.direction = RIGHT
                
            self.step(rand_x, rand_y)
            map.cur_turn +=  1
    
        elif self.movetype == ENEMY:
            if self.parent.cur_turn != self.turn_number:
                return
            if self.enemy_attack(map):
                map.cur_turn += 1 
                return
            angle = degrees (atan2 (-(map.player.next_y - self.next_y), map.player.next_x - self.next_x))
            if angle < 0:
                angle += 360
            self.move(angle)
            map.cur_turn +=  1
           
    def move(self, angle):
        direction = int(angle / 22.5)
        if direction == 0:
            self.direction = RIGHT
            if not (self.step(1, 0)):
                self.step(1, - 1)
        if direction == 1:
            self.direction = RIGHT
            if not (self.step(1,  - 1)):
                self.step( + 1, 0)
        if direction == 2:
            self.direction = UP
            if not (self.step(1,  - 1)):
                self.step(0,  - 1)
        if direction == 3:
            self.direction = UP
            if not (self.step(0,  - 1)):
                self.step( + 1,  - 1)
        if direction == 4:
            self.direction = UP
            if not (self.step(0,  - 1)):
                self.step( - 1,  - 1)
        if direction == 5:
            self.direction = UP
            if not (self.step( - 1,  - 1)):
                self.step(0,  - 1)
        if direction == 6:
            self.direction = LEFT
            if not (self.step( - 1,  - 1)):
                self.step( - 1, 0)
        if direction == 7:
            self.direction = LEFT
            if not (self.step( - 1, 0)):
                self.step( - 1,  - 1)
        if direction == 8:
            self.direction = LEFT
            if not (self.step( - 1, 0)):
                self.step( - 1,  + 1)
        if direction == 9:
            self.direction = LEFT
            if not (self.step( - 1,  + 1)):
                self.step( - 1, 0)
        if direction == 10:
            self.direction = DOWN
            if not (self.step( - 1,  + 1)):
                self.step(0,  + 1)
        if direction == 11:
            self.direction = DOWN
            if not (self.step(0,  + 1)):
                self.step( - 1,  + 1)
        if direction == 12:
            self.direction = DOWN
            if not (self.step(0,  + 1)):
                self.step( + 1,  + 1)
        if direction == 13:
            self.direction = DOWN
            if not (self.step(1, 1)):
                self.step(0,  + 1)
        if direction == 14:
            self.direction = RIGHT
            if not (self.step(1, 1)):
                self.step( + 1, 0)
        if direction == 15:
            self.direction = RIGHT
            if not (self.step( + 1, 0)):
                self.step( + 1,  + 1)
    
    def step(self, x, y):
        if self.parent.is_movable(self.x + x, self.y + y):
            self.vx, self.vy = x * self.speed, y * self.speed
            self.moving = True
            self.next_x = self.x + x
            self.next_y = self.y + y
            return True
        return False                                     
        
    def set_pos(self, x, y, dir):
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.direction = dir
        
    def draw(self, screen, offset):
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
        
    def enemy_attack(self, map):
        for (x, y) in self.direction_list:
            chara = map.get_chara (self.x + x, self.y + y)
            if chara != None:
                if chara.x == map.player_x and chara.y == map.player_y:
                    map.player.cur_hp -= self.attack_point
                    map.parent.sounds["hit"].play()
                    return True
        return False
        
        
class Enemy(Character):
    
    def __init__(self,name,pos,dir,movetype, hp, attack, guard, exp, parent):
        Character.__init__(self, name, pos, dir, ENEMY, parent, hp, hp, attack, guard, exp)
        self.msg_engine = parent.parent.msg_engine
        self.dest_x, self.dest_y = self.search_dest()
        self.relay1_x = 0
        self.relay1_y = 0
        self.relay2_x = 0
        self.relay2_y = 0
        self.relay3_x = 0
        self.relay3_y = 0
        self.place_panel = ROOM
        self.pos_panel = ROOM
        
            
    def search_dest(self):
        dest_list = self.parent.map_info[self.y][self.x].get_enter_point()
        while True:
            (x, y) = dest_list[random.randint(0, len(dest_list) - 1)]
            if x == self.x and y == self.y:
                continue
            return x, y
        
    def search_relay(self):
        [((self.relay1_x, self.relay1_y), (self.relay2_x, self.relay2_y))] = self.parent.map_info[self.y][self.x].get_relay_point()
    
    def update(self, map):
        self.frame += 1
        self.image = self.split_images[self.name][self.direction*3+self.frame/self.animcycle%3]
        from math import atan2, degrees, pi
         
        if self.moving == True:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了
                self.moving = False
                self.x = self.rect.left / GS
                self.y = self.rect.top / GS
                
        else:
            if self.parent.cur_turn != self.turn_number:
                return
            if self.enemy_attack(map):
                map.cur_turn += 1 
            else: 
                if self.place_panel == ROOM:
                    self.pos_panel = ROOM
                    if self.is_same_room(self.x, self.y):
                        self.dest_x, self.dest_y = self.parent.player_x, self.parent.player_y
                    angle = degrees (atan2 (-(self.dest_y - self.y), self.dest_x - self.x))
                    if angle < 0:
                        angle += 360
                    self.move(angle)
                    self.parent.cur_turn = self.parent.cur_turn + 1
                elif self.place_panel == WAY:
                    self.pos_panel = WAY
                    if self.x == self.relay1_x and self.y == self.relay1_y:
                        self.dest_x, self.dest_y = self.relay2_x, self.relay2_y
                    if self.x == self.relay2_x and self.y == self.relay2_y:
                        self.dest_x, self.dest_y = self.relay3_x, self.relay3_y
                    angle = degrees (atan2 (-(self.dest_y - self.y), self.dest_x - self.x))
                    if angle < 0:
                        angle += 360 
                    self.move(angle)
                    self.parent.cur_turn = self.parent.cur_turn + 1
                elif self.place_panel == ENTER:
                    self.dest_x, self.dest_y = self.search_dest()
                    if len(self.parent.map_info[self.y][self.x].get_enter_point()) == 2:
                        if self.is_same_room(self.x, self.y):
                            self.dest_x, self.dest_y = self.parent.player_x, self.parent.player_y
                            angle = degrees (atan2 (-(self.dest_y - self.y), self.dest_x - self.x))
                            if angle < 0:
                                angle += 360 
                            self.move(angle)
                            self.parent.cur_turn = self.parent.cur_turn + 1
                        elif self.check_line(self.x, self.dest_x, True) or self.check_line(self.y, self.dest_y, False):
                            self.search_relay()
                            self.relay3_x, self.relay3_y = self.dest_x, self.dest_y
                            self.dest_x, self.dest_y = self.relay1_x, self.relay1_y
                            angle = degrees (atan2 (-(self.dest_y - self.y), self.dest_x - self.x))
                            if angle < 0:
                                angle += 360 
                            self.move(angle)
                            self.parent.cur_turn = self.parent.cur_turn + 1
                    else:
                        if self.pos_panel == ROOM:
                            if self.is_same_room(self.x, self.y):
                                self.dest_x, self.dest_y = self.parent.player_x, self.parent.player_y
                            elif self.check_line(self.x, self.dest_x, True) or self.check_line(self.y, self.dest_y, False):
                                self.search_relay()
                                self.relay3_x, self.relay3_y = self.dest_x, self.dest_y
                                self.dest_x, self.dest_y = self.relay1_x, self.relay1_y
                            angle = degrees (atan2 (-(self.dest_y - self.y), self.dest_x - self.x))
                            if angle < 0:
                                angle += 360 
                            self.move(angle)
                            self.parent.cur_turn = self.parent.cur_turn + 1
                        elif self.pos_panel == WAY:
                            if not (self.check_line(self.x, self.dest_x, True) or self.check_line(self.y, self.dest_y, False)):
                                angle = degrees (atan2 (-(self.dest_y - self.y), self.dest_x - self.x))
                                if angle < 0:
                                    angle += 360 
                                self.move(angle)
                                self.parent.cur_turn = self.parent.cur_turn + 1
                        
        self.place_panel = self.parent.map_info[self.y][self.x].get_panel()
            
    def is_same_room(self, x, y):
        return not (self.check_line(x, self.parent.player_x, True) or self.check_line(y, self.parent.player_y, False)) and \
            (self.parent.map_info[self.parent.player_y][self.parent.player_x].get_panel() == ROOM or \
            self.parent.map_info[self.parent.player_y][self.parent.player_x].get_panel() == ENTER)
                    
        
    def check_line(self, s, t, x_frag):
        if s > t:
            s, t = self.swap(s, t)
        for i in range(s, t + 1):
            if x_frag:
                if self.parent.map_info[self.y][i].get_panel() == WALL:
                    return True
            else:
                if self.parent.map_info[i][self.x].get_panel() == WALL:
                    return True
        return False
        
        
    def swap(self, a, b):
        return b, a
            
                
    def draw(self, screen, offset):
        """オフセットを考慮してプレイヤーを描画"""
        Character.draw(self, screen, offset)
       
    

  
