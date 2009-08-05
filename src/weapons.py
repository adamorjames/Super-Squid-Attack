#!/usr/bin/env python
#
#       weapons.py
#       
#       Copyright 2009 Emmanuel Jacyna <xavieran@Le-Chateau>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import os
import sys

import pygame
from pygame.locals import *

import classes as c1
from utils import *
from const import *

class Weapon(c1.SimpleSprite):
    '''Our generic weapon class'''
    def __init__(self, spos, vector, damage):
        self.damage = damage
        self.dirty = 1
        c1.SimpleSprite.__init__(self, spos, vector)
        
    def update(self, ticks):
        self.rect.move_ip(self.vector)
        if self.rect.top < 0: self.kill()

    def die(self):
        self.kill()

    def kill(self):
        #Do something fancy in here, for the weapon type,
        #ie, eject some sparkles, and then call.
        c1.SimpleSprite.kill(self)


class RedLaser(Weapon):
    type = LASER
    refire = 20
    def __init__(self, spos):
        self.image, self.rect = load_image('images/weapons/laser_red.png')
        self.drawrect = self.rect.move([0,0])
        damage = .5
        self.speed = 8
        vector = [0,-self.speed]
        Weapon.__init__(self, spos, vector, damage)

class GreenLaser(Weapon):
    type = LASER
    refire = 30
    def __init__(self, spos):
        self.image, self.rect = load_image('images/weapons/laser_green.png')
        self.drawrect = self.rect.move([0,0])
        damage = 1
        self.speed = 8
        vector = [0,-self.speed]
        Weapon.__init__(self, spos, vector, damage)


class Rocket(Weapon):

    type = ROCKET
    refire = 100
    def __init__(self, spos):
        self.image, self.rect = load_image('images/weapons/rocket.png')
        self.drawrect = self.rect.move([0,0])
        damage = 20
        speed = -3
        vector = [0,speed]
        Weapon.__init__(self, spos, vector, damage)
        
        
class GuidedRocket(Weapon):
    type = ROCKET
    refire = 100
    def __init__(self, spos):
        self.image, self.rect = load_image('images/weapons/guided_rocket.png')
        self.drawrect = self.rect.move([0,0])
        self.speed = 2
        damage = .5
        vector = [0,0]
        Weapon.__init__(self, spos, vector, damage)
    
    def navigate(self):
        vector = [0,0]
        centerx, centery = pygame.mouse.get_pos()
        if not centerx - 5 > self.rect.centerx > centerx + 5:
            #If it is right of the target, go left
            if self.rect.centerx > centerx:
                vector[0] = -self.speed
            #If it is left of the target, go right
            elif self.rect.centery < centerx:
                vector[0] = self.speed
                
        if not centery - 5 > self.rect.centery > centery + 5:
            #If it is below the target, go up
            if self.rect.centery < centery:
                vector[1] = self.speed
            #If it is above the target, go down
            elif self.rect.centery > centery:
                vector[1] = -self.speed
        
        return vector
            
    def update(self, ticks):
        Weapon.update(self, ticks)
        self.vector = self.navigate()
 
if __name__=='__main__':
                
    #Initialize the display and background
    pygame.init()
    display = pygame.display.set_mode((400,400))
    pygame.display.set_caption("TAB to change weapon, click to fire")
    background, _ = load_image('images/background.png')
    pos = [0,0]
    pygame.display.flip()

    #Set the group to be drawn, and set this as the default
    #container for the Weapon class.
    shots = c1.DrawGroup()
    Weapon.containers = shots
    #Instantiate a list of weapons
    guns = [RedLaser, GreenLaser, Rocket, GuidedRocket]
    gun = 0
    
    #Start the clock
    x = pygame.time.Clock()
    
    while 1:
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()
            elif i.type == MOUSEBUTTONDOWN:
                guns[gun](pygame.mouse.get_pos())
            elif i.type == KEYDOWN:
                if i.key == K_TAB:
                    gun = (gun+1)%(len(guns))
                    print gun
                
        ticks = x.tick(50)
        #shots.clear(display, background)
        display.blit(background, pos)
        shots.update(ticks)
        shots.draw(display)
        pos[1]-=2
        pygame.display.flip()
