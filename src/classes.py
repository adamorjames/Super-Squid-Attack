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

from utils import *
from const import *

class DrawGroup(pygame.sprite.Group):
    """Modified versions of draw and clear."""
    def __init__(self,*sprites):
        pygame.sprite.Group.__init__(self)
        self.add(*sprites)
        
    def draw(self, surface):
        """
        draw(surface)
        draw all sprites onto the surface
        
        Draws all the sprites onto the given surface.
           
        A little different from the default, because the sprites also
        need a drawrect attribute, to show what part of the image
        to draw.
           
        This will come in handy when doing animations."""
           
        sprites = self.sprites()
        for i in sprites:
            if i.visible:
                self.spritedict[i]=surface.blit(i.image,i.rect,i.drawrect)
        self.lostsprites = []

    def clear(self,surface,bgd):
        """clear(surface, bgd)
           erase the previous position of all sprites

           Clears the area of all sprites with the dirty flag. 
           The bgd argument should be a Surface which has the same
           dimensions as the surface."""

        for i in self.lostsprites:
            surface.blit(bgd,i,i)
        for i in self.spritedict.values():
            if i is not 0:
                surface.blit(bgd,i,i)
        

class MySprite(pygame.sprite.DirtySprite):
    """Base class for my sprites
    Handles anims quite well..."""
    def __init__(self,anim,spos,vector):
        self.anim=anim
        self.image=anim.image
        self.anim.rect.topleft=spos
        self.rect=self.anim.rect
        self.drawrect=self.anim.drawrect
        self.vector=vector
        
        pygame.sprite.DirtySprite.__init__(self)
        
    def update(self,ticks):
        if self.anim.dirty:
            self.rect=self.anim.rect
            self.drawrect=self.anim.drawrect
        self.anim.update(ticks)
        
    def switch_anim(self,newanim):
        spos=self.rect.topleft
        self.anim=newanim
        self.image=self.anim.image
        self.anim.rect.topleft=spos
        self.rect=self.anim.rect
        self.drawrect=self.anim.drawrect
        
    def move(self,pos):
        self.rect.topleft=pos
        self.anim.rect.topleft=pos

    def moverel(self,offset):
        self.rect.move_ip(offset)
        self.anim.move(self.rect.topleft)
        
    

class Animation:
    def __init__(self,image,rect,step,time,spos,startframe=0,onceoff=False):
        """
        Class to animate an image.
        image: a pygame image object
        step: how far to go across
        time: how often to change images
        startframe: the frame to start at, this may be useful...
        onceoff: stop animating when we reach the end of the sequence"""
        self.dirty=1
        self.dead=False
        self.onceoff=onceoff
        self.image=image
        self.rect=Rect(spos,(step,rect.bottom))
        self.rect.topleft=spos
        self.spos=spos
        self.animlength=rect.right
        self.step=step
        self.startframe=step*startframe
        self.timer=Timer(time,self.next)
        self.drawrect=pygame.Rect([self.startframe,0],(self.step,self.rect.bottom))
        
    def next(self):
        """Go to the next image in the animation."""
        
        if self.dead:return False
        #Calculate the newrect
        newrect=self.drawrect.move((self.step,0))
        #We have to subtract the offset from the rectangle
        #in order to account for the offset.
        if newrect.topleft[0] >= self.animlength:
            #If we are a one off (eg. an explosion) then we can die now.
            if self.onceoff:
                self.dead=True
            #Otherwise return to the beginning of the animation sequence
            else:
                newrect=pygame.Rect([self.startframe,0],(self.step,self.rect.bottom))
        
        self.drawrect=newrect
        
        self.dirty=True
        return True
        
    def move(self,newpos):
        """Move the animation to a new position.
        newpos: a [x,y] of the new coordinates"""
        
        self.rect.topleft=newpos
        self.spos=newpos
        
    def update(self,ticks):
        """Call this every loop to update the timer.
        Return False if dead, True if alive."""
        
        self.timer.update(ticks)
        if self.dead:return False
        return True
            
    
if __name__ == "__main__":
    pygame.init()
    display=pygame.display.set_mode((800,200))
    background,_=load_image('images/background.png')
    display.blit(background,(0,0))
    pygame.display.flip()
    
    image,rect=load_image('images/BlackEagle/normal.png')
    anim=Animation(image,rect,97,400,[000,000])
    explo1,explo1rect=load_image('images/explosions/explosion-1.png')
    explosion=Animation(explo1,explo1rect,64,40,[20,20],True)
    ship=MySprite(anim,[50,20],[1,1])
    dg=DrawGroup(ship)
    x=pygame.time.Clock()
    d=6
    while 1:
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()
        #display.blit(background,anim.rect,anim.rect)
        #display.blit(anim.image,anim.rect,anim.drawrect)
        #print "BLITTIED IT@",anim.rect.topleft
        #print "This much:",anim.drawrect
        ticks=x.tick(40)
        dg.clear(display,background)
        dg.update(ticks)
        dg.draw(display)
        ship.moverel([d,0])
        if ship.rect.right > 800 or ship.rect.left < 0:
            ship.switch_anim(explosion)
            d=-d
        if ship.anim.dead:ship.kill()
        pygame.display.flip()
        
