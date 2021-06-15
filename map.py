# -*- coding: utf-8 -*-


import random
from pygame.locals import *
from dig import *
from event import *
from menu import *


class Map:
    enemy_list = {}
    images = [] 
    movable_type = [] 
    player_x = 0
    player_y = 0
    wall_panel = 0
    floor_panel = 0
    max_floor = 0
    cur_floor = 0
    max_enemy = 0
    
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.charas = []
        self.statuswnd = StatusWindow(parent.msg_engine)
        self.split_images = parent.split_images
        self.player = Player("alice", (15,15), DOWN, self)
        self.add_chara(self.player)
        self.row = -1  
        self.col = -1  
        self.map_data = []
        self.map_info = []
        self.events = []
        self.is_random = 0
        self.load_event()
        self.load()  
        self.cur_turn = 0
        self.max_turn = 0
        self.turn_all = 0
        self.update_turn_number()
        
        
    def create(self, dest_map, is_random, wall, floor):
        self.name = dest_map
        self.charas = []
        self.events = []
        self.map_data = []
        self.map_info = []
        self.cur_turn = 0
        self.max_turn = 0
        self.turn_all = 0
        self.is_random = 0
        self.is_random = is_random
        if self.is_random == 1:
            self.wall_panel = wall
            self.floor_panel = floor
        self.load_event()
        self.load()
        self.gen_enemy(self.cur_floor)
        self.gen_enemy(self.cur_floor)
        self.gen_enemy(self.cur_floor)
        self.gen_enemy(self.cur_floor)
        self.gen_enemy(self.cur_floor)
      
        
    def add_chara(self, chara):
        self.charas.append(chara)
        
    def update(self):        
        for chara in self.charas:
                chara.update(self)
        if self.cur_turn == self.max_turn:
            self.cur_turn = 0
        self.statuswnd.update()
        
    def gen_enemy(self, cur_floor):
        if self.max_enemy == 25:
            return
        enemy_aux = self.enemy_list[cur_floor]
        enemy = enemy_aux[random.randint(0, len(enemy_aux) - 1)]
        name = enemy[0]
        direction = int(enemy[1])
        movetype = int(enemy[2])
        max_hp = int(enemy[3])
        attack_point =int(enemy[4])
        guard_point =int(enemy[5])
        exp =int(enemy[6])
        prob = enemy[7]
        x, y = self.get_coord()
        if random.randint(0, 99) < prob * 100:
            chara = Enemy(name, (x, y), direction, movetype, max_hp, attack_point, guard_point, exp, self)
            self.charas.append(chara)
            self.update_turn_number()
            self.max_enemy = 1
        
            
    def update_turn_number(self):
        tmp = 0
        for chara in self.charas:
            chara.turn_number = tmp
            tmp = tmp + 1
        self.max_turn = tmp
        
    
    def draw(self, screen):
        offset = self.calc_offset(self.player)
        offsetx, offsety = offset
        startx = offsetx / GS
        endx = startx + PLAY_RECT.width/GS + 1
        starty = offsety / GS
        endy = starty + PLAY_RECT.height/GS + 1
        for y in range(starty, endy):
            for x in range(startx, endx):
                if x < 0 or y < 0 or x > self.col-1 or y > self.row-1:
                    screen.blit(self.images[self.default], (x*GS-offsetx,y*GS-offsety))
                else:
                    screen.blit(self.images[self.map_data[y][x]], (x*GS-offsetx,y*GS-offsety))
        
      
        for event in self.events:
            event.draw(screen, offset)
        for chara in reversed (self.charas):
            chara.draw(screen, offset)
        
        self.statuswnd.draw(screen)
       
    
    def is_movable(self, x, y):
        if x < 0 or x > self.col-1 or y < 0 or y > self.row-1:
            return False
        if self.movable_type[self.map_data[y][x]] == 0:
            return False
        for chara in self.charas:
            if chara.next_x == x and chara.next_y == y:
                return False
        for chara in self.charas:
            if chara.x == x and chara.y == y:
                return False
        return True
    
    
    def attack(self, x, y, player):
        for chara in self.charas:
            if chara.movetype == FRIEND:
                if chara.x == x and chara.y == y:
                    self.parent.talk_field = TalkWindow()
                    self.parent.game_state = TALK
            elif chara.movetype == ENEMY:
                if chara.x == x and chara.y == y:
                    self.cur_turn += 1
                    self.turn_all += 1
                    if self.turn_all % 10 == 0 and self.cur_floor != 0:
                                self.gen_enemy(self.cur_floor)
                    chara.cur_hp -= max(0, player.attack_point - chara.guard_point )
                    self.parent.sounds["hit"].play()
                    player.pushing =True
                    if chara.cur_hp <= 0:
                        self.player.exp += chara.exp
                        self.level_up()
                        self.charas.remove(chara)
                        self.parent.sounds["hit2"].play()
                        self.update_turn_number()
                    
    def level_up(self):
        if (self.player.level == 1 and self.player.exp > 10) or \
            (self.player.level == 2 and self.player.exp > 50) or \
            (self.player.level == 3 and self.player.exp > 150) or \
            (self.player.level == 4 and self.player.exp > 350) or \
            (self.player.level == 5 and self.player.exp > 650) or \
            (self.player.level == 6 and self.player.exp > 950) or \
            (self.player.level == 7 and self.player.exp > 1200) or \
            (self.player.level == 8 and self.player.exp > 1700) or \
            (self.player.level == 9 and self.player.exp > 2500):
            self.parent.sounds["level_up"].play()
            self.player.level += 1
            self.player.attack_point += 4
            self.player.max_hp += 30
            
    def get_chara(self, x, y):
        for chara in self.charas:
            if chara.next_x == x and chara.next_y == y:
                return chara
        return None
    
    def get_event(self, x, y):
        for event in self.events:
            if event.x == x and event.y == y:
                return event
            
        return None
    def load(self):
        file = os.path.join("data", self.name + ".map")
        fp = open(file, "rb")
        self.row = struct.unpack("i", fp.read(struct.calcsize("i")))[0] 
        self.col = struct.unpack("i", fp.read(struct.calcsize("i")))[0] 
        self.default = struct.unpack("B", fp.read(struct.calcsize("B")))[0]  
        if self.is_random == 1:
            gen = DgGenerator(self.row, self.col, self.wall_panel, self.floor_panel)
            self.map_data, self.map_info = gen.start()
            player_i, player_j = self.get_coord()
            self.player.set_pos(player_i, player_j, DOWN)  # プレイヤーを移動先座標へ
            self.add_chara(self.player)  # マップに再登録
            self.update_turn_number()
            if self.cur_floor <  self.max_floor:
                kaidan_i, kaidan_j = self.get_coord()
                move = DungeonEvent((kaidan_i, kaidan_j), "kaidan", "dungeon", self.wall_panel, self.floor_panel, self)
                self.events.append(move)
                self.cur_floor += 1
        else:
            self.map_data = [[0 for c in range(self.col)] for r in range(self.row)]
            for r in range(self.row):
                for c in range(self.col):
                    self.map_data[r][c] = struct.unpack("B", fp.read(struct.calcsize("B")))[0]
        fp.close()
        
    def get_coord(self):
        while True:
            i = random.randint(0, self.row - 1)
            j = random.randint(0, self.col - 1)
            if self.map_info[i][j].get_panel() == ROOM:
                return  j, i


        
    def load_event(self):
        file = os.path.join("data", self.name + ".evt")
        fp = codecs.open(file, "r", "utf-8")
        for line in fp:
            line = line.rstrip()  
            if line.startswith("#"): continue  
            data = line.split(",")
            event_type = data[0]
            if event_type == "BGM":
                self.play_bgm(data)
            elif event_type == "CHARA":  
                self.create_chara(data)
            elif event_type == "ENEMY":
                self.create_enemy(data)
            elif event_type == "ENEMY_DUN":
                self.create_enemy_dungeon(data)
            elif event_type == "MOVE":  
                self.create_move(data)
            elif event_type == "MOVE_DUN":
                self.create_dungeon(data)
            elif event_type == "ITEM":  
                self.create_item(data)
        fp.close()
        
    def play_bgm(self, data):
        bgm_file = "%s.mp3" % data[1]
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)
        
    def create_chara(self, data):
        name = data[1]
        x, y = int(data[2]), int(data[3])
        direction = int(data[4])
        movetype = int(data[5])
        max_hp = int(data[6])
        cur_hp = int(data[7])
        attack = int(data[8])
        guard = int(data[9])
        exp = int(data[10])
        chara = Character(name, (x,y), direction, movetype, self, max_hp, cur_hp, attack, guard, exp)
        self.charas.append(chara)
        
    def create_enemy(self, data):
        name = data[1]
        x, y = int(data[2]), int(data[3])
        direction = int(data[4])
        movetype = int(data[5])
        max_hp = int(data[6])
        attack_point =int(data[7])
        guard_point =int(data[8])
        exp =int(data[9])
        chara = Enemy(name, (x,y), direction, movetype, max_hp, attack_point, guard_point, exp, self)
        self.charas.append(chara)
        
    def create_enemy_dungeon(self,data):
        name = data[1]
        direction = int(data[2])
        movetype = int(data[3])
        max_hp = int(data[4])
        attack_point =int(data[5])
        guard_point =int(data[6])
        exp =int(data[7])
        enemy_floor = int(data[8])
        prob = float(data[9])
        if enemy_floor in self.enemy_list:
            enemy_list = self.enemy_list[enemy_floor]
            enemy_list.append([name, direction, movetype, max_hp, attack_point, guard_point, exp, prob])
            self.enemy_list[enemy_floor] = enemy_list
        else:
            self.enemy_list[enemy_floor] = [[name, direction, movetype, max_hp, attack_point, guard_point, exp, prob]]

        
        
    def create_move(self, data):
        x, y = int(data[1]), int(data[2])
        name = int(data[3])
        dest_map = data[4]
        dest_x, dest_y = int(data[5]), int(data[6])
        move = MoveEvent((x,y), name, dest_map, (dest_x,dest_y), self)
        self.events.append(move)
        
    def create_dungeon(self, data):
        x, y = int(data[1]), int(data[2])
        name = data[3]
        dest_map = data[4]
        wall_panel, floor_panel = int(data[5]), int(data[6])
        self.max_floor = int(data[7])
        move = DungeonEvent((x,y), name, dest_map, wall_panel, floor_panel, self)
        self.events.append(move)
        
    def create_item(self,data):
        sort = int(data[1])
        name = data[2]
        x, y = int(data[3]), int(data[4])
        item = ItemEvent((x,y),sort, name, self)
        self.events.append(item)
        
    
        
    def calc_offset(self, player):
        offsetx = player.rect.topleft[0] - PLAY_RECT.width/2
        offsety = player.rect.topleft[1] - PLAY_RECT.height/2
        return offsetx, offsety   
        