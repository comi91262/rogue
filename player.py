# -*- coding: utf-8 -*-

from chara import *
from menu import *

class Player(Character):
    level = 1
    pushing = False
    
    #デバッグ用
    dest_x = 0
    dest_y = 0
    
    def __init__(self, name, pos, dir, parent):
        Character.__init__(self, name, pos, dir, False, parent, 30, 30, 4, 0, 0)
        self.msg_engine = parent.parent.msg_engine
        self.menuwnd = MenuWindow(self, self.msg_engine)
       
           
        
    def update(self, map):
        self.menuwnd.update()
        map.player_x,map.player_y = self.next_x, self.next_y
        self.frame += 1
        self.image = self.split_images[self.name][self.direction*3+self.frame/self.animcycle%3]
        
        """プレイヤー状態を更新する。
        mapは移動可能かの判定に必要。"""
        # プレイヤーの移動処理
        if self.moving == True:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了
                self.moving = False
                self.x = self.rect.left / GS
                self.y = self.rect.top / GS
                # TODO: ここに接触イベントのチェックを入れる
                event = map.get_event(self.x, self.y)
                if event != None:
                    map.statuswnd.message_list.append("%sがある。"% event.name)
                    
        else:
            if map.cur_turn != self.turn_number:
                return
            # プラットフォーム依存っぽい
            pressed_keys = pygame.key.get_pressed()
            count = 0
            for ele in pressed_keys:  
                if ele == 1:
                    count += 1
            if count < 2:
                self.pushing = False
            if self.pushing == False:
                if pressed_keys[K_c]:
                    if pressed_keys[K_DOWN] and pressed_keys[K_RIGHT]:
                        self.direction = DOWN  # 移動できるかに関係なく向きは変える
                        if map.is_movable(self.x+1, self.y+1):
                            self.vx, self.vy = self.speed, self.speed
                            self.moving = True
                            self.next_x = self.x + 1
                            self.next_y = self.y + 1
                            map.cur_turn += 1
                            map.turn_all += 1
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x+1, self.y+1, self)
                    elif pressed_keys[K_DOWN] and pressed_keys[K_LEFT]:
                        self.direction = DOWN  # 移動できるかに関係なく向きは変える
                        if map.is_movable(self.x-1, self.y+1):
                            self.vx, self.vy = - self.speed , self.speed 
                            self.moving = True
                            self.next_x = self.x - 1
                            self.next_y = self.y + 1
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x-1, self.y+1, self)
                    elif pressed_keys[K_UP] and pressed_keys[K_RIGHT]:
                        self.direction = UP  # 移動できるかに関係なく向きは変える
                        if map.is_movable(self.x+1, self.y-1):
                            self.vx, self.vy = self.speed, -self.speed 
                            self.moving = True
                            self.next_x = self.x + 1
                            self.next_y = self.y - 1
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x+1, self.y-1, self)
                    elif pressed_keys[K_UP] and pressed_keys[K_LEFT]:
                        self.direction = UP # 移動できるかに関係なく向きは変える
                        if map.is_movable(self.x-1, self.y-1):
                            self.vx, self.vy = -self.speed , -self.speed 
                            self.moving = True
                            self.next_x = self.x - 1
                            self.next_y = self.y - 1
                            self.cur_hp += 1
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x-1, self.y-1, self)
                    
                else:
                    if pressed_keys[K_DOWN]:
                        self.direction = DOWN  # 移動できるかに関係なく向きは変える
                        if map.is_movable(self.x, self.y+1):
                            self.vx, self.vy = 0, self.speed
                            print id(self.speed)
                            print self.speed
                            self.moving = True
                            self.next_x = self.x
                            self.next_y = self.y + 1
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x, self.y+1, self)
                    elif pressed_keys[K_LEFT]:
                        self.direction = LEFT
                        if map.is_movable(self.x-1, self.y):
                            self.vx, self.vy = -self.speed, 0
                            self.moving = True
                            self.next_x = self.x - 1
                            self.next_y = self.y
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x-1, self.y, self)
                    elif pressed_keys[K_RIGHT]:
                        self.direction = RIGHT
                        if map.is_movable(self.x+1, self.y):
                            self.vx, self.vy = self.speed, 0
                            self.moving = True
                            self.next_x = self.x + 1
                            self.next_y = self.y
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x+1, self.y, self)
                    elif pressed_keys[K_UP]:
                        self.direction = UP
                        if map.is_movable(self.x, self.y-1):
                            self.vx, self.vy = 0, -self.speed
                            self.moving = True
                            self.next_y = self.y - 1
                            self.next_x = self.x
                            map.cur_turn += 1
                            map.turn_all += 1 
                            if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                            if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                        map.attack (self.x, self.y-1, self)
                    elif pressed_keys[K_z] and pressed_keys[K_x]:
                        self.vx, self.vy = 0, 0
                        map.cur_turn = map.cur_turn + 1
                        map.turn_all = map.turn_all + 1
                        if self.cur_hp < self.max_hp: 
                                self.cur_hp += 1
                        if map.turn_all % 10 == 0 and map.cur_floor != 0:
                                map.gen_enemy(map.cur_floor)
                    elif pressed_keys[K_z]:
                        self.pushing =True
                        self.vx, self.vy = 0, 0
                        map.cur_turn += 1
                        map.turn_all += 1 
                        if self.cur_hp <= self.max_hp: 
                                self.cur_hp += 1
                        event = map.get_event(self.x, self.y)
                        self.proc_event(map, event)
                    elif pressed_keys[K_v]:
                        self.pushing = True
                        if self.speed == 4:
                            Character.speed = 8
                        elif self.speed == 8:
                            Character.speed = 4
                    
    def proc_event(self, map, event):
        from event import *
        if isinstance(event, ItemEvent): 
            map.parent.sounds["step"].play()
            map.events.remove(event)
            map.statuswnd.message_list.append(u"%sを手に入れた。" %event.name) 
            self.menuwnd.item_list.append(event)
            count = 0
            for li in self.menuwnd.item_list:
                li.order = count
                count += 1
        
        elif isinstance(event, MoveEvent):  
            map.parent.sounds["step"].play()
            dest_map = event.dest_map
            dest_x = event.dest_x
            dest_y = event.dest_y
            map.create(dest_map, 0)  
            self.set_pos(dest_x, dest_y, DOWN)  
            map.add_chara(self) 
            map.update_turn_number()
        elif isinstance(event, DungeonEvent):
            map.parent.sounds["step"].play()
            dest_map = event.dest_map
            dest_wall = event.wall
            dest_floor = event.floor
            map.statuswnd.message_list.append(u"階段を降りた。") 
            map.create(dest_map, 1, dest_wall, dest_floor)  
        elif event == None:
            map.statuswnd.message_list.append(u"足元には何もない。")
                    
                    
    def draw(self, screen, offset):
        """オフセットを考慮してプレイヤーを描画"""
        self.menuwnd.draw(screen)
        Character.draw(self, screen, offset)
        pygame.draw.rect(screen, (0,255,0), Rect(50,531 ,150 * self.cur_hp / self.max_hp, 25 ))
        pygame.draw.rect(screen, (0,0,0), Rect(50,531, 150, 25), 10)
       