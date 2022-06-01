import state
from snake import Snake, LevelMap
from section_ui import LevelEnd
import pygame.freetype as font
import math
import pygame as pg
#TODO - ResourceManager for music, fonts, images (cut loading time

LEVEL_TIME = 15

class Timer: # keep track and display time left in level
    def __init__(self, seconds_to_ring):
        self.seconds_to_ring = seconds_to_ring
        self.retro_font = font.Font("res/pixelart.ttf", 24)
    def draw(self, screen):
        if self.seconds_to_ring >= 0:
            time_left = str(math.floor(self.seconds_to_ring))
            surface, rect = self.retro_font.render("TIME LEFT " + str(time_left),  (255, 255, 255))
            screen.blit(surface, (1024/2-rect.width/2, 50))
    def update(self, dt):
        if self.seconds_to_ring >= 0:
            self.seconds_to_ring -= dt
    def has_rung(self):
        return self.seconds_to_ring <= 0
    
class Counter: # keep track and display score in level
    def __init__(self):
        self.counter = 0
        self.retro_font = font.Font("res/pixelart.ttf", 24)
    def add_one(self):
        self.counter += 1
    def get_score(self):
        return self.counter
    def draw(self, screen):
        surface, rect = self.retro_font.render("SCORE " + str(self.counter), (255, 255, 255))
        screen.blit(surface, (1024/2-rect.width/2, 700))
        
class Level1(state.Scene):
    def on_start(self, data):
        self.player = Snake((64, 64), 150, 1.5)
        self.player.add_segment()
        self.player.add_segment()
        self.map = LevelMap("level1.txt")
        self.timer = Timer(LEVEL_TIME)
        self.counter = Counter()
        pg.mixer.music.load("res/level1.wav")
        pg.mixer.music.play(-1)
        self.sound = pg.mixer.Sound("res/beep.wav")
        self.sound_obj = None
    def on_event(self, e):
        pass
    def on_update(self, dt, fsm):
        self.player.update(dt)
        if self.player.update_apple(self.map):
            self.counter.add_one()
            self.sound_obj = self.sound.play()
        self.timer.update(dt)
        
        if self.player.is_dead(self.map):
            fsm.transition_to(LevelEnd(), [self.map, True, None, None])
        elif self.timer.has_rung():
            fsm.transition_to(LevelEnd(), [self.map, False, 0, self.counter.get_score()])
    def on_draw(self, screen):
        self.timer.draw(screen)
        self.counter.draw(screen)
        self.map.draw(screen)
        self.player.draw(screen)
    def on_exit(self):
        pg.mixer.music.stop()
        if(self.sound_obj):
            self.sound_obj.stop()
        pass

class Level2(state.Scene):
    def on_start(self, data):
        self.player = Snake((64, 64), 200, 1.6)
        self.player.add_segment()
        self.player.add_segment()
        self.map = LevelMap("level2.txt")
        self.timer = Timer(LEVEL_TIME)
        self.counter = Counter()
        pg.mixer.music.load("res/level2.wav")
        pg.mixer.music.play(-1)
        self.sound = pg.mixer.Sound("res/beep.wav")
        self.sound_obj = None
    def on_event(self, e):
        pass
    def on_update(self, dt, fsm):
        self.player.update(dt)
        if self.player.update_apple(self.map):
            self.counter.add_one()
            self.sound_obj = self.sound.play()
        self.timer.update(dt)
        
        if self.player.is_dead(self.map):
            fsm.transition_to(LevelEnd(), [self.map, True, None, None])
        elif self.timer.has_rung():
            fsm.transition_to(LevelEnd(), [self.map, False, 1, self.counter.get_score()])
    def on_draw(self, screen):
        self.timer.draw(screen)
        self.counter.draw(screen)
        self.map.draw(screen)
        self.player.draw(screen)
    def on_exit(self):
        pg.mixer.music.stop()
        if(self.sound_obj):
            self.sound_obj.stop()
        pass

class Level3(state.Scene):
    def on_start(self, data):
        self.player = Snake((64, 64), 275, 1.75)
        self.player.add_segment()
        self.player.add_segment()
        self.map = LevelMap("level3.txt")
        self.timer = Timer(LEVEL_TIME)
        self.counter = Counter()
        pg.mixer.music.load("res/level3.wav")
        pg.mixer.music.play(-1)
        self.sound = pg.mixer.Sound("res/beep.wav")
        self.sound_obj = None
    def on_event(self, e):
        pass
    def on_update(self, dt, fsm):
        self.player.update(dt)
        if self.player.update_apple(self.map):
            self.counter.add_one()
            self.sound_obj = self.sound.play()
        self.timer.update(dt)
        
        if self.player.is_dead(self.map):
            fsm.transition_to(LevelEnd(), [self.map, True, None, None])
        elif self.timer.has_rung():
            fsm.transition_to(LevelEnd(), [self.map, False, 2, self.counter.get_score()])
    def on_draw(self, screen):
        self.timer.draw(screen)
        self.counter.draw(screen)
        self.map.draw(screen)
        self.player.draw(screen)
    def on_exit(self):
        pg.mixer.music.stop()
        if(self.sound_obj):
            self.sound_obj.stop()
        pass

class Level4(state.Scene):
    def on_start(self, data):
        self.player = Snake((64, 64), 325, 2.25)
        self.player.add_segment()
        self.player.add_segment()
        self.map = LevelMap("level4.txt")
        self.timer = Timer(LEVEL_TIME)
        self.counter = Counter()
        pg.mixer.music.load("res/level4.wav")
        pg.mixer.music.play(-1)
        self.sound = pg.mixer.Sound("res/beep.wav")
        self.sound_obj = None
    def on_event(self, e):
        pass
    def on_update(self, dt, fsm):
        self.player.update(dt)
        if self.player.update_apple(self.map):
            self.counter.add_one()
            self.sound_obj = self.sound.play()
        self.timer.update(dt)
        
        if self.player.is_dead(self.map):
            fsm.transition_to(LevelEnd(), [self.map, True, None, None])
        elif self.timer.has_rung():
            fsm.transition_to(LevelEnd(), [self.map, False, 3, self.counter.get_score()])
    def on_draw(self, screen):
        self.timer.draw(screen)
        self.counter.draw(screen)
        self.map.draw(screen)
        self.player.draw(screen)
    def on_exit(self):
        pg.mixer.music.stop()
        if (self.sound_obj):
            self.sound_obj.stop()
        pass