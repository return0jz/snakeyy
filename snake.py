from curses import KEY_LEFT
import pygame as pg
from pygame import Vector2
import math
import random

RADIUS = 15

class LevelMap: 
    def __init__(self, path):
        self.apple_x = 0
        self.apple_y = 0
        self.obstacles = []
        self.excluded = []
        self.obstacle_spr = pg.transform.scale(pg.image.load("res/obstacle.png"), (32, 32))
        self.apple_spr = pg.transform.scale(pg.image.load("res/apple.png"), (32, 32))
        with open(path, 'r') as file:
            data = file.read().replace('\n', '')
        assert len(data) == 768
        for i in range(0, len(data)):
            if data[i] == ".":
                pass
            elif data[i] == "#":
                self.obstacles.append( (32*(i % 32), 32*math.floor(i/32) ) )
            elif data[i] == "x":
                self.excluded.append( (32*(i % 32), 32*math.floor(i/32) ) )
            else:
                assert False
        self.generate_apple()
    def generate_apple(self):
        repeat = True
        while repeat:
            repeat = False
            self.apple_x = random.randint(0, 31)*32
            self.apple_y = random.randint(0, 15)*32
            for i in self.obstacles:
                if (self.apple_x == i[0]) and (self.apple_y == i[1]):
                    repeat = True
            for i in self.excluded:
                if (self.apple_x == i[0]) and (self.apple_y == i[1]):
                    repeat = True
    def draw(self, screen):
        self.draw_map_only(screen)
        screen.blit(self.apple_spr, pg.Rect(self.apple_x, self.apple_y, 32, 32))
    def draw_map_only(self, screen):
        for o in self.obstacles:
            screen.blit(self.obstacle_spr, pg.Rect(o[0], o[1], 32, 32))

class Snake:
    def __init__(self, coord, speed, turning_scale=1):
        self.turning_scale = turning_scale
        self.speed = speed
        self.head = pg.transform.scale(pg.image.load("res/head.png"), (RADIUS*2, RADIUS*2))
        self.body = pg.transform.scale(pg.image.load("res/body.png"), (RADIUS*2, RADIUS*2))
        self.x = coord[0] 
        self.y = coord[1] 
        self.tongue_x = self.x + RADIUS # coordinates of tongue part of the head
        self.tongue_y = self.x + RADIUS
        self.vec_x = 0 # vector of direction the head is moving
        self.vec_y = 0 #
        self.tail_vec_x = 0 # vector of direction the tail is moving
        self.tail_vec_y = 0
        self.angle = 0
        self.segments = []
    def update(self, dt):
        keys = pg.key.get_pressed()
        self.angle += (keys[pg.K_RIGHT] - keys[pg.K_LEFT])*dt*math.pi*self.turning_scale
        self.vec_x = math.cos(self.angle)
        self.vec_y = math.sin(self.angle)
        self.tail_vec_x = self.vec_x
        self.tail_vec_y = self.vec_y
        self.x += self.vec_x*self.speed*dt
        self.y += self.vec_y*self.speed*dt
        
        for i in range(0, len(self.segments)): # make segments follow the previous (or head)
            if i == 0:
                direction_x = self.x - self.segments[i][0]
                direction_y = self.y - self.segments[i][1]
            else:
                direction_x = self.segments[i-1][0] - self.segments[i][0]
                direction_y = self.segments[i-1][1] - self.segments[i][1]
            mag = (direction_x**2 + direction_y **2)**(1/2)
            if mag >= RADIUS:
                direction_x /= mag
                direction_y /= mag
                self.segments[i][0] += direction_x*self.speed*dt
                self.segments[i][1] += direction_y*self.speed*dt
            if (i+1) == len(self.segments):
                if mag > 0: # one in a thousand chance for mag = 0 (when apple spawns the same place where snake spawns)
                    self.tail_vec_x = direction_x / mag
                    self.tail_vec_y = direction_y / mag
                else:
                    self.tail_vec_x = 0
                    self.tail_vec_y = 0
        
        self.tongue_x = self.x + math.cos(self.angle)*RADIUS # update where tongue is based on angle and location of head
        self.tongue_y = self.y + math.sin(self.angle)*RADIUS
    def draw(self, screen):
        old_head_rect = self.head.get_rect(center = (self.x,self.y))
        rotated = pg.transform.rotate(self.head, -1*self.angle*360/(2*math.pi) + 90)
        new_head_rect = rotated.get_rect(center = old_head_rect.center)
        screen.blit(rotated, new_head_rect)
        
        for i in self.segments:
            screen.blit(self.body, self.body.get_rect(center = (i[0], i[1])))
    def add_segment(self):
        spawn_vec_x = self.tail_vec_x * -1 * RADIUS
        spawn_vec_y = self.tail_vec_y * -1 * RADIUS
        if len(self.segments):
            new_seg = [self.segments[-1][0] + spawn_vec_x, self.segments[-1][1] + spawn_vec_y]
            self.segments.append(new_seg)
        else:
            new_seg = [self.x + spawn_vec_x, self.y + spawn_vec_y]
            self.segments.append(new_seg)
    def is_self_colliding(self):
        for i in self.segments:
            if ((self.tongue_x-i[0])**2 + (self.tongue_y-i[1])**2)**(1/2) <= RADIUS:
                return True
        return False
    def collide_with_rect(self, x, y, w, h):
        if (self.tongue_x >= x) and (self.tongue_x <= x+w) and (self.tongue_y >= y) and (self.tongue_y <= y+h):
            return True
        return False
    def is_dead(self, levelmap):
        if self.is_self_colliding():
            return True
        for i in levelmap.obstacles:
            if self.collide_with_rect(i[0], i[1], 32, 32):
                return True
        return False
    def update_apple(self, levelmap):
        if self.collide_with_rect(levelmap.apple_x, levelmap.apple_y, 32, 32):
            self.add_segment()
            levelmap.generate_apple()
            return True
        return False