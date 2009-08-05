#!/usr/bin/env python
#
#       old.py
#       
#       Copyright 2009 Rafal Jacyna <rafal@Le-Ville>
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

###########################################################
##Just a bunch of old code, that I may or may not need...##
###########################################################


class SimpleAnimation:
    def __init__(self, image, rect, step, time, spos, startframe=0,\
        onceoff=False):
        """
        Class to animate an image.
        image: a pygame image object
        step: how far to go across
        time: how often to change images
        startframe: the frame to start at, this may be useful...
        onceoff: stop animating when we reach the end of the sequence"""
        
        self.dirty = 1
        self.dead = False
        self.onceoff = onceoff
        self.image = image
        self.rect = Rect(spos, (step,rect.bottom))
        self.rect.topleft = spos
        self.spos = spos
        self.animlength = rect.right
        self.step = step
        self.startframe = step*startframe
        self.drawrect = pygame.Rect([self.startframe,0], (self.step,self.rect.bottom))
        self.timer = Timer(time, self.next)
        
        
    def next(self):
        """Go to the next image in the animation."""
        
        if self.dead: return False
        #Calculate the newrect
        newrect = self.drawrect.move((self.step, 0))
        #We have to subtract the offset from the rectangle
        #in order to account for the offset.
        if newrect.topleft[0] >= self.animlength:
            #If we are a one off (eg. an explosion) then we can die now.
            if self.onceoff: self.dead = True
            #Otherwise return to the beginning of the animation sequence
            else:
                newrect = pygame.Rect([self.startframe,0], (self.step,self.rect.bottom))
        
        self.drawrect = newrect
        self.dirty = True
        return True
        
    def move(self, newpos):
        """Move the animation to a new position.
        newpos: a [x,y] of the new coordinates"""
        
        self.rect.topleft = newpos
        self.spos = newpos

        
    def update(self, ticks):
        """Call this every loop to update the timer.
        Return False if dead, True if alive."""
        
        self.timer.update(ticks)
        if self.dead: return False
        return True
            

