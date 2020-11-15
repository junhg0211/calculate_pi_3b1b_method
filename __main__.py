from math import sqrt

import pygame

pygame.init()

clock = pygame.time.Clock()


class Const:
    BACKGROUND_COLOR = (31, 33, 37)
    TEXT_COLOR = (222, 222, 222)

    COLOR_1 = (192, 109, 48)
    COLOR_2 = (45, 142, 196)


class Box:
    def __init__(self, x: float, color: tuple, mass: float, velocity: float):
        self.x = x
        self.color = color
        self.mass = mass
        self.velocity = velocity

    def collide(self, box):
        self_velocity = ((self.mass - box.mass) * self.velocity + 2 * box.mass * box.velocity) / (self.mass + box.mass)
        box_velocity = (2 * self.mass * self.velocity + (box.mass - self.mass) * box.velocity) / (self.mass + box.mass)

        self.velocity = self_velocity
        box.velocity = box_velocity

    def tick(self):
        self.x += self.velocity

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, self.color, (self.x, 0), (self.x, Program.HEIGHT))


class Program:
    WIDTH, HEIGHT = 1280, 720

    def __init__(self):
        self.window = pygame.display.set_mode((Program.WIDTH, Program.HEIGHT))
        self.running = False

        self.box1 = Box(Program.WIDTH / 4, Const.COLOR_1, 1, 0)
        self.box2 = Box(Program.WIDTH, Const.COLOR_2, 100 ** 6, -10)

        self.total_collision = 0

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def tick(self):
        for _ in range(int(sqrt(self.box2.mass) / 10)):
            break_ = True
            if self.box2.x <= self.box1.x:
                self.box1.collide(self.box2)
                self.total_collision += 1
                break_ = False
            if self.box1.x <= 0:
                self.box1.velocity *= -1
                self.total_collision += 1
                break_ = False

            self.box1.tick()
            self.box2.tick()

            if break_:
                break

        print(self.total_collision)

    def render(self, surface: pygame.Surface):
        surface.fill(Const.BACKGROUND_COLOR)
        self.box1.render(surface)
        self.box2.render(surface)
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
