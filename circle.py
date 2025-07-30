import pygame


class Circle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def step(self):
        self.x += self.vx
        self.y += self.vy

    def collision(self, top_bottom: bool = False, left_right: bool = False):
        if top_bottom:
            self.y *= -1
        if left_right:
            self.x *= -1

