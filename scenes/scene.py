class Scene:
    def __init__(self):
        self.actions = []
        self.times = []
        self.index = 0
        self.timer = 0

    def add(self, action, time: float):
        """add new frame to scene

        Args:
            action (function(dt: float, game: Game)): action that takes in `dt` and `game` as parameters
            time (float): how long the frame lasts
        """
        self.actions.append(action)
        self.times.append(time)

    def update(self, dt: float, game):
        if self.index >= len(self.actions):
            return
        self.actions[self.index](dt, game, self)
        self.timer += dt
        if self.timer >= self.times[self.index]:
            self.index += 1
            self.timer = 0
