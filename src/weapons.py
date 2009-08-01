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
from utils import *
from const import *

class Weapon(c1.MySprite):
    '''Our generic weapon class'''
    def __init__(self,spos,anim,vector,damage):
        self.speed=speed
        self.vector=vector
        self.damage=damage
        
        c1.MySprite.__init__(self,spos,anim,vector)
        
    def update(self):
        self.rect.move_ip(self.vector)
        if self.rect.top < 0:self.kill()

    def die(self):
        self.kill()


class Red_Laser(Weapon):
    image,rect=load_image('images/weapons/laser_red.png')
    normal=c1.Animation(image,rect,0,10000,[0,0])
    type=LASER
    #Refire needs to be a class attribute because it needs to be
    #used before the Weapon is instantiated...
    refire=20
    def __init__(self,spos,speed=-10):
        damage=.5
        anim=self.normal
        anim.move(spos)
        vector=[0,speed]
        Weapon.__init__(self,spos,anim,vector,damage)


class Green_Laser(Weapon):
    image,rect=load_image('images/weapons/laser_green.png')
    normal=c1.Animation(image,rect,0,10000,[0,0])
    type=LASER
    #Refire needs to be a class attribute because it needs to be
    #used before the Weapon is instantiated...
    refire=30
    def __init__(self,spos,speed=-10):
        damage=1
        anim=self.normal
        anim.move(spos)
        vector=[0,speed]
        Weapon.__init__(self,spos,anim,vector,damage)


class Rocket(Weapon):
    image,rect=load_image('images/weapons/rocket.png')
    normal=c1.Animation(image,rect,0,10000,[0,0])
    type=ROCKET
    #Refire needs to be a class attribute because it needs to be
    #used before the Weapon is instantiated...
    refire=100
    def __init__(self,spos,speed=-3):
        damage=20
        anim=self.normal
        anim.move(spos)
        vector=[0,speed]
        Weapon.__init__(self,spos,anim,vector,damage)
        
        
class GuidedRocket(Weapon):
    image,rect=load_image('images/weapons/guided_rocket.png')
    normal=c1.Animation(image,rect,0,10000,[0,0])
    type=ROCKET
    #Refire needs to be a class attribute because it needs to be
    #used before the Weapon is instantiated...
    refire=100
    def __init__(self,spos,speed=-10):
        damage=.5
        anim=self.normal
        anim.move(spos)
        vector=[0,speed]
        Weapon.__init__(self,spos,anim,vector,damage)
    
    def navigate(self):
        vector=[0,0]
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
            
    def update(self,ticks):
        Weapon.update(self,ticks)

        self.vector=self.navigate()
 
if __name__=='__main__':pass
