#!/bin/python2
# -*- coding: utf-8

import os
import pygame       # https://pygame.org
import random
import perlin
import xresources
import math

class Fish:
    def __init__(self):
        self.pos = (random.randint(0,width),random.randint(0,height))
        self.maxvel = random.uniform(2,4)
        self.vel = (random.uniform(-self.maxvel,self.maxvel),random.uniform(-self.maxvel,self.maxvel))
        self.acc = (0,0)
        self.c = random.choice(colors[1:])
        self.lines = []
        self.xoff = random.randint(0,10000)
        self.noise = 0
        self.trail_length = random.randint(15,30)
        self.weight = random.uniform(0.5,1.5)

    def update(self):
        self.xoff += 0.1
        self.noise = perlin.noise(self.xoff)
        self.lines.insert(0,self.pos)
        if len(self.lines) > self.trail_length + 30*self.noise: 
            self.lines.pop()
        ax,ay = self.acc
        vx,vy = self.vel
        px,py = self.pos
        vx += ax
        vy += ay
        self.vel = (vx,vy)
        if get_distance((0,0),self.vel) > self.maxvel + 2*self.noise:
            self.vel = lendir((0,0),get_direction((0,0),self.vel),self.maxvel)
            vx,vy = self.vel
        px += vx
        py += vy
        if px < 0: px = width
        if py < 0: py = height
        if px > width: px = 0
        if py > height: py = 0
        self.pos = (px,py)
        self.acc = (0,0)

    def apply_force(self,force):
        ax,ay = self.acc
        fx,fy = force
        self.acc = (ax+fx,ay+fy)

    def draw(self):
        i = 0
        while i < len(self.lines)-1:
            if i < len(self.lines)/2:
                weight = i
            else:
                weight = -i + len(self.lines)
            weight *= self.weight
            weight += 4*self.noise
            x1,y1 = self.lines[i]
            x2,y2 = self.lines[i+1]
            i += 1
            if get_distance((x1,y1),(x2,y2)) <= self.maxvel * 2:
                pygame.draw.line(screen, self.c, (int(x1),int(y1)),(int(x2),int(y2)),int(weight))
    
    def swim(self,grid):
        x,y = self.pos
        x = int(x/scale)
        y = int(y/scale)
        i = x + (y-1) * col
        try:
            force = lendir((0,0),grid[i],strength)
            self.apply_force(force)
        except IndexError:
            pass

def lendir(begin,direction,length):
    bx,by = begin
    x = bx + math.cos(math.radians(direction)) * length
    y = by + math.sin(math.radians(direction)) * length
    return (x,y)

def get_direction(p1, p2):
    p1x,p1y = p1
    p2x,p2y = p2
    deltaY = float(p2y) - float(p1y)
    deltaX = float(p2x) - float(p1x)
    direction = math.degrees(math.atan2(float(deltaY), float(deltaX)))
    return direction

def get_distance(p1,p2):
    p1x,p1y = p1
    p2x,p2y = p2
    dx = p1x - p2x
    dy = p1y - p2y
    if dx < 0: dx *= -1
    if dy < 0: dy *= -1
    return (dx+dy)/2

colors = []
for color in xresources.colors:
    colors.append(pygame.Color(color))

inc = 0.2
size = width, height = 600, 600
scale = height/20
col = width/scale
row = height/scale
grid = []
strength = 0.5
for i in range(0,col*row):
    grid.append(0)

pygame.init()
pygame.display.set_caption("fish")
screen = pygame.display.set_mode(size)
running = True

zoff = 0
fish = []
for i in range(0,len(colors)):
    fish.append(Fish())
    fish[i].c = colors[i]

while running:
    screen.fill(colors[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    yoff = 0
    for y in range(1,width,scale):
        xoff = 0
        for x in range(1,height,scale):
            i = x/scale + (y/scale) * col
            c = int(len(colors)*perlin.noise(xoff,yoff,zoff))
            direction = (2*360)*perlin.noise(xoff,yoff,zoff)
            grid[i] = direction
            xoff += inc
        yoff += inc
    zoff += inc/10
    for f in fish:
        f.update()
        f.swim(grid)
        f.draw()
    pygame.display.flip()
