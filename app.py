import pygame, json

GAME_DIRECTORY = __file__.replace("app.py", "")

class Sonic:
    def __init__(self):
        self.spritesheet = pygame.image.load(f"{GAME_DIRECTORY}\\assets\\images\\sonic_spritesheet.png")
        with open(f"{GAME_DIRECTORY}\\assets\\data\\sprites.json") as f:
            self.sprites = json.load(f)
        self.animations = {}
        for animation in self.sprites:
            animations = []
            for sprite in self.sprites[animation]:
                coords = sprite[0].split("x")
                size = sprite[1].split("x")
                image = self.spritesheet.subsurface(int(coords[0]), int(coords[1]), int(size[0]), int(size[1]))
                image.set_colorkey((0, 128, 128))
                image = pygame.transform.scale(image, (image.get_width() * 5, image.get_height() * 5))
                animations.append(image)
            self.animations[animation] = animations
        self.x = 50
        self.y = 500
        self.state = "Idle"
        self.current_sprite = 0
        self.speed = [0, 0]
    
    def get_image(self):
        return self.animations[self.state][self.current_sprite - 1]

    def update(self):
        self.current_sprite =+ 1
        if self.current_sprite < len(self.sprites[self.state]) - 1:
            self.current_sprite = 0

        print(self.current_sprite)
        pygame.key.get_pressed()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.speed[0] = -5; self.state = "Running"
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.speed[0] = 5; self.state = "Running"
        else:
            self.speed[0] = 0; self.state = "Idle"

        self.x += self.speed[0]; self.y += self.speed[1]

    def get_renderable(self):
        self.image = self.get_image()
        self.update()
        return self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Supersonic: Turbocharge")
        pygame.display.set_icon(pygame.image.load(f"{GAME_DIRECTORY}\\assets\\images\\icon.ico"))
        self.Clock = pygame.time.Clock()
        self.running = True
        self.renderables = []

        self.sonic = Sonic(); self.renderables.append(self.sonic)

        self.loop()

    def loop(self):

        while self.running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            for renderable in self.renderables:
                self.screen.blit(*renderable.get_renderable())

            self.Clock.tick(60)
            pygame.display.flip()

if __name__ == "__main__":
    Game()