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

from pygame.locals import *
import pygame

import time
import os
import sys

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
        
    def change_interval(self,new_int):
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

def load_image(path):
    """Return a loaded image and it's rect"""
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print 'Cannot load image:', path
        raise SystemExit, message

    #image = image.convert()
    return image, image.get_rect()

def within(x,y,z):
    if y < x < z:
        return True
    return False
