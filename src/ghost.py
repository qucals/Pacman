import game_object


class Ghost(game_object.GameObject):
    def __init__(self, name, pictures):
        super().__init__()

        # Pictures of the ghost
        self.pictures = pictures
        
        # Name of the ghost
        self.name = name

        self.isAlive = True
        self.isKill = False

    def draw(self):
        super().draw()
