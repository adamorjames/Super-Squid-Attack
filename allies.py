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
import time
import os
import sys
import random

import classes as c1
import weapons
from const import *

from utils import Timer


class PlayerShip(c1.Ship):
    def __init__(self,spos,health,speed,weapons,mountpoints,enemies,shots,shotg,drawg):
        self.enemies=enemies
        self.target=0
        self.shots=shots
        self.drawg=drawg
        self.shotg=shotg
        #The speed the ship can move
        self.speed=speed
        #We need this for self.fire() to know where to shoot the 
        #projectiles from. It is a dictionary that looks like this:
        #{'laser_top':15,'laser_left':-13,'laser_right':-13,\
        #'bomb_drop':[50,15]}
        #Laser top is the "y" value for where the lasers should come from
        self.mountpoints=mountpoints
        #The weapons we can fire
        self.weapons=weapons
        #Index in self.weapons of the (surprise) currently
        #active weapon
        self.active_weapon=0
        #strobe
        self._strobe=0
        #Store what projectiles we've fired
        #The game uses this to test for collisions 
        self.image=self.images['image']
        self.timers={'refire':Timer(200,self.fireable),'strobe':Timer(200,self.strobe)}
        #These will be used later
        self.dying = False
        self.rotations=0
        self.can_fire=True
        c1.Ship.__init__(self,spos,health,[0,0])
        

    def on_hit(self):
        if self.health <= 0:
            self.dying = True
        else:
            self.health-=1
            
    def fireable(self):
        """Make self.can_fire = True"""
        self.can_fire=True
        
    def strobe(self):
        if self._strobe:
            self.image=self.images['image']
            self._strobe=0
        else:
            self.image=self.images['strobe']
            self._strobe=1

    def fire(self):
        if not self.can_fire:return
        
        weapon=self.weapons[self.active_weapon]
        mp=self.mountpoints
        if weapon.type == LASER:
            #The left laser:
            self.shots.append(weapon(\
            (self.rect.left+mp['laser_left'],self.rect.top+mp['laser_top']-weapon.image.get_rect().bottom)))
            #Add to our projectiles_group
            self.shots[-1].add(self.shotg)
            self.shots[-1].add(self.drawg)
            #The right laser:
            self.shots.append(weapon(\
            (self.rect.left+mp['laser_right'],self.rect.top+mp['laser_top']-weapon.image.get_rect().bottom)))
            self.shots[-1].add(self.shotg)
            self.shots[-1].add(self.drawg)
        #A little different for a rocket
        elif weapon.type == ROCKET:
            self.shots.append(weapon(\
            (self.rect.left+mp['bomb_mid'],self.rect.top+mp['bomb_top'])))
            self.shots[-1].add(self.shotg)
            self.shots[-1].add(self.drawg)
        elif weapon.type == GUIDED_ROCKET:
            self.shots.append(weapon(\
            (self.rect.left+mp['bomb_mid'],self.rect.top+mp['bomb_top']),\
            self.enemies[self.target]))
            self.shots[-1].add(self.shotg)
            self.shots[-1].add(self.drawg)
        self.can_fire=False

    def next_weapon(self):
        self.active_weapon=(self.active_weapon+1)%len(self.weapons)
        self.timers['refire'].change_interval(self.weapons[self.active_weapon].refire)
        
    def next_target(self):
        self.target=(self.target+1)%len(self.enemies)

    def start_moving(self,dir):
        if dir == UP:
            self.vector[1]=-self.speed
            #self.image = self.mu_image
        elif dir == DOWN:
            self.vector[1]=self.speed
           # self.image = self.images['move_up']
        elif dir == RIGHT:
            self.vector[0]=self.speed
           # self.image = self.images['move_right']
        elif dir == LEFT:
            self.vector[0]=-self.speed
           # self.image = self.images['move_left']
        
    def stop_moving(self,dir):
        if dir == UP:self.vector[1]=0
        elif dir == DOWN:self.vector[1]=0
        elif dir == RIGHT:self.vector[0]=0
        elif dir == LEFT:self.vector[0]=0
        self.image = self.images['image']
        
    def update(self,time=5):
        for timer in self.timers.values():
            timer.update(time)
        self.rect=self.rect.move(self.vector)
        if self.dying:
            if self.rotations == 8:
                self.kill()
            else:
                self.image=pygame.transform.rotate(self.image,35)
                self.rotations+=1



class BlueFalcon(PlayerShip):
    images={'image':pygame.image.load('images/BlueFalcon/ship.png'),\
    'strobe':pygame.image.load('images/BlueFalcon/ship_strobe.png')}

    def __init__(self,spos,enemies,shots,shotg,drawg):
        speed=6
        health=99
        mountpoints={'laser_top':22,'laser_left':6,'laser_right':49,'bomb_top':-20,'bomb_mid':21}
        guns=[weapons.Rocket,weapons.Red_Laser,weapons.Blue_Laser]
        PlayerShip.__init__(self,spos,health,speed,guns,mountpoints,enemies,shots,shotg,drawg)
        self.vector=[2,0]
        
        
    def update(self,time=5):
        for timer in self.timers.values():
            timer.update(time)
        self.rect=self.rect.move(self.vector)
        if self.dying:
            if self.rotations == 8:
                self.kill()
            else:
                self.image=pygame.transform.rotate(self.image,35)
                self.rotations+=1
                
        if random.randint(1,30)==5:self.fire()
        if random.randint(1,50) == 5:self.next_weapon()
        if self.rect.right > 800:
            self.vector[0]=-self.vector[0]
        if self.rect.left < 0:
            self.vector[0]=-self.vector[0]
            

class BlackEagle(PlayerShip):
    images={'image':pygame.image.load('images/BlackEagle/ship.png'),\
    'strobe':pygame.image.load('images/BlackEagle/ship_strobe.png')}
    
    def __init__(self,spos,enemies,shots,shotg,drawg):
        speed=8
        health=99
        mountpoints={'laser_top':56,'laser_left':14,'laser_right':82,'bomb_top':-20,'bomb_mid':21}
        guns=[weapons.Red_Laser,weapons.Rocket,weapons.GuidedRocket]
        PlayerShip.__init__(self,spos,health,speed,guns,mountpoints,enemies,shots,shotg,drawg)
