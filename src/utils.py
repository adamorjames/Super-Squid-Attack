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

import pygame

import os
import sys

#I'm only doing this here to convert images, because image.convert_alpha()
#needs the display to be initialized
pygame.display.init()
pygame.display.set_mode((0,0))

#Comes from:http://eli.thegreenplace.net/2009/02/13/writing-a-game-in-py
#thon-with-pygame-part-iv/
#Thanks to Eli Bendersky for the code

class Timer(object):
    """ A Timer that can periodically call a given callback 
        function.
        
        After creation, you should call update() with the 
        amount of time passed since the last call to update() 
        in milliseconds.
        
        The callback calls will result synchronously during these
        calls to update()
    """
    def __init__(self, interval, callback, oneshot=False):
        """ Create a new Timer.
        
            interval: The timer interval in milliseconds
            callback: Callable, to call when each interval expires
            oneshot: True for a timer that only acts once
        """
        self.interval = interval
        self.callback = callback
        self.oneshot = oneshot
        self.time = 0
        self.alive = True
        
    def change_interval(self, new_int):
        self.interval = new_int

    def update(self, time_passed):
        if not self.alive:
            return
            
        self.time += time_passed
        
        if self.time > self.interval:
            self.time -= self.interval
            self.callback()
            
            if self.oneshot:
                self.alive = False

class ResourceHandler:
    def __init__(self):
        self.resources={}

    def get_image(self,name):
        if self.resources.has_key(name):
            return self.resources[name]
        else:
            self.resources[name] = load_image(\
            os.path.join('data','images',name))[0]

    def get_animation(self,name):
        if self.resources.has_key(name):
            return self.resources[name]


def load_image(path):
    """Return a loaded image and it's rect"""
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', path
        raise SystemExit, message

    #image = image.convert()
    return image, image.get_rect()

def load_anim(anim):
    """Return a list with:
    [image, rect, time, frames]"""
    fin=open(anim)
    #Split the file into a list, ignoring comments (#)
    lines=[i.strip().split('=')[1] for i in fin if not i[0] == '#']
    
    #Get the image
    image=lines.pop(0)
    image_path=os.path.join(os.path.split(anim)[0],image)
    image = load_image(image_path)[0]
    
    #Get the time
    time = int(lines.pop(0))
    
    #Get the frames
    frames = []
    for i in lines:
        x,y = i.split(';')
        xs,xe = x.split(',')
        ys,ye = y.split(',')
        frames.append(pygame.Rect((int(xs),int(ys)), (int(xe)-int(xs),int(ye)-int(ys))))
    
    return [image, time, frames]
