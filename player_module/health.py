class Health:
    def __init__(self, max_health: int):
        self.health = max_health
        self.max_health = max_health
    def heal(self, amount: int = 1):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    def reset(self):
        self.health = self.max_health
    def damage(self, amount: int = 1) -> bool:
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            return True
        return False