# Define stepper motor functions in Micropython on the Raspberry Pi Pico
#
# This original version of this code was written by Jessica Riordan for her UCD Physics Stage 4 Project in 2021-2022

from machine import Pin
import time

####
# set up pins for microstepping the motor.
# The microstepper controller is a

pin_step = Pin(2, Pin.OUT)                        # Set up Step pin
pin_dir = Pin(3, Pin.OUT)                         # Set up Direction pin

pin_mircostepM1 = Pin(8, Pin.OUT)
pin_mircostepM2 = Pin(7, Pin.OUT)
pin_mircostepM3 = Pin(6, Pin.OUT)

# set to 1/16 microstep?
pin_mircostepM1.value(1)
pin_mircostepM2.value(1)
pin_mircostepM3.value(0)
####

####
# Set up pin for the limit sensor which is located at one end (the 'start' position)
# There is no limit sensor at the other end but the limit is achieved in software through
# setting a maximum on the number of steps that can be taken. 

pin_limitsensor = Pin(9, Pin.IN, Pin.PULL_UP)

maxsteps16 = 200_000   # macimum number of steps for 1/16 microstepping.

####

initialised = False
currentpos = 0
steptime16_us = 200.       # Note: will not move with steptime 200us if not microstepping

maxsteps = maxsteps16
steptime_us = steptime16_us


def _step(direction):
    """take one step in the given direction where 
    the direction is either 0 for away from limit switch/motor 
    or 1 for towards the limit switch/motor.
    This function should not be called by the user - use move()
    instead which checks limits"""
  
    pin_dir.value(direction)
    pin_step.value(0)
    time.sleep_us(steptime_us)
    pin_step.value(1)
    time.sleep_us(steptime_us)


def initialise():
    """Bring back to limit switch and then back off slightly to release the limit switch.
    This funciton must be called before any further movement of the motor can be done.
    Note that the position of 0 is defined as the point at which the limit switch is released. 
    This function intially prints "Initialising" and then starts to move the slider - it
    does not return any value nor does it print anything when done. It is blocking so 
    no other commands will be accepted while initialisation is being done"""
    
    global initialised
    global maxsteps
    global currentpos
   
    printf("Initialising")
    
    # move 'home' until limit sensor is triggered
    while pin_limitsensor.value(): 
        _step(1)   

    # now back off until limit sensor is no longer set    
    while not pin_limitsensor.value():
        _step(0)
    
    initialised = True
    currentpos = 0
    
    
def atlimit():
    if limitsensor.value():
        return False
    else:
        return True
    
def getcurrentpos():
    global currentpos
    return currentpos

def move(steps):
    """Move slider a given number steps.
    If steps is positive then it is away from the motor/limit sensor.
    If steps is negative then it is towards the motor/limit sensor.
    
    The possible return values are:
    "Not Initialised!"
    "Beyond limit requested - not moved"
    "Limit hit - you must reinitilise before moving again."
    "Success"
    
    Note: if the number of steps requested takes longer than the tieout set in PySerial 
    then nothing may be returned and a re-read of the serial should be performed
    at a later time. 
    """
    
    global initialised
    global maxsteps
    global currentpos
    
    if not initialised:
        return "Not Initialised!"
   
    target_steps = abs(steps)
    
    if steps >= 0:
        direction = 0
    else:
        direction = 1        
    
    counter = 0
    pin_dir.value(direction)                              
    
    if currentpos + steps > maxsteps:
        return "Beyond limit requested - not moved"

    current_pos += steps
              
    while counter < target_steps:    # At 1/16th microstepping
        counter = counter + 1
        _step(direction)
        
        if not limitsensor.value():
            initialised=False
            currentpos=0
            return "Limit hit - you must reinitilise before moving again."
     
    return("Success")       
