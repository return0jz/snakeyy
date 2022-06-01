import state
import pygame as pg
import pygame_gui as pg_gui
import math

from section_levels import Level1, Level2, Level3, Level4
from section_ui import LevelPreview

class StartScreen(state.Scene):
    def on_start(self, data):
        self.stopwatch = 0
        self.menu1 = pg.transform.scale(pg.image.load("res/menu1.png"), (1024, 768))
        self.menu2 = pg.transform.scale(pg.image.load("res/menu2.png"), (1024, 768))
        self.gui = pg_gui.UIManager((1024, 768), 'theme.json')
        self.level1 = pg_gui.elements.UIButton(relative_rect=pg.Rect((230, 600), (100, 50)), text='LEVEL1', manager=self.gui)
        self.level2 = pg_gui.elements.UIButton(relative_rect=pg.Rect((380, 600), (100, 50)), text='LEVEL2', manager=self.gui)
        self.level3 = pg_gui.elements.UIButton(relative_rect=pg.Rect((530, 600), (100, 50)), text='LEVEL3', manager=self.gui)
        self.level4 = pg_gui.elements.UIButton(relative_rect=pg.Rect((680, 600), (100, 50)), text='LEVEL4', manager=self.gui)
        self.next_data = None
        pg.mixer.music.load("res/menutheme.mp3")
        pg.mixer.music.play(-1)
    def on_event(self, e):
        if e.type == pg_gui.UI_BUTTON_PRESSED:
            if e.ui_element == self.level1:
                self.next_data = ("level1.txt", Level1())
            if e.ui_element == self.level2:
                self.next_data = ("level2.txt", Level2())
            if e.ui_element == self.level3:
                self.next_data = ("level3.txt", Level3())
            if e.ui_element == self.level4:
                self.next_data = ("level4.txt", Level4())
        self.gui.process_events(e)
    def on_update(self, dt, fsm):
        if self.next_data:
            fsm.transition_to(LevelPreview(), self.next_data)
        self.gui.update(dt)
        self.stopwatch += dt
    def on_draw(self, screen):
        if math.floor(self.stopwatch*1.8) % 2 == 0:
            screen.blit(self.menu1, (0,0))
        else:
            screen.blit(self.menu2, (0,0))
        self.gui.draw_ui(screen)
    def on_exit(self):
        pg.mixer.music.stop()