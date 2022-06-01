import pygame as pg
import pygame.freetype
from loop import Mainloop

def main():
    pg.init()
    pg.mixer.init()
    pg.font.init()
    pg.display.set_caption("GAME")
    screen = pg.display.set_mode((1024, 768))
    clock = pg.time.Clock()
    
    loop = Mainloop()
    running = True
    while running:
        dt = clock.tick()/1000
        event_queue = pg.event.get()
        for event in event_queue:
            if event.type == pg.QUIT:
                running = False 
            loop.handle_event(event)
        loop.handle_event_q(event_queue)
        loop.update(dt)
        screen.fill((0, 0, 0))
        loop.draw(screen)
        pg.display.flip()
    pg.quit()
                
if __name__ == "__main__":
    main()