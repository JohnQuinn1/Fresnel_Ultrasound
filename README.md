# Fresnel Diffraction using Ultrasound Experiment

In 2022 the Fresnel Diffraction using Ultrasound Experiment was 
automated using a micro-stepped stepper motor to precisely move 
the diffracting screen and a USB Oscilloscope to record the traces.

Python was used for the stepper motor control, USB oscilloscope 
readout and data analysis.

The stepper motor is controlled using a Rapsberry Pi Pico microcontroller.
Communication with the Pi Pico from the PC is acheved over USB using PySerial
and the PiPico's REPL feature, inspired by this 
[artice](http://blog.rareschool.com/2021/01/controlling-raspberry-pi-pico-using.html): 
We originally used Adafruit's Blinka but found it too slow for this application. 
