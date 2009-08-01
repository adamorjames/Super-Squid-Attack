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
import weapons
import allies

pygame.init()



class EnemyShip(c1.MySprite):
    def __init__(self,anim,spos,vector,health,speed):
        self._dying = False
        self.speed=speed
        c1.MySprite.__init__(self,anim,spos,vector)
    
    def die(self):
        self.kill()
        
    def update(self,ticks):
        c1.MySprite.update(self,ticks)
            
            
class Squid(EnemyShip):
    image,rect=load_image('images/enemies/squid/squid.png')
    normal=c1.Animation(image,rect,57,10000,[0,0])
    image,rect=load_image('images/enemies/squid/squid-attack.png')
    attack_anim=(image,rect,57,100,[0,0],False,True)

    def __init__(self,spos):
        speed=4
        health=50
        vector=[speed,0]
        anim=self.normal
        self.attacking=False
        EnemyShip.__init__(self,anim,spos,vector,health,speed,)

    def update(self,ticks):
        EnemyShip.update(self,ticks)
        self.moverel(self.vector)
        
        #Watch out for the edges
        if self.rect.right > 480:self.vector[0]=-self.vector[0]
        elif self.rect.left < 0:self.vector[0]=-self.vector[0]
        
        if not self.attacking and random.randint(1,30) == 5:
            self.attack()
            
        if self.attacking:
            if self.anim.dead:
                self.attacking=False
                self.switch_anim(self.normal)
        
    def attack(self):
        self.attacking=True
        self.switch_anim(c1.Animation(*self.attack_anim))
        


if __name__ == "__main__":
    print "Testing"
    pygame.init()
    display=pygame.display.set_mode((600,200))
    background,_=load_image('images/background.png')
    background=background.convert()
    display.blit(background,(0,0))
    pygame.display.flip()
    
    dg=c1.DrawGroup()
    baddies=Squid([0,0])
    baddies.add(dg)
    baddies.normal.image=baddies.normal.image.convert_alpha()
        
    x=pygame.time.Clock()
    
    while 1:
        pygame.event.pump()
        ticks=x.tick(40)
        print ticks
        dg.clear(display,background)
        dg.update(ticks)
        dg.draw(display)
        pygame.display.flip()
