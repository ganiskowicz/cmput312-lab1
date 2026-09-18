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

from ev3dev2.display import Display
from ev3dev2.button import Button as EV3Button
from ev3dev2.sound import Sound

# ==================== Constants ==================== #
TEXT_HEIGHT = 15
PADDING = 2

# ===================== Classes ===================== #
class Text:
    def __init__(self, text):
        self.text = text

        return

class Button:
    def __init__(self, text, method):
        self.text = text
        self.method = method

        return

class Menu:
    def __init__(self, elements):
        self.button = EV3Button()
        self.display = Display()
        self.sound = Sound()

        self.elements = elements

        self.buttons = [element for element in self.elements if isinstance(element, Button)]

        self.current = 0
        self.last = 0

        return

    def clear(self):
        self.display.clear()

    def draw(self):
        self.display.clear()

        yOffset = 0
        buttonIndex = 0

        for element in self.elements:
            if isinstance(element, Button):
                if buttonIndex == self.current:
                    self.display.rectangle(clear_screen = False, x1 = 0, y1 = yOffset, x2 = self.display.xres, y2 = yOffset + TEXT_HEIGHT + PADDING * 2, fill_color = "black", outline_color = "black")
                    self.display.text_pixels(">{}".format(element.text), clear_screen = False, x = PADDING, y = yOffset + PADDING, text_color = "white", font = "helvB14")
                else:
                    self.display.text_pixels(element.text, clear_screen = False, x = PADDING, y = yOffset + PADDING, text_color = "black", font = "helvB14")
                buttonIndex += 1
            elif isinstance(element, Text):
                self.display.text_pixels(element.text, clear_screen = False, x = PADDING, y = yOffset + PADDING, text_color = "black", font = "helvB14")
            yOffset += TEXT_HEIGHT + PADDING * 2

        self.display.update()

        return

    def selectCurrent(self):
        self.display.clear()
        self.sound.beep()
        if len(self.buttons) > self.current:
            button = self.buttons[self.current]
            return button.method()
        else:
            return

    def inputAsync(self):
        self.draw()

        while True:
            if self.button.down:
                self.current = (self.current + 1) % len(self.buttons)
                self.draw()
                self.sound.beep("-f 200")
                time.sleep(0.2)

            elif self.button.up:
                self.current = (self.current - 1) % len(self.buttons)
                self.draw()
                self.sound.beep("-f 200")
                time.sleep(0.2)

            elif self.button.enter:
                return self.selectCurrent()

            elif self.button.backspace:
                return

            time.sleep(0.05)

        return