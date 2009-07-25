#!/usr/bin/env python
#
#       classes.py
#       
#       Copyright 2009 Unknown <xavieran@Le-Chateau>
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


import time
import os
import sys

import pygame
from pygame.locals import *

from utils import Timer
from const import *

class Background(pygame.sprite.Sprite):
    '''Scrolling Background'''
    def __init__(self,image,speed):
        self.speed=speed
        self.image=pygame.image.load(image)
        self.rect=self.image.get_rect()
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        self.rect=self.rect.move((0,self.speed))




class Ship(pygame.sprite.Sprite):
    def __init__(self,spos,health,vector):
        self.rect=self.image.get_rect()
        self.rect.topleft=spos
        self.health=health
        self.vector=vector
        pygame.sprite.Sprite.__init__(self)
        
    def move(self,dir):
        self.rect=self.rect.move(dir)
        
    def on_hit(self,weapon):
        self.health-=weapon.damage
        if self.health <= 0:
            self.die()
        else:
            pass
            #self.bullet_hit_anim()
            
    def die(self):
        self.kill()
    
def within(x,y,z):
    if y < x < z:
        return True
    return False
    
class HealthBar(pygame.sprite.Sprite):
    images={}
    [images.__setitem__(i,pygame.image.load('images/interface/health/%d.png'%i)) for i in [100,80,60,40,20,10]]
    
    def __init__(self,spos):
        self.image=self.images[100]
        self.rect=self.image.get_rect()
        self.rect.topleft=spos
        pygame.sprite.Sprite.__init__(self)
        
    def update_life(self,health):
        if within(health,81,100):self.image=self.images[100]
        elif within(health,61,80):self.image=self.images[80]
        elif within(health,41,60):self.image=self.images[60]
        elif within(health,21,40):self.image=self.images[40]
        elif within(health,11,20):self.image=self.images[20]
        else:self.image=self.images[10]




if __name__ == "__main__":print "TEST"
