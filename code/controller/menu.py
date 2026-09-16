#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: n/a
 
Brief Program/Problem Description: 

	...

Brief Solution Summary:

	Algorithmic idea, underlying theory, etc...

Used Resources/Collaborators:
	...

I/we hereby certify that I/we have produced the following solution 
using only the resources listed above in accordance with the 
CMPUT 312 collaboration policy.
"""

# Written By Graeme Aniskowicz

# ===================== Modules ===================== #
import time

from PIL import Image, ImageDraw, ImageFont
from ev3dev2.display import Display
from ev3dev2.button import Button
from ev3dev2.sound import Sound

# ==================== Constants ==================== #
TEXT_HEIGHT = 15
PADDING = 2

# ===================== Module ====================== #
class Option:
    def __init__(self, name, method):
        self.name = name
        self.method = method

        return

class Menu:
    def __init__(self, title, options):
        self.button = Button()
        self.display = Display()
        self.sound = Sound()
        self.last = 0
        self.current = 0
        self.title = title
        self.options = options

        self.display.clear()
        
        # Title
        self.display.text_pixels(self.title, x = PADDING, y = PADDING, text_color = "black", font = "helvB14")
        
        # Options
        yOffset = TEXT_HEIGHT + PADDING * 2
        for index, option in enumerate(self.options):
            if index == self.current:
                self.display.rectangle(clear_screen = False, x1 = 0,  y1 = yOffset, x2 = self.display.xres, y2 = yOffset + TEXT_HEIGHT + PADDING * 2, fill_color = "black", outline_color = "black")
                self.display.text_pixels(">{}".format(option.name), clear_screen = False, x = PADDING, y = yOffset + PADDING, text_color = "white", font = "helvB14")
            else:
                self.display.text_pixels("{}".format(option.name), clear_screen = False, x = PADDING, y = yOffset + PADDING, text_color = "black", font = "helvB14")
            yOffset += TEXT_HEIGHT + PADDING * 2
            
        # Draw
        self.display.update()

        return

    def update(self):
        # Options
        yOffset = TEXT_HEIGHT + PADDING * 2

        # Last
        lastOption = self.options[self.last]
        lastYOffset = yOffset + (TEXT_HEIGHT + PADDING * 2) * self.last
        self.display.rectangle(clear_screen = False, x1 = 0,  y1 = lastYOffset, x2 = self.display.xres, y2 = lastYOffset + TEXT_HEIGHT + PADDING * 2, fill_color = "white", outline_color = "white")
        self.display.text_pixels("{}".format(lastOption.name), clear_screen = False, x = PADDING, y = lastYOffset + PADDING, text_color = "black", font = "helvB14")

        # Current
        currentOption = self.options[self.current]
        currentYOffset = yOffset + (TEXT_HEIGHT + PADDING * 2) * self.current
        self.display.rectangle(clear_screen = False, x1 = 0,  y1 = currentYOffset, x2 = self.display.xres, y2 = currentYOffset + TEXT_HEIGHT + PADDING * 2, fill_color = "black", outline_color = "black")
        self.display.text_pixels(">{}".format(currentOption.name), clear_screen = False, x = PADDING, y = currentYOffset + PADDING, text_color = "white", font = "helvB14")

        # Draw
        self.display.update()

        self.last = self.current

        return

    def selectCurrent(self):
        option = self.options[self.current]
        method = option.method

        self.sound.beep()
        self.display.clear()
        self.display.text_pixels("Running: {}".format(option.name), clear_screen = False, x = PADDING, y = PADDING, font = "helvB14")
        self.display.update()
        
        return method()

    def inputAsync(self):
        self.update()
        while True:
            if self.button.down:
                self.current = (self.current + 1) % len(self.options)
                self.update()
                self.sound.beep("-f 200")
                time.sleep(0.2)
            elif self.button.up:
                self.current = (self.current - 1) % len(self.options)
                self.update()
                self.sound.beep("-f 200")
                time.sleep(0.2)
            elif self.button.enter:
                return self.selectCurrent()
            elif self.button.backspace:
                return

            time.sleep(0.05)

        return
