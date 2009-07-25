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



import pygame
from pygame.locals import *
import time
import os
import sys

import classes as c1
from const import *

class Weapon(pygame.sprite.Sprite):
    '''Our generic weapon class'''
    def __init__(self,spos,image,speed,refire,damage):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=spos
        self.speed=speed
        self.refire=refire
        self.damage=damage
        pygame.sprite.Sprite.__init__(self)
        
    def update(self):
        self.rect=self.rect.move((0,self.speed))
        if self.rect.top < 0:self.kill()

    def die(self):
        self.kill()

class Red_Laser(Weapon):
    image=pygame.image.load('images/weapons/laser_red.png')
    type=LASER
    refire=20
    def __init__(self,spos,speed = -10):
        damage=.5
        #refire=20
        Weapon.__init__(self,spos,self.image,speed,self.refire,damage)
        
class Green_Laser(Weapon):
    image=pygame.image.load('images/weapons/laser_green.png')
    type=LASER
    refire=30
    def __init__(self,spos,speed = -10):
        damage=1
        #refire=30
        Weapon.__init__(self,spos,self.image,speed,self.refire,damage)

class Blue_Laser(Weapon):
    image=pygame.image.load('images/weapons/laser_blue.png')
    type=LASER
    refire=40
    def __init__(self,spos,speed = -10):
        damage=1.5
        #refire=40
        Weapon.__init__(self,spos,self.image,speed,self.refire,damage)
        
class Purple_Laser(Weapon):
    image=pygame.image.load('images/weapons/laser_purple.png')
    type=LASER
    refire=70
    def __init__(self,spos,speed = -10):
        damage=2
        #refire=50
        Weapon.__init__(self,spos,self.image,speed,self.refire,damage)

class Rocket(Weapon):
    image=pygame.image.load('images/weapons/missile.png')
    type=ROCKET
    refire=100
    def __init__(self,spos,speed=-5):
        damage=10
        #refire=100
        Weapon.__init__(self,spos,self.image,speed,self.refire,damage)


class GuidedRocket(Weapon):
    image=pygame.image.load('images/weapons/guided_missile.png')
    type=GUIDED_ROCKET
    refire=50
    def __init__(self,spos,target,speed=2):
        damage=10
        self.vector=[0,0]
        self.target=target
        Weapon.__init__(self,spos,self.image,speed,self.refire,damage)
    
    def navigate(self):
        vector=[0,0]
        #if not self.target.centerx-5 > self.rect.centerx > self.target.centerx+5:
            ##If it is right of the target, go left
            #if self.rect.centerx > self.target.rect.centerx:
                #vector[0]=-self.speed
            ##If it is left of the target, go right
            #elif self.rect.centery < self.target.rect.centerx:
                #vector[0]=self.speed
                
        #if not self.target.centery-5 > self.rect.centery > self.target.centery+5:
            ##If it is below the target, go up
            #if self.rect.centery < self.target.rect.centery:
                #vector[1]=self.speed
            ##If it is above the target, go down
            #elif self.rect.centery > self.target.rect.centery:
                #vector[1]=-self.speed
        centerx,centery=pygame.mouse.get_pos()
        if not centerx-5 > self.rect.centerx > centerx+5:
            #If it is right of the target, go left
            if self.rect.centerx > centerx:
                vector[0]=-self.speed
            #If it is left of the target, go right
            elif self.rect.centery < centerx:
                vector[0]=self.speed
                
        if not centery-5 > self.rect.centery > centery+5:
            #If it is below the target, go up
            if self.rect.centery < centery:
                vector[1]=self.speed
            #If it is above the target, go down
            elif self.rect.centery > centery:
                vector[1]=-self.speed
        
        return vector
            
    def update(self):
        self.vector=self.navigate()
        self.rect=self.rect.move(self.vector)
        if self.rect.top < 0:self.kill()
 
