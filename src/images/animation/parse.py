#!/usr/bin/env python
#
#       parse.py
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


class Animation:
    def __init__(self, anim, spos, startframe=0, onceoff=False):
        """
        Class to animate an image.
        anim: an anim definition file
        startframe: the frame to start at, this may be useful...
        onceoff: stop animating when we reach the end of the sequence"""
        
        self.dirty = 1
        self.dead = False
        self.onceoff = onceoff

        fin=open('ship.anim')
        lines=[i.strip().split('=')[1] for i in fin if not i[0] == '#']
        #Get the image
        image=lines.pop(0)
        time=int(lines.pop(0))
        self.frames=[]
        for i in lines:
            x,y = i.split(';')
            xs,xe = x.split(',')
            ys,ye = y.split(',')
            self.frames.append(pygame.Rect((int(xs),int(ys)), (int(xe)-int(xs),int(ye)-int(ys))))

    
        self.image, self.rect = load_image(image)
        self.rect.topleft = spos
        self.animlength = rect.right
        self.startframe = startframe
        self.index=self.startframe
        self.drawrect = self.frames[self.index]
        self.timer = Timer(time, self.next)
        
        
    def next(self):
        """Go to the next image in the animation."""

        self.index=(self.index+1)%len(self.frames)
        if self.dead: return False
        self.drawrect=
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




print image
print time
print frames
