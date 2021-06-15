#!python
# -*- coding: utf-8 -*-

import sys
import os
import struct
import pygame
import random
from pygame.locals import *
from dig import *
from map import *
from chara import *
from menu import *
from player import *

SCR_RECT = Rect(0, 0, 1440, 810)
PLAY_RECT = Rect(0, 0, 832, 544)
GS = 32

TITLE,FIELD,TALK,SELECT = 0,1,2,3


def load_image(dire, filename):
    filename = os.path.join(dire, filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert_alpha()
    return image

def split_image(image):
        imageList = []
        for i in range(0, 128, GS):
            for j in range(0, 96, GS):
                surface = pygame.Surface((GS,GS))
                surface.blit(image, (0,0), (j,i,GS,GS))
                surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
                surface.convert()
                imageList.append(surface)
        return imageList


class Main:
    split_images = {}
    items = {}
    sounds = {}
    mouse_x = 0
    mouse_y = 0
    talk_field = None
    select_field = None
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF|SRCALPHA)
        pygame.display.set_caption(u"Poteto and Courage v0.33")
        
        self.load_sounds("data", "sound.dat")
        self.load_charachips("data", "charachip.dat")
        self.load_mapchips("data", "mapchip.dat")
        self.load_items("data", "item.dat")
        
        self.msg_engine = MessageEngine()
        self.map = Map("field", self)
        
        self.game_state = FIELD
        self.debug = False
        self.mainloop()
        
    def mainloop(self):
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            self.update()
            self.render()
            pygame.display.update()
            self.check_event()
              
            
        
    def update(self):
        if self.game_state == FIELD:
            self.map.update()
        elif self.game_state == TALK:
            self.talk_field.update()
        elif self.game_state == SELECT:
            self.select_field.update()
           
    def render(self):
        if self.game_state == FIELD:
            self.map.draw(self.screen)
            if self.debug:
                self.debug_mode()
        elif self.game_state == TALK:
            self.talk_field.draw(self.screen)
        elif self.game_state == SELECT:
            self.select_field.draw(self.screen)
            
                
    def check_event(self):
        """イベントハンドラ"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if self.game_state == TITLE:
                self.title_handler(event)
            elif self.game_state == FIELD:
                self.field_handler(event)
            elif self.game_state == TALK:
                self.talk_handler(event)
            elif self.game_state == SELECT:
                self.select_handler(event)
                
    def title_handler(self, event):
        return #TODO:
   
    def field_handler(self, event):
        if event.type == KEYDOWN and event.key == K_LSHIFT:
            self.debug = True
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_x, self.mouse_y = event.pos
            
            
    def talk_handler(self, event):
        if event.type == KEYDOWN and event.key == K_x:
            self.game_state = FIELD
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            self.game_state = FIELD
    
    def select_handler(self, event):
        if event.type == KEYDOWN and event.key == K_x:
            self.game_state = FIELD
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_x, self.mouse_y = event.pos
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            self.game_state = FIELD
            
    def debug_mode(self):
        mx, my = pygame.mouse.get_pos()
        self.msg_engine.set_color(self.msg_engine.RED)
        self.msg_engine.draw_string(self.screen, (10, 30), u"キャラの位置 %d %d" % (self.map.player.x, self.map.player.y))
        self.msg_engine.draw_string(self.screen, (10, 55), u"パネル %d" % (self.map.map_info[self.map.player.y][self.map.player.x].status))
        self.msg_engine.draw_string(self.screen, (10, 80), u"総ターン数 %d" % (self.map.turn_all))
        OFFSET_Y = 160
        tmp2 = 0
        for chara in self.map.charas:
            self.msg_engine.draw_string(self.screen, (10 + tmp2 * OFFSET_Y, 105), u"HP %d/%d" % (chara.cur_hp, chara.max_hp))
            self.msg_engine.draw_string(self.screen, (10+ tmp2 * OFFSET_Y, 130), u"攻撃力:%d" % chara.attack_point)
            self.msg_engine.draw_string(self.screen, (10+ tmp2 * OFFSET_Y, 155), u"防御力:%d" % chara.guard_point)
            self.msg_engine.draw_string(self.screen, (10+ tmp2 * OFFSET_Y, 180), u"獲得経験値:%d" % chara.exp)
            self.msg_engine.draw_string(self.screen, (10+ tmp2 * OFFSET_Y, 205), u"位置:(%d.%d)" % (chara.x, chara.y))
            self.msg_engine.draw_string(self.screen, (10+ tmp2 * OFFSET_Y, 230), u"目的:(%d.%d)" % (chara.dest_x, chara.dest_y))
            tmp2 += 1
            
        
        OFFSET = 24
        tmp = 1
        for (x, y) in self.map.map_info[self.map.player.y][self.map.player.x].enter_point_list:
            self.msg_engine.draw_string(self.screen, (10, 230 + tmp * OFFSET), u"入り口 %d %d" % (x, y))
            tmp += 1
        tmp1 = 0
        for ((x1,y1), (x2, y2)) in self.map.map_info[self.map.player.y][self.map.player.x].relay_point_list:
            self.msg_engine.draw_string(self.screen, (10, 230 + (tmp + tmp1) * OFFSET), u"中継点 (%d,%d) (%d,%d)" % (x1,y1,x2, y2))
            tmp1 += 1
        self.msg_engine.set_color(self.msg_engine.WHITE)
            
    def load_sounds(self, dire, filename):
        """サウンドをロードしてsoundsに格納"""
        filename = os.path.join(dire, filename)
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            se_name = data[0]
            se_file = os.path.join("se", data[1])
            self.sounds[se_name] = pygame.mixer.Sound(se_file)
        fp.close()
    
    def load_charachips(self, dire, filename):
        """キャラクターチップをロードしてCharacter.imagesに格納"""
        filename = os.path.join(dire, filename)
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            chara_id = int(data[0])
            chara_name = data[1]
            self.split_images[chara_name] = split_image(load_image("charachip", "%s.png" % chara_name))
        fp.close()
        
    def load_items(self, dire, filename):
        """キャラクターチップをロードしてCharacter.imagesに格納"""
        filename = os.path.join(dire, filename)
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            item_id = int(data[0])
            item_name = data[1]
            self.items[item_id] = load_image("item", "%s.png" %item_name)
        fp.close()
    
    def load_mapchips(self, dire, filename):
        """マップチップをロードしてMap.imagesに格納"""
        filename = os.path.join(dire, filename)
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()
            data = line.split(",")
            mapchip_id = int(data[0])
            mapchip_name = data[1]
            movable = int(data[2])  # 移動可能か？
            transparent = int(data[3])  # 背景を透明にするか？
            if transparent == 0:
                Map.images.append(load_image("mapchip", "%s.png" % mapchip_name))
            else:
                Map.images.append(load_image("mapchip", "%s.png" % mapchip_name))
            Map.movable_type.append(movable)
        fp.close()
        
    
   

if __name__ == "__main__":
    Main()
