# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 16:22:42 2020

@author: rikus
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:24:17 2020

@author: rikus
"""

import math
from tkinter import *
import time
import random


# APUFUNKTIOT
################################################################################

def canvasMove(shape, moveX, moveY):
    """
    Liikuttaa canvas-objektia koordinaatistossa.
    moveX: positiivinen luku liikuttaa objektia oikealle
    moveY: positiivinen luku liikuttaa objektia ylöspäin
    """
    canvas.move(shape, moveX, -moveY)
    
    
def coordinates(shape, size, height):
    """
    Hakee tkinter canvas-objektin koordinaatit.
    shape: canvas-objekti
    size: objektin halkaisija
    height: koordinaatiston korkeus
    """
    pos_tkinter = canvas.coords(shape)
    x, y = pos_tkinter[0], pos_tkinter[1]
    x = x+size/2
    y = (height-y)-size/2
    return (x, y)


def createObject(size, height, colour, startX, startY):
    """
    Luo objektin canvas-koordinaatistoon.
    size: objektin halkaisija
    height: koordinaatiston korkeus
    startX: objektin keskipisteen x-koordinaatti
    startY: objektin keskipisteen y-koordinaatti
    """
    x = startX-size/2
    y = startY+size/2-height
    shape = canvas.create_oval(1, 1, size, size, fill=colour)
    canvasMove(shape, x, y)
    return shape


def createPlanet(earth_mass, earth_size, earth_angle, earth_velocity, earth_colour, earth_X, earth_Y, system):
    count = len(system)
    name = "planet" + str(count)
    planet = Body(name, earth_mass, earth_size, earth_angle, earth_velocity, earth_colour, earth_X, earth_Y)
    return planet


def distFromSun(distance, sun_X, sun_Y):
    planet_X = sun_X - distance
    planet_Y = sun_Y
    return planet_X, planet_Y


def moreMass():
    sun_mass = 1.9884 * 10**30
    mass = sun.getMass()
    newMass = 2*mass
    sun.setMass(newMass)
    text_widget.delete("1.0", END)
    text_widget.insert(END, "Sun's mass: " + str(newMass/sun_mass))
    
    
def lessMass():
    sun_mass = 1.9884 * 10**30
    mass = sun.getMass()
    newMass = 0.5*mass
    sun.setMass(newMass)
    text_widget.delete("1.0", END)
    text_widget.insert(END, "Sun's mass: " + str(newMass/sun_mass))


def addPlanet():
    velocity = random.uniform(0.3, 1.5) * earth_velocity
    colour = random.choice(colours)
    planet = createPlanet(earth_mass, earth_size, earth_angle, velocity, colour, earth_X, earth_Y, system)
    system.append(planet)
    print(len(system))


################################################################################

WIDTH = 1600
HEIGHT = 1000
colours = ["red", "green", "blue", "orange", "yellow", "cyan", "magenta", "dodgerblue",
           "turquoise", "grey", "gold", "pink"]

window = Tk()


# WIDGETS
################################################################################

canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
window.title("Solar System Simulation")

buttonMM = Button(window, text="+ mass", command=moreMass)
buttonLM = Button(window, text="- mass", command=lessMass)
button_addPlanet = Button(window, text="add planet", command=addPlanet)

text_widget = Text(window, height=2, width=30)
text_widget.insert(END, "Sun's mass: 1.0")


canvas.grid(row=0, column=0, columnspan=12)
buttonMM.grid(row=1, column=4)
buttonLM.grid(row=1, column=5)
text_widget.grid(row=1, column=6)
button_addPlanet.grid(row=1, column=7)


################################################################################


# LUOKAT
################################################################################

class Body(object):
    
    def __init__(self, name, mass, size, angle, velocity, colour, startX, startY):
        
        assert type(name) == str, "name is not string"
        assert type(mass) == int or type(mass) == float, "mass is not a number"
        assert type(size) == int or type(size) == float, "size is not a number"
        assert type(angle) == int and 0 < angle < 360, "erroneus angle"
        assert type(velocity) == int or type(velocity) == float, "velocity is not a number"
        assert type(colour) == str
        
        self.name = name
        self.mass = mass
        self.size = size
        # angle (muutettu radiaaneiksi)
        self.angle = math.radians(angle)
        # velocityX (lasketaan anglesta ja velocitystä)
        self.velocity_X = math.cos(self.angle) * velocity
        # velocityY (lasketaan anglesta ja velocitystä)
        self.velocity_Y = math.sin(self.angle) * velocity
        # Luodaan kappale haluttuihin aloituskoordinaatteihin
        self.shape = createObject(self.size, HEIGHT, colour, startX, startY)
        self.position = coordinates(self.shape, self.size, HEIGHT)
        self.force = 0
        self.distance = 0
        
    def getName(self):
        return self.name
        
    def getMass(self):
        return self.mass
    
    def setMass(self, mass):
        self.mass = mass
        
    def getPosition(self):
        return self.position
    
    def getForce(self):
        return self.force
    
    def getDistance(self):
        return self.distance
        
    def move(self):
        """
        Liikuttaa kappaletta avaruudessa yhden TIMESTEP verran.
        """
        canvasMove(self.shape, TIMESTEP*self.velocity_X, TIMESTEP*self.velocity_Y)
        self.position = coordinates(self.shape, self.size, HEIGHT)
        
    def addForces(self, bodies):
        """
        Ottaa listan saman luokan objekteja. Laskee jokaisen etäisyyden ja lisää
        niistä muodostuvat kiihtyvyydet tämän objektin nopeusvektoreihin.
        """
        
        assert type(bodies) == list, "bodies not a list"
        assert len(bodies) != 0, "bodies is empty"
        
        # tämän kappaleen massa ja positio
        mass_self = self.mass
        position_self = self.position
        for other in bodies:
            if other.getName() == self.name:
                pass
            else:
                # toisen kappaleen massa ja positio
                mass_other = other.getMass()
                position_other = other.getPosition()
                
                # etäisyydet X- ja Y-akseleilla
                distance_X = position_self[0] - position_other[0]
                distance_Y = position_self[1] - position_other[1]
                
                # kiihtyvyydet x ja y -akseleille
                # lasketaan etäisyys c
                self.distance = (abs(distance_X)**2 + abs(distance_Y)**2) ** 0.5
                # lasketaan kulma alfa
                angle = math.atan(abs(distance_Y) / abs(distance_X))
                # lasketaan Fc
                force = ((G*mass_self*mass_other) / self.distance**2) / SCALE
                self.force = force
                # lasketaan Fa
                force_Y = math.sin(angle) * force
                # lasketaan Fb
                force_X = math.cos(angle) * force
                # lasketaan aX
                acceleration_X = force_X / mass_self
                # lasketaan aY
                acceleration_Y = force_Y / mass_self
                
                # jos dist_X on positiivinen, vähennetään kiihtyvyys velocity_X
                if distance_X > 0:
                    acceleration_X = -acceleration_X
                # jos dist_Y on positiivinen, vähennetään kiihtyvyys velocity_Y
                if distance_Y > 0:
                    acceleration_Y = -acceleration_Y
                
                # lisätään kiihtyvyydet nopeuksiin
                self.velocity_X += TIMESTEP * acceleration_X
                self.velocity_Y += TIMESTEP * acceleration_Y


################################################################################


# the length of single time step in simulation (in seconds)
TIMESTEP = 100000
# The distances in the simulation are in scale 1:scale.
SCALE = 100000000000000000000000000
# gravitational constant
G = 6.674 * 10**-11
sun_X, sun_Y = WIDTH/2, HEIGHT/2


earth_name = "earth"
earth_dist_km = 151660000
earth_diam_km = 6371
earth_mass = 5.97237 * 10**24
earth_angle = 90
earth_velocity = 0.000069
earth_colour = "blue"
earth_size = 10
earth_distance = 300
earth_X, earth_Y = distFromSun(earth_distance, sun_X, sun_Y)


sun_name = "sun"
sun_mass = 1.9884 * 10**30
sun_size = 0.05*109.298*earth_size
sun_angle = 1
sun_velocity = 0
sun_colour = "yellow"
#sun_X, sun_Y: löytyvät ylempää



# MAIN LOOP
################################################################################

earth = Body(earth_name, earth_mass, earth_size, earth_angle, earth_velocity, earth_colour, earth_X, earth_Y)
sun = Body(sun_name, sun_mass, sun_size, sun_angle, sun_velocity, sun_colour, sun_X, sun_Y)

system = []

system.append(sun)
system.append(earth)



while True:
    for planet in system:
        planet.addForces(system)
    for planet in system:
        planet.move()
    window.update()
    time.sleep(0.01)

window.mainloop()


################################################################################



































