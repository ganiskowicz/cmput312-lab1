#!/usr/bin/env python3

"""
Group Members: Matvey Okoneshnikov (okoneshn), Graeme Aniskowicz (ganiskow), Dominik Vrbanek (vrbanek)

Date: September 14th 2026
 
Brick Number: ...

Lab Number: 1

Problem Number: n/a
 
Brief Program/Problem Description: 
	A menu system for the EV3 brick display. The menu displays both static text 
    and selectable buttons, and allows the user to navigate between buttons using 
    the EV3 controls, and execute afunction when a menu option is selected.

Brief Solution Summary:
	The program defines Text and Button classes to represent menu elements,
    and a Menu class to manage display, navigation, and selection. Button input 
    is polled in a loop, with up/down cycling through available options, 
    right selecting the current option, and backspace exiting the menu. 
    Each Button stores a callable method which is executed when that option is selected.

Used Resources/Collaborators:
	https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/display.html
    https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/button.html
    https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/sound.html?highlight=sound

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
        """
        Refresh when a new button is selected
        """
                
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

            elif self.button.right:
                return self.selectCurrent()

            elif self.button.backspace:
                return

            time.sleep(0.05)

        return