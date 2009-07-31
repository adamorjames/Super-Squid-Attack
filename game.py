#!/usr/bin/env python
#
#       game.py
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

import os
import sys

import pygame
from pygame.locals import *

#Comes from:http://eli.thegreenplace.net/2009/02/13/writing-a-game-in-py
#thon-with-pygame-part-iv/
#Thanks to Eli Bendersky for the code
from utils import Timer

from classes import *
from const import *
import weapons
import allies
import enemies

pygame.init()



########################################################################
#######GAME#CODE########################################################
########################################################################

class Game:
    def __init__(self,height=800,width=600):
        self._running = True
        self.display = None
        self.height=height
        self.width=width

    def Init(self):
        #initialize our display
        self.display = pygame.display.set_mode((self.height,self.width))
        #The game is now running
        self._running = True
        #If we are firing?
        
        self.firing=False
        #We're not interested in these
        pygame.event.set_blocked(MOUSEMOTION)
        #Our clock
        self.clock=pygame.time.Clock()
        #Everything in this group will be drawn and updated
        self.drawgroup=pygame.sprite.RenderUpdates()
        #The enemies go in here
        self.aliengroup=pygame.sprite.Group()
        #All player bullets go in here
        self.projectiles=pygame.sprite.Group()
        #Powerups go here:
        self.powerups=pygame.sprite.Group()
        #The background image
        self.background=Background('background.png',-2)
        #This will draw the background
        self.display.blit(self.background.image,self.background.rect.topleft)
        pygame.display.flip()
        self.lasers=[]
        #Just hold aliens
        self.aliens=[]
        #Draw the first aliens to the screen
        for i in range(6):
            self.aliens.append(enemies.Squid([i*100,100]))
            self.aliens[-1].add(self.aliengroup)
            self.aliens[-1].add(self.drawgroup)
        #A friend :)
        self.ally=allies.BlueFalcon([100,500],self.aliens,self.lasers,self.projectiles,self.drawgroup)
        self.ally.add(self.drawgroup)
        #You arrive :D
        self.ship=allies.BlackEagle([400,400],self.aliens,self.lasers,self.projectiles,self.drawgroup)
        self.ship.add(self.drawgroup)
 
    def HandleEvent(self, event):
        #print event.type
        if event.type == QUIT:
            self._running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:self.ship.dying=True
            elif event.key == K_LEFT:self.ship.start_moving(LEFT)
            elif event.key == K_RIGHT:self.ship.start_moving(RIGHT)
            elif event.key == K_UP:self.ship.start_moving(UP)
            elif event.key == K_DOWN:self.ship.start_moving(DOWN)
            elif event.key == K_TAB:self.ship.next_weapon()
            elif event.key == K_t: self.ship.next_target()
            elif event.key == K_d:self.ship.health-=10
            elif event.key == K_e:self.ship.health+=10
            elif event.key == K_g:
                self.aliens.append(enemies.Button([200,200]))
                self.aliens[-1].add(self.aliengroup)
                self.aliens[-1].add(self.drawgroup)
            elif event.key == K_SPACE:
                self.firing=True
                
        elif event.type == KEYUP:
            if event.key == K_LEFT:self.ship.stop_moving(LEFT)
            elif event.key == K_RIGHT:self.ship.stop_moving(RIGHT)
            elif event.key == K_UP:self.ship.stop_moving(UP)
            elif event.key == K_DOWN:self.ship.stop_moving(DOWN)
            elif event.key == K_SPACE:self.firing=False
            
            
    def Logic(self):
        self.clock.tick(40)
        self.drawgroup.update()
        self.healthbar.update_life(self.ship.health)
        self.display.blit(self.healthbar.image,self.healthbar.rect.topleft)
        pygame.display.flip()
        if self.ship.alive():
            ship_collides=pygame.sprite.spritecollide(self.ship,self.aliengroup,False)
            if ship_collides:
                self.ship.health-=30
                self.ship.on_hit()
                for i in ship_collides:
                    i.die()
            sprites=pygame.sprite.groupcollide(self.aliengroup,self.projectiles,False,False)
            if sprites:
                for k,v in sprites.iteritems():
                    print k
                    for bullet in v:
                        k.on_hit(bullet)
                        bullet.die()
        
    def Draw(self):
        if self.firing:self.ship.fire()
        self.drawgroup.clear(self.display,self.background.image)
        changes=self.drawgroup.draw(self.display)
        pygame.display.update(changes)
        
    def Quit(self):
        print 'Quitting'
        pygame.quit()
 
    def Run(self):
        if self.Init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.HandleEvent(event)
            self.Logic()
            self.Draw()
        self.Quit()
 
if __name__ == "__main__" :
    game = Game()
    game.Run()
