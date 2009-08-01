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
    def __init__(self,width=600,height=400):
        self._running = True
        self.display = None
        self.height=height
        self.width=width

    def Init(self):
        #initialize our display
        self.display = pygame.display.set_mode((self.width,self.height))
        #The game is now running
        self._running = True
        #We're not interested in these
        pygame.event.set_blocked(MOUSEMOTION)
        #Our clock
        self.clock=pygame.time.Clock()
        #Everything in this group will be drawn and updated
        self.drawgroup=DrawGroup()
        #The enemies go in here
        self.aliengroup=pygame.sprite.Group()
        #The background image
        self.background=load_image('images/background.png')[0]
        #This will draw the background
        self.display.blit(self.background,(0,0))
        pygame.display.flip()
        
        #Just hold enemies
        self.enemies=[]
        #Draw the first aliens to the screen
        for i in range(6):
            self.enemies.append(enemies.Squid([i*50,60]))
            self.enemies[-1].add(self.aliengroup)
            self.enemies[-1].add(self.drawgroup)
            
        #You arrive :D
        self.ship=allies.BlackEagle([self.width/4,self.height/2])
        self.ship.add(self.drawgroup)
 
    def HandleEvent(self, event):
        #print event.type
        if event.type == QUIT:
            self._running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:self.ship.die()
            elif event.key == K_LEFT:self.ship.start_moving(LEFT)
            elif event.key == K_RIGHT:self.ship.start_moving(RIGHT)
            elif event.key == K_UP:self.ship.start_moving(UP)
            elif event.key == K_DOWN:self.ship.start_moving(DOWN)
            elif event.key == K_SPACE:
                self.firing=True

        elif event.type == KEYUP:
            if event.key == K_LEFT:self.ship.stop_moving(LEFT)
            elif event.key == K_RIGHT:self.ship.stop_moving(RIGHT)
            elif event.key == K_UP:self.ship.stop_moving(UP)
            elif event.key == K_DOWN:self.ship.stop_moving(DOWN)
            elif event.key == K_SPACE:self.firing=False
            
            
    def Logic(self):
        ticks=self.clock.tick(40)
        self.drawgroup.update(ticks)

        
    def Draw(self):
        self.drawgroup.clear(self.display,self.background)
        self.drawgroup.draw(self.display)
        pygame.display.flip()
        
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
