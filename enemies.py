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

#Comes from:http://eli.thegreenplace.net/2009/02/13/writing-a-game-in-py
#thon-with-pygame-part-iv/
#Thanks to Eli Bendersky for the code
from utils import Timer

import classes as c1
from const import *
import weapons
import allies

pygame.init()



class EnemyShip(c1.Ship):
    def __init__(self,spos,health,speed,vector):
        self._dying = False
        self.speed=speed
        c1.Ship.__init__(self,spos,health,vector)
    
    def die(self):
        self.kill()
        
    def update(self):
        self.rect=self.rect.move(self.vector)
        #Watch out for the edges
        if self.rect.right > 800:self.vector[0]=-self.vector[0]
        elif self.rect.left < 0:self.vector[0]=-self.vector[0]
            
            
class Squid(EnemyShip):
    normimage=pygame.image.load('images/enemies/squid/squid.png')
    image=normimage
    attack_imgs=[pygame.image.load('images/enemies/squid/squid_attack%d.png'%i) for i in range(1,5)]
    def __init__(self,spos):
        speed=4
        health=50
        vector=[speed,0]
        self._attacking=False
        self._anim_index=0
        self.timer=Timer(20,self.change_anim)
        EnemyShip.__init__(self,spos,health,speed,vector)
        
    def update(self):
        self.rect=self.rect.move(self.vector)
        if self.rect.right > 800:self.vector[0]=-self.vector[0]
        elif self.rect.left < 0:self.vector[0]=-self.vector[0]
        if random.randint(1,15) == 5:
            self.attack()
        self.timer.update(6)
        
    def change_anim(self):
        if not self._attacking:return
        if self._anim_index > len(self.attack_imgs)-1:
            self._attacking=False
            self.image=self.normimage
            self._anim_index=0
        else:
            position=self.rect.topleft
            self.image=self.attack_imgs[self._anim_index]
            self.rect=self.image.get_rect()
            self.rect.topleft=position
            self._anim_index+=1

    def attack(self):
        self._attacking=True
        
class Button(EnemyShip):
    images=[pygame.image.load('images/enemies/buttons/button_ON_anim%d.png'%i) for i in range(0,13)]
    bomb_images=[pygame.image.load('images/explosions/explosion_BOMB_animation_%s.png'%str(i).zfill(4)) for i in range(0,30)]
    def __init__(self,spos):
        self.index=0
        self.image=self.images[self.index]
        self.dir=UP
        speed=3
        self.timer=Timer(20,self.change_anim)
        health=1
        vector=[speed,0]
        EnemyShip.__init__(self,spos,health,speed,vector)
        
    def change_anim(self):
        if self.dir == UP:
            if self.index > len(self.images)-2:
                if self._dying:self.kill()
                self.dir=DOWN
                self.index-=1
            else:self.index+=1
            
        else:
            self.index-=1
            if self.index < 0:
                self.index=0
                self.dir = UP
                
    def die(self):
        self.images=self.bomb_images
        self.vector[0]=0
        self.index=0
        self._dying=1

    def update(self,ticks=8):
        self.rect=self.rect.move(self.vector)
        if self.rect.right > 800:
            self.vector[0]=-self.vector[0]
        if self.rect.left < 0:
            self.vector[0]=-self.vector[0]
        self.timer.update(ticks)
        self.image=self.images[self.index]
