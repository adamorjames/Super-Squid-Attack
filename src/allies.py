#!/usr/bin/env python
#
#       allies.py
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



import pygame
from pygame.locals import *

import os
import sys
import random

import classes as c1
from const import *
from utils import *
import weapons


class PlayerShip(c1.AnimSprite):
    def __init__(self, anim, spos, vector, health, shield, speed):
        """A base class for a PlayerShip
        spos: the starting position. eg. [30,50]
        anim: an Animation object which will be used as the image
        health: integer value for health
        shield: integer value for shield
        speed: the speed the ship can move at
        vector: an initial movement vector"""
        
        #The speed we can go
        self.speed = speed
        #health & shields
        self.health = health
        self.shield = shield

        c1.AnimSprite.__init__(self, anim, spos, vector)
        
    def start_moving(self, dir):
        """Change direction of ship movement.
        Uses const modules constants UP,DOWN,LEFT, and RIGHT"""
        if dir == UP: self.vector[1] = -self.speed
        elif dir == DOWN: self.vector[1] = self.speed
        elif dir == RIGHT: self.vector[0] = self.speed
        elif dir == LEFT: self.vector[0] = -self.speed
        
    def stop_moving(self, dir):
        #Stop movement in dir
        if dir == UP: self.vector[1] = 0
        elif dir == DOWN: self.vector[1] = 0
        elif dir == RIGHT: self.vector[0] = 0
        elif dir == LEFT: self.vector[0] = 0
        
    def update(self,ticks):
        c1.AnimSprite.update(self, ticks)
        
        #Move self and change animation position accordingly
        self.rect.move_ip(self.vector)
        self.anim.move(self.rect.topleft)

        
class BlackEagle(PlayerShip):
    normal = (load_anim('images/BlackEagle/ship.anim'), [0,0])
    #exploding = (load_anim('images/BlackEagle/explode.anim'),[0,0])
    
    def __init__(self, spos):
        self.weapons = [weapons.RedLaser, weapons.GreenLaser, weapons.Rocket]
        self.active = 0
        anim = c1.Animation(*self.normal)
        anim.move(spos)
        vector = [0,0]
        speed = 4
        health = 99
        shield = 99
        
        PlayerShip.__init__(self, anim, spos, vector, health, shield, speed)

    def die(self):
        if self.anim.dead: self.kill()
        elif self.anim.onceoff == True: pass
        else:
            self.switch_anim(self.exploding)
            self.vector = [0,0]

    def fire(self):
        self.weapons[self.active]((self.rect.centerx,self.rect.centery))


if __name__ == "__main__":
    print "Testing"
    pygame.init()
    display = pygame.display.set_mode((600,480))
    background, _ = load_image('images/background.png')
    display.blit(background, (0,0))
    pygame.display.flip()
    
    ship = BlackEagle([100,0])
    dg = c1.DrawGroup(ship)
    weapons.Weapon.containers = dg
    x = pygame.time.Clock()
    
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT: sys.exit()
            #Keyboard events
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: ship.die()
                elif event.key == K_LEFT: ship.start_moving(LEFT)
                elif event.key == K_RIGHT: ship.start_moving(RIGHT)
                elif event.key == K_UP: ship.start_moving(UP)
                elif event.key == K_DOWN: ship.start_moving(DOWN)
                elif event.key == K_SPACE: ship.fire()
            elif event.type == KEYUP:
                if event.key == K_LEFT: ship.stop_moving(LEFT)
                elif event.key == K_RIGHT: ship.stop_moving(RIGHT)
                elif event.key == K_UP: ship.stop_moving(UP)
                elif event.key == K_DOWN: ship.stop_moving(DOWN)
                
        ticks = x.tick(40)
        dg.clear(display, background)
        dg.update(ticks)
        dg.draw(display)
        pygame.display.flip()
