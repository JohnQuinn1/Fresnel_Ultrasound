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

pin_mircostepper_M1 = Pin(8, Pin.OUT)
pin_mircostepper_M2 = Pin(7, Pin.OUT)
pin_mircostepper_M3 = Pin(6, Pin.OUT)

# set to 1/16 microstep?
pin_mircostepper_M1.value(1)
pin_mircostepper_M2.value(1)
pin_mircostepper_M3.value(0)
####

####
# Set up pin for the limit sensor which is located at one end (the 'start' position)
# There is no limit sensor at the other end but the limit is achieved in software through
# setting a maximum on the number of steps that can be taken. 

pin_limit_sensor = Pin(9, Pin.IN, Pin.PULL_UP)

max_steps_16 = 200_000   # macimum number of steps for 1/16 microstepping.

####

initialised = False
current_pos = 0
step_time_16_us = 200.       # Note: will not move with steptime 200us if not microstepping

max_steps = max_steps_16
step_time_us = step_time_16_us


def _step(direction: int) -> None:
    """take one step in the given direction where 
    the direction is either 0 for away from limit switch/motor 
    or 1 for towards the limit switch/motor.
    This function should not be called by the user - use move()
    instead which checks limits"""
  
    pin_dir.value(direction)
    pin_step.value(0)
    time.sleep_us(step_time_us)
    pin_step.value(1)
    time.sleep_us(step_time_us)


def initialise() -> None:
    """Bring back to limit switch and then back off slightly to release the limit switch.
    This funciton must be called before any further movement of the motor can be done.
    Note that the position of 0 is defined as the point at which the limit switch is released. 
    
    This function intially prints "Initialising" and then starts to move the slider - it
    does not return any value nor does it print anything when done. 
    
    It is blocking so no other commands will be accepted while initialisation is being done"""
    
    global initialised
    global max_steps
    global current_pos
   
    printf("Initialising")        # must print as cannot return here
    
    # move 'home' until limit sensor is triggered
    while pin_limit_sensor.value(): 
        _step(1)   

    # now back off until limit sensor is no longer set    
    while not pin_limit_sensor.value():
        _step(0)
    
    initialised = True
    current_pos = 0
    
    
def at_limit() -> bool:
    """Check if the limitsensor switch is set"""
    if limit_sensor.value():
        return False
    else:
        return True
    
def get_current_pos() -> int:
    global current_pos
    return current_pos

def move(steps: int) -> str:
    """Move slider a given number steps.
    If steps is positive then it is away from the motor/limit sensor.
    If steps is negative then it is towards the motor/limit sensor.
    
    The possible return values are:
    "Not initialised!"
    "Beyond limit requested - not moved"
    "Limit hit - you must re-initilise() before moving again."
    "Success"
    
    Note: if the number of steps requested takes longer than the tieout set in PySerial 
    then nothing may be returned and a re-read of the serial should be performed
    at a later time. 
    """
    
    global initialised
    global max_steps
    global current_pos
    
    if not initialised:
        return "Not initialised!"
   
    target_steps = abs(steps)
    
    if steps >= 0:
        direction = 0
    else:
        direction = 1        
    
    counter = 0
    pin_dir.value(direction)                              
    
    if current_pos + steps > max_steps:
        return "Beyond limit requested - not moved"

    current_pos += steps
              
    while counter < target_steps:    # At 1/16th microstepping
        counter = counter + 1
        _step(direction)
        
        if at_limit():
            initialised = False
            current_pos = 0
            return "Limit hit - you must re-initilise() before moving again."
     
    return "Success"       
