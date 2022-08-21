# Code for Fresnel Diffraction using Ultrasound Experiment

In 2022, as a Stage 4 final-year project, the Fresnel Diffraction 
using Ultrasound Experiment was automated using a linear slider rail controlled
with a micro-stepped motor to precisely move the diffracting screen and a USB Oscilloscope to 
read out the traces. The project was undertaken by Jessica Riordan and the code
she developed was the starting point for this work. 

Python was used for the stepper motor control, USB oscilloscope 
readout and data analysis.

## Stepper Motor Control
The stepper motor is controlled using a Rapsberry Pi Pico microcontroller.
Communication with the Pi Pico from the PC is acheved over USB using PySerial
and the PiPico's REPL feature, inspired by this 
[artice](http://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html). 
We originally used Adafruit's Blinka but found it too slow for this application. 

The stepper motor control is achieved by defining a set of functions in micropython 
on the Pi Pico which are in a file call main.py that gets executed when the Pico starts up.
These functions can then be called from Python on the PC using PySerial. Note: for safety reasons
only these functions should be used for moving the motor as they check for limits being reached.

Using the Pico in this way results in whatever one would see in Thonny being sent over serial instead,
including '>>>' so these have to be handled in the code. Sample code is provided in this
repository.

## USB Oscilloscope

The USB Oscillosope used is a Picoscope model ???? which can be read out from Python.
An extensive library is available (link) but in the sample code in this repositoty 
only the essential features are used.

## Data Analysis

The analysis of the data involves Fresnel integrals for diffraction with cartesian symmetry 
and Hankel transforms for apertures with circular symmetry. 

### Fresnel Integrals 
To perform the Fresnel Integrals use the [scipy.special.fresnel](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.fresnel.html) libray.

### Hankel Transforms
While there are several libraries
available in Python for performing Hankel Transforms (pyhank and hankel) we found for this experiment
directl peforming the transform using Bessel functions: [Scipy Special Bessel](https://docs.scipy.org/doc/scipy/reference/special.html#bessel-functions) and numerically integrate using 
[scipy.integrate.quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)
