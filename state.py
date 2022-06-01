class SceneManager:
    def __init__(self, first_state):
        self.current_state = first_state
        self.current_state.on_start([])
    def transition_to(self, state, data=[]):
        self.current_state.on_exit()
        self.current_state = state
        self.current_state.on_start(data)
    def update(self, dt):
        self.current_state.on_update(dt, self)
    def handle_event(self, e):
        self.current_state.on_event(e)
    def handle_event_q(self, e):
        self.current_state.on_event_q(e)
    def draw(self, screen):
        self.current_state.on_draw(screen)
    
class Scene(object): # interface
    def on_start(self, data):
        pass
    def on_event(self, e):
        pass
    def on_event_q(self, q):
        pass
    def on_update(self, dt, fsm):
        pass
    def on_draw(self, screen):
        pass
    def on_exit(self):
        pass
    