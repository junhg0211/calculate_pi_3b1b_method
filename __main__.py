import pygame

pygame.init()

clock = pygame.time.Clock()


class Const:
    BACKGROUND_COLOR = (31, 33, 37)
    TEXT_COLOR = (222, 222, 222)

    YELLOW = (255, 255, 0)

    COLOR_1 = (192, 109, 48)
    COLOR_2 = (45, 142, 196)


class Text:
    def __init__(self, x: int, y: int, text: str, font_name: str, size: int, color: tuple):
        self.x = x
        self.y = y
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(font_name, size)
        self.surface = self.refresh_surface()

    def set_color(self, color: tuple):
        self.color = color
        self.refresh_surface()
        return self

    def refresh_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        return self.surface

    def set_text(self, text: str):
        self.text = text
        self.refresh_surface()
        return self

    def render(self, surface: pygame.Surface):
        surface.blit(self.surface, (self.x, self.y))


class Box:
    def __init__(self, x: float, color: tuple, mass: float, velocity: float, width: int):
        self.x = x
        self.color = color
        self.mass = mass
        self.velocity = velocity
        self.width = width
        self.text = Text(0, 80, '', 'Consolas', 24, self.color)

    def refresh_text(self):
        self.text.x = self.x
        self.text.set_text(f'{self.velocity:.01f} px/f')
        return self.text

    def collide(self, box):
        self_velocity = ((self.mass - box.mass) * self.velocity + 2 * box.mass * box.velocity) / (self.mass + box.mass)
        box_velocity = (2 * self.mass * self.velocity + (box.mass - self.mass) * box.velocity) / (self.mass + box.mass)

        self.velocity = self_velocity
        box.velocity = box_velocity

    def tick(self):
        self.x += self.velocity
        self.refresh_text()

    def render(self, surface: pygame.Surface):
        # pygame.draw.line(surface, self.color, (self.x, 0), (self.x, Program.HEIGHT))
        pygame.draw.rect(surface, self.color, ((self.x, 100), (self.width, self.width)))
        self.text.render(surface)

    def get_left_x(self):
        return self.x

    def get_right_x(self):
        return self.x + self.width


class Program:
    WIDTH, HEIGHT = 1280, 720

    def __init__(self):
        self.window = pygame.display.set_mode((Program.WIDTH, Program.HEIGHT))
        self.running = False

        self.box1 = Box(Program.WIDTH / 4, Const.COLOR_1, 1, 0, 100)
        self.box2 = Box(Program.WIDTH, Const.COLOR_2, 100 ** 1, -5, 300)

        self.total_collision = 0

        self.collision_count_text = Text(0, Program.HEIGHT - 72, '', 'Consolas', 72, Const.TEXT_COLOR)

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def tick(self):
        for i in range(int(self.box2.mass)):
            break_ = True
            if self.box2.get_left_x() <= self.box1.get_right_x():
                self.box1.collide(self.box2)
                self.total_collision += 1
                break_ = False
            if self.box1.get_left_x() <= 0:
                self.box1.velocity *= -1
                self.total_collision += 1
                break_ = False

            self.box1.tick()
            self.box2.tick()

            if break_:
                break

        self.collision_count_text.set_text(str(self.total_collision))

        if 0 <= self.box1.velocity <= self.box2.velocity:
            self.collision_count_text.set_color(Const.YELLOW)

    def render(self, surface: pygame.Surface):
        surface.fill(Const.BACKGROUND_COLOR)
        self.box1.render(surface)
        self.box2.render(surface)
        self.collision_count_text.render(surface)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle()
            self.tick()
            self.render(self.window)
            clock.tick(60)

    def start(self):
        self.running = True
        self.run()


if __name__ == '__main__':
    program = Program()
    program.start()
