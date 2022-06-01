from curses.ascii import isalpha
from tracemalloc import is_tracing
import state
from snake import LevelMap
import pygame as pg
import pygame.freetype as font
import pygame_textinput as textinput
import math
import section_start
import pickle

#TODO - ResourceManager for music, fonts, images (cut loading time)

class Save:
    state = [[("------------", 1) for i in range(0,10)], [("------------", 1) for i in range(0,10)], [("------------", 1) for i in range(0,10)], [("------------", 1) for i in range(0,10)]]

class RegisterScore(state.Scene):
    def on_start(self, data): # data -> [level_number, score, data]
        self.is_transition = False
        self.counter = 0
        self.level_number = data[0]
        self.score = data[1]
        self.data = data[2]
        def validator(inp):
            is_good = True
            if not (0 <= len(inp) <= 12):
                is_good = False
            for i in inp:
                if not i.isalpha():
                    is_good = False
            return is_good
        self.text_manager = textinput.TextInputManager(validator = validator)
        self.text_input_obj = textinput.TextInputVisualizer(manager=self.text_manager,font_object=pg.font.Font("res/pixelart.ttf", 50))
        self.text_input_obj.cursor_width = 4
        self.text_input_obj.cursor_blink_interval = 400
        self.text_input_obj.cursor_color = (255, 255, 255)
        self.text_input_obj.font_color = (255, 255, 255)
        
        self.retro_font = font.Font("res/pixelart.ttf", 16)
        self.text_surface, self.text_rect = self.retro_font.render("ENTER YOUR NAME TO RECORD YOU HIGH SCORE OF " + str(self.score) + "!", (255, 255, 255))
    def on_event_q(self, q):
        self.text_input_obj.update(q)
    def on_event(self, e):
        if e.type == pg.KEYUP:
            if e.key == pg.K_RETURN:
                self.is_transition = True
                for i in range(0, len(self.data.state[self.level_number])):
                    if self.score >= self.data.state[self.level_number][i][1]:
                        self.data.state[self.level_number].insert(i, (self.text_input_obj.value, self.score))
                        self.data.state[self.level_number].pop()
                        try:
                            with open('save.pck', 'wb') as f:
                                pickle.dump(self.data, f)
                        except:
                            assert False
                        break
                        
    def on_draw(self, screen):
        screen.blit(self.text_input_obj.surface, (1024/2-self.text_input_obj.surface.get_rect().width/2, 250))
        screen.blit(self.text_surface, (1024/2-self.text_rect.width/2, 500))
    def on_update(self, dt, fsm):
        if self.is_transition:
            fsm.transition_to(Leaderboard(), [self.level_number])

class Leaderboard(state.Scene):
    def on_start(self, data): # data -> [level_number]
        self.is_transition = False
        self.level_number = data[0]
        self.retro_font = font.Font("res/pixelart.ttf", 24)
        self.name_surfaces = []
        self.score_surfaces = []
        with open("save.pck", "rb") as f:
            self.data = pickle.load(f)
        for pair in self.data.state[self.level_number]:
            name_surface, rect = self.retro_font.render(pair[0], (255, 255, 255))
            score_surface, rect = self.retro_font.render(str(pair[1]), (255, 255, 255))
            self.name_surfaces.append(name_surface)
            self.score_surfaces.append(score_surface)
        pg.mixer.music.load("res/leaderboard.wav")
        pg.mixer.music.play()
    def on_draw(self, screen):
        for i in range(0, 10):
            screen.blit(self.name_surfaces[i], (384+36, (i+1)*50))
            screen.blit(self.score_surfaces[i], (1024/2 + 64 + 36, (i+1)*50))
    def on_event(self, e):
        if (e.type == pg.KEYDOWN) or (e.type == pg.MOUSEBUTTONDOWN):
            self.is_transition = True
    def on_update(self, dt, fsm):
        if self.is_transition:
            fsm.transition_to(section_start.StartScreen())
    def on_exit(self):
        pg.mixer.music.stop()
            
class CheckHighScore(state.Scene):
    def on_start(self, data): # data -> [level_number, score]
        self.level_number = data[0]
        self.score = data[1]
        try:
            with open("save.pck", "rb") as f:
                self.data = pickle.load(f)
                print(self.data)
        except FileNotFoundError:
            self.data = Save()
            with open("save.pck", "wb") as f:
                pickle.dump(self.data, f)
        self.is_high_score = False
        for save_info in self.data.state[self.level_number]:
            if self.score > save_info[1]:
                self.is_high_score = True
                break
    def on_update(self, dt, fsm):
        if self.is_high_score:
            fsm.transition_to(RegisterScore(), [self.level_number, self.score, self.data])
        else:
            fsm.transition_to(Leaderboard(), [self.level_number])

class LevelPreview(state.Scene):
    def on_start(self, data):
        self.map = LevelMap(data[0])
        self.next_state = data[1]
        self.is_transition = False
        
        self.black_surface = pg.Surface((1024, 768))
        self.black_surface.set_alpha(128)
        self.black_surface.fill((0, 0, 0))
        
        self.retro_font = font.Font("res/pixelart.ttf", 24)
        self.text_surface, self.text_rect = self.retro_font.render("USE LEFT AND RIGHT ARROW KEYS TO TURN!", (255, 255, 255))
        start_sound = pg.mixer.Sound("res/pacman_start.wav")
        self.sound_obj = start_sound.play()

        self.counter = 0
    def on_event(self, e):
        if ((e.type == pg.KEYDOWN) or (e.type == pg.MOUSEBUTTONDOWN)) and self.counter >= 1:
            self.is_transition = True
    def on_update(self, dt, fsm):
        if self.is_transition:
            fsm.transition_to(self.next_state)
        self.counter += dt
    def on_draw(self, screen):
        self.map.draw_map_only(screen)
        screen.blit(self.black_surface, (0, 0))
        if (math.floor(self.counter) % 2 == 0): #TODO replace with Pygame tick
            screen.blit(self.text_surface, (1024/2-self.text_rect.width/2, 768/2-self.text_rect.height/2))
    def on_exit(self):
        self.sound_obj.stop()
        
class LevelEnd(state.Scene):
    def on_start(self, data): # data -> [LevelMap, player_has_died : bool, level_number (if not died), score (if not died)]
        self.map = data[0]
        self.player_has_died = data[1]
        self.level_number = data[2]
        self.score = data[3]
        self.counter = 0
        self.is_transition = False
        
        self.black_surface = pg.Surface((1024, 768))
        self.black_surface.set_alpha(128)
        self.black_surface.fill((0, 0, 0))
        
        self.retro_font = font.Font("res/pixelart.ttf", 24)
        if self.player_has_died:
            self.text_surface, self.text_rect = self.retro_font.render("OH NO, YOU DIED! BETTER LUCK NEXT TIME!", (255, 255, 255))
            sound = pg.mixer.Sound("res/death_sound.wav")
        else:
            self.text_surface, self.text_rect = self.retro_font.render("CONGRATS! YOU WON!", (255, 255, 255))
            sound = pg.mixer.Sound("res/victory_sound.wav")
        self.sound_obj = sound.play()
    def on_event(self, e):
        if ((e.type == pg.KEYDOWN) or (e.type == pg.MOUSEBUTTONDOWN)) and self.counter >= 1:
            self.is_transition = True
    def on_update(self, dt, fsm):
        if self.is_transition:
            if self.player_has_died:
                fsm.transition_to(section_start.StartScreen())
            else:
                fsm.transition_to(CheckHighScore(), [self.level_number, self.score])
        self.counter += dt
    def on_draw(self, screen):
        self.map.draw_map_only(screen)
        screen.blit(self.black_surface, (0,0))
        if (math.floor(self.counter) % 2 == 0): 
            screen.blit(self.text_surface, (1024/2-self.text_rect.width/2, 768/2-self.text_rect.height/2))
    def on_exit(self):
        self.sound_obj.stop()