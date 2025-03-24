from pygame import *
from settings import *
from entities.entity import Entity

class Persistent_entities(Entity):

    def __init__(self, game, rect: Rect, lifespan: float, update_after_ticks: float):
        super().__init__(rect)
        self.lifespan = lifespan
        self.update_after_ticks = update_after_ticks
        self.hitable_entities = []
        self.count_ticks = 0

    
    def update(self, dt: float, game):
        #super().update(dt, game)
        if self.count_ticks % self.update_after_ticks == 0 and not (self.update_after_ticks == -1):
            for entity in game.entities:
                if(entity.body):
                    self.hitable_entities.append(entity)

        for entity in self.hitable_entities:
            if entity.body:
                if self.rect.colliderect(entity):
                    entity.damage(game, entity)
                    self.hitable_entities.remove(entity)

        if self.count_ticks >= 1000:
            self.destroy(game)
        
        self.count_ticks +=1
        
        
    def draw(self, screen, camera):
        pass