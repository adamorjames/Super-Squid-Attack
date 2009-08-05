#!/usr/bin/env python
#
#       enemies.py
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
import random

import pygame
from pygame.locals import *

from utils import *
from const import *
import classes as c1
#import weapons
#import allies




class EnemyShip(c1.AnimSprite):
    def __init__(self, anim, spos, vector, health, speed):
        self._dying = False
        self.speed = speed
        self.health = health
        c1.AnimSprite.__init__(self, anim, spos, vector)
    
    def die(self):
        self.kill()

    def on_hit(self,shot):
        if type(shot) == 'list':
            for i in shot:
                self.health -= i.damage
        #else:
        #    self.health -= shot.damage

    def update(self, ticks):
        c1.AnimSprite.update(self, ticks)


#!!!!!!!!!#####!!!!!!!!!
import copy
            
class Squid(EnemyShip):
    animation = load_anim('images/enemies/squid/squid.anim')
    normal_anim = (animation, [0,0], 0, 0)
    attack_anim = (animation, [0,0], 1, 4, True)

    def __init__(self, spos):
        speed = 4
        health = 50
        vector = [speed,0]
        anim = c1.Animation(*self.normal_anim)
        self.attacking = False
        self.movetimer = Timer(10, self.moveti)
        EnemyShip.__init__(self, anim, spos, vector, health, speed)

    def moveti(self):
        #Watch out for the edges
        if self.rect.right > 600: self.vector[0] = -self.vector[0]
        elif self.rect.left < 0: self.vector[0] = -self.vector[0]
            
        self.moverel(self.vector)
        
    def update(self,ticks):
        EnemyShip.update(self, ticks)
        self.movetimer.update(ticks)

        
        if not self.attacking and random.randint(1, 50) == 5: self.attack()
            
        if self.attacking:
            if self.anim.dead:
                self.attacking = False
                self.switch_anim(c1.Animation(*self.normal_anim))
        
    def attack(self):
        self.attacking = True
        self.switch_anim(c1.Animation(*self.attack_anim))


if __name__ == "__main__":
    print "Testing"
    pygame.init()
    display = pygame.display.set_mode((600,480))
    pygame.display.set_caption("Mouse click!, press a key to exit")
    background, _ = load_image('images/background.png')
    background = background.convert()
    display.blit(background, (0,0))
    pygame.display.flip()
    
    squid = c1.DrawGroup()
    Squid.containers = squid
       
    x = pygame.time.Clock()
    
    while 1:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                Squid(pygame.mouse.get_pos())
            elif event.type == KEYDOWN:
                pygame.quit()
                sys.exit()
        ticks = x.tick(40)
        print ticks
        squid.clear(display, background)
        squid.update(ticks)
        squid.draw(display)
        pygame.display.flip()
