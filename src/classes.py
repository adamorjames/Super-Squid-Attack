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


import os
import sys

import pygame
from pygame.locals import *

from utils import *
from const import *

class DrawGroup(pygame.sprite.Group):
    """Modified versions of draw and clear."""
    def __init__(self, *sprites):
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
        for spr in sprites:
            if spr.visible:
                self.spritedict[spr] = surface.blit(spr.image,spr.rect,spr.drawrect)
        self.lostsprites = []

    def clear(self, surface, bgd):
        """clear(surface, bgd)
           erase the previous position of all sprites

           Clears the area of all sprites with the dirty flag. 
           The bgd argument should be a Surface which has the same
           dimensions as the surface."""

        for spr in self.lostsprites:
            surface.blit(bgd, spr, spr)
        for spr in self.spritedict.values():
            if spr is not 0:
                surface.blit(bgd, spr, spr)

        

class SimpleSprite(pygame.sprite.DirtySprite):
    """
    A simple sprite class.
    
    When inheriting from this class, you will have to make sure
    image, drawrect, and rect, are already in the object
    """
    containers=[]
    def __init__(self, spos, vector):
        self.rect.topleft=spos
        self.vector = vector
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        
    def update(self,ticks): pass
        
    def move(self, pos):
        self.rect.topleft = pos

    def moverel(self, offset):
        self.rect.move_ip(offset)        


        
class AnimSprite(pygame.sprite.DirtySprite):
    """Base class for various classes
    Handles anims quite well..."""
    containers=[]
    def __init__(self, anim, spos, vector):
        self.anim = anim
        self.image = anim.image
        self.anim.rect.topleft = spos
        self.rect = self.anim.rect
        self.drawrect = self.anim.drawrect
        self.vector = vector
        
        pygame.sprite.DirtySprite.__init__(self, self.containers)
        
    def update(self, ticks):
        if self.anim.dirty:
            self.rect = self.anim.rect
            self.drawrect = self.anim.drawrect
        self.anim.update(ticks)
        
    def switch_anim(self, newanim):
        pos = self.rect.topleft
        self.anim = newanim
        self.image = self.anim.image
        self.anim.rect.move_ip(pos)
        self.rect = self.anim.rect
        self.drawrect = self.anim.drawrect
        
    def move(self, pos):
        self.rect.topleft = pos
        self.anim.move(pos)

    def moverel(self, offset):
        self.rect.move_ip(offset)
        self.anim.move(self.rect.topleft)
        
    

class Animation:
    def __init__(self, data, spos, sframe=0, eframe=None, onceoff=False):
        """
        Class to animate an image.
        data: a list, [image, time, frames]
              as returned by utils.load_anim
        sframe: the frame to start at.
        eframe: the frame to end at.
        onceoff: stop animating when we reach the end of the sequence

        """
        
        self.dirty = 1
        self.dead = False
        self.onceoff = onceoff

        self.image, time, self.frames = data
        
        self.sframe = sframe
        self.index=self.sframe
        if eframe == None: self.len = len(self.frames)
        else: self.len = eframe + 1
        self.drawrect = self.frames[self.index]
        self.rect = self.drawrect.move(spos)

        self.timer = Timer(time, self.next)
        
        
    def next(self):
        """Go to the next image in the animation."""
        if self.dead: return False
        
        if not self.onceoff: self.index = (self.index+1) % self.len
        else:
            if self.index == self.len - 1: self.dead = True
            else: self.index+=1
            
        self.drawrect = self.frames[self.index]
        self.rect = self.drawrect.move(self.rect.topleft)
        self.dirty = True
        return True
        
    def move(self, newpos):
        """Move the animation to a new position.
        newpos: a [x,y] of the new coordinates"""
        self.rect.topleft = newpos
        
    def update(self, ticks):
        """Call this every loop to update the timer.
        Return False if dead, True if alive."""
        
        self.timer.update(ticks)
        if self.dead: return False
        return True


if __name__ == "__main__":
    #Initialize the display and background
    pygame.init()
    display = pygame.display.set_mode((400,400))
    background, _ = load_image('images/background.png')
    display.blit(background, (0,0))
    pygame.display.flip()

    #Prepare the animations
    anim = Animation(load_anim('images/BlackEagle/ship.anim'), [0,0])
    explosion = Animation(load_anim('images/effects/explo.anim'), [20,20], onceoff=True)

    #Create the ship
    ship = AnimSprite(anim, [0,20], [1,1])
    #Add it to the drawgroup
    
    dg = DrawGroup(ship)
    #Start the clock
    x = pygame.time.Clock()

    #This is the ships speed
    v = [2,2]
      
    while 1:
        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.quit()
                sys.exit()
        ticks = x.tick(40)
        dg.clear(display, background)
        dg.update(ticks)
        dg.draw(display)
        ship.moverel(v)
        
        if ship.rect.right > 400 or ship.rect.left < 0:
            #ship.switch_anim(explosion)
            v[0] = -v[0]
        if ship.rect.top < 0 or ship.rect.bottom > 400:
            v[1] = -v[1]
        if ship.anim.dead: ship.kill()
        pygame.display.flip()
        
