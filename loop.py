import pygame as pg
import pygame_menu as pg_menu
import state
import section_start

class Mainloop:
    def __init__(self):
        self.fsm = state.SceneManager(section_start.StartScreen())
    def handle_event(self, e):
        self.fsm.handle_event(e)
    def handle_event_q(self, q):
        self.fsm.handle_event_q(q)
    def update(self, dt):
        self.fsm.update(dt)
    def draw(self, screen):
        self.fsm.draw(screen)
        pass
