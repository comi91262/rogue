# -*- coding: utf-8 -*-
import os
import pygame
from pygame.locals import *
from pip._vendor.requests.packages.urllib3.util.connection import select

PLAY_RECT = Rect(0, 0, 832, 544)
TITLE,FIELD,TALK,SELECT = 0,1,2,3
CHARA_SIZE = 16
CHARA_MARGIN = 25

def load_image(dir, file):
    file = os.path.join(dir, file)
    try:
        image = pygame.image.load(file)
    except pygame.error, message:
        print "Cannot load image:", file
        raise SystemExit, message
    image = image.convert_alpha()
    return image


class StatusWindow:

    message_list = []
    MAX_MESSAGE = 10
    
    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.window = load_image("system", "log.png")

    def update(self):
        if len(self.message_list) == 0:
            return
        if self.MAX_MESSAGE < len(self.message_list):
            self.message_list.pop(0)
        
        
    def draw(self, screen):
        screen.blit(self.window,(0, 560))
        CHARA_MARGIN = 25
        i = 0
        for li in reversed (self.message_list):
            self.msg_engine.set_color(self.msg_engine.BLACK) 
            self.msg_engine.draw_string(screen, (30, 576 + CHARA_MARGIN * i), li)
            i += 1
        
        
        
class MenuWindow():
    STATUS, SKILL, ITEM = 0, 1, 2
    current = 0
    item_list = []
    
    def __init__(self, parent, msg_engine):
        self.parent = parent
        self.msg_engine = msg_engine
        self.menu_x, self.menu_y = 0,0
        self.window1 = load_image("system", "menu1.png")
        self.window2 = load_image("system", "menu2.png")
        self.window3 = load_image("system", "menu3.png")
        self.select0 = load_image("system", "select0.png")
        self.select1 = load_image("system", "select1.png")
        
        
    def update(self):
        x, y = self.parent.parent.parent.mouse_x, self.parent.parent.parent.mouse_y
        if 55 + PLAY_RECT.width< x < 55 + 133 + PLAY_RECT.width and 46< y < 46 + 26:
            self.current = self.STATUS
        if 200 + PLAY_RECT.width< x < 200 + 133 + PLAY_RECT.width and 46< y < 46 + 26:
            self.current = self.SKILL
        if 345 + PLAY_RECT.width< x < 345 + 133 + PLAY_RECT.width and 46< y < 46 + 26:
            self.current = self.ITEM
        if self.current == self.ITEM:
            for li in self.item_list:
                if 902 < x < 902 + CHARA_SIZE * li.count and 100 + li.order * CHARA_MARGIN < y < 100 + li.order * CHARA_MARGIN + CHARA_SIZE:
                    self.menu_x, self.menu_y = 902, 100 + li.order * CHARA_MARGIN
                    self.parent.parent.parent.game_state = SELECT
                    self.parent.parent.parent.select_field = SelectWindow(self.msg_engine, x, y, li, self.parent.parent.parent)
                    self.parent.parent.parent.mouse_x, self.parent.parent.parent.mouse_y = 0,0
                    return
        
        
    def draw(self, screen):
        if self.current == self.STATUS:
            screen.blit(self.window1,(832, 0))
            self.msg_engine.draw_string(screen, (902, 130), u"%dF" % self.parent.parent.cur_floor)
            self.msg_engine.draw_string(screen, (902, 155), u"LV:%d " % self.parent.level)
            self.msg_engine.draw_string(screen, (902, 180), u"HP:%d/%d" % (self.parent.cur_hp, self.parent.max_hp))
            self.msg_engine.draw_string(screen, (902, 205), u"攻撃力:%d" % self.parent.attack_point)
            self.msg_engine.draw_string(screen, (902, 230), u"防御力:%d" % self.parent.guard_point)
            self.msg_engine.draw_string(screen, (902, 255), u"累計経験値:%d" % self.parent.exp)
        if self.current == self.SKILL:
            screen.blit(self.window2,(832, 0))
        if self.current == self.ITEM:
            screen.blit(self.window3,(832, 0))
            i = 0
            for li in self.item_list:
                self.msg_engine.draw_string(screen, (902, 100 + i * CHARA_MARGIN), li.name)
                i += 1
            self.pos_x, self.pos_y = pygame.mouse.get_pos()
            for li in self.item_list:
                if 902 < self.pos_x < 902 + CHARA_SIZE * li.count and 100 + li.order * CHARA_MARGIN < self.pos_y < 100 + li.order * CHARA_MARGIN + CHARA_SIZE:
                    self.menu_x, self.menu_y = 902, 100 + li.order * CHARA_MARGIN
                    self.draw_line(screen, li.count)
                    return
            
            
            
    def draw_line(self, screen, count):
        for i in range (0, count):
            screen.blit(self.select1, (self.menu_x + i * CHARA_SIZE, self.menu_y))
                
class TalkWindow():
    
    def __init__(self):
        self.talkwnd = load_image("system", "talk.png")
        
    def update(self):
        return
        
    def draw(self, screen):
        screen.blit(self.talkwnd, (420, 205))
        
class SelectWindow():
    
    def __init__(self, msg_engine, x, y, item, parent):
        self.selectwnd = load_image("system", "select0.png")
        self.select1 = load_image("system", "select1.png")
        self.item = item
        self.parent = parent
        self.msg_engine = msg_engine
        self.x = x
        self.y = y
        self.menu_x = 0
        self.menu_y = 0
        
    def update(self):
        return
        
    def draw(self, screen):
        OFFSET = 18
        screen.blit(self.selectwnd, (self.x, self.y))
        self.msg_engine.draw_string(screen, (self.x + OFFSET, self.y + OFFSET), u"装備する")
        self.msg_engine.draw_string(screen, (self.x + OFFSET, self.y + OFFSET + 16), u"置く")
        self.msg_engine.draw_string(screen, (self.x + OFFSET, self.y + OFFSET + 32), u"投げる")
        self.msg_engine.draw_string(screen, (self.x + OFFSET, self.y + OFFSET + 48), u"詳細")
        self.msg_engine.draw_string(screen, (self.x + OFFSET, self.y + OFFSET + 64), u"戻る")
        x, y = pygame.mouse.get_pos()
        for i in range(0, 5):
            if self.x + OFFSET  < x < self.x + OFFSET + CHARA_SIZE * 4 and self.y + OFFSET + i * CHARA_SIZE < y < self.y + OFFSET + (i + 1) * CHARA_SIZE:
                self.menu_x, self.menu_y = self.x + OFFSET, self.y + OFFSET + i * CHARA_SIZE
                self.draw_line(screen, 4)
        x, y = self.parent.mouse_x, self.parent.mouse_y
        i = 0
        if self.x + OFFSET  < x < self.x + OFFSET + CHARA_SIZE * 4 and self.y + OFFSET + i * CHARA_SIZE < y < self.y + OFFSET + (i + 1) * CHARA_SIZE:
            self.parent.map.statuswnd.message_list.append(u"%sを装備した。" %self.item.name)
            self.parent.game_state = FIELD
            self.parent.mouse_x, self.parent.mouse_y = 0,0
                
        
    def draw_line(self, screen, count):
        for i in range (0, count):
            screen.blit(self.select1, (self.menu_x + i * CHARA_SIZE, self.menu_y))

        
        
class MessageEngine:
    FONT_WIDTH = 16
    FONT_HEIGHT = 22
    BLACK,WHITE, RED, GREEN, BRUE = (255,255,255),(0,0,0),(255,0,0),(0,255,0),(0,0,255)
    def __init__(self):
        self.font = pygame.font.Font("mika.ttf", 16)
        self.color = self.WHITE
    def set_color(self, color):
        self.color = color
        if not self.color in [self.WHITE,self.RED,self.GREEN,self.BRUE]:
            self.color = self.WHITE
    def draw_character(self, screen, pos, ch):
        x, y = pos
        try:
            character = self.font.render(ch, True, self.color)
            screen.blit(character, (x,y))
        except KeyError:
            print u"認識できない文字があります:%s" % ch
            return
    def draw_string(self, screen, pos, str1):
        x, y = pos
        for i, ch in enumerate(str1):
            dx = x + self.FONT_WIDTH * i
            self.draw_character(screen, (dx,y), ch)