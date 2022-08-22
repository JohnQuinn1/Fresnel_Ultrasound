import serial

class PicoSerial:
    """Class to send and receive Python commands to the Pi Pico using its REPL.
    The timeout specified in the constructor means that this is how long each
    command sent and read back will each take"""

    def __init__(self, device='COM4', baud=9600, timeout=1):
        self.serial = serial.Serial(device, baud, timeout=timeout)

    def receive(self) -> str:
        """Reads one line line (after timeout), decodes it and removes
        any '>>>' if present."""
 
        line = self.serial.readline()
        response = line.decode('UTF8').replace(">>>","").strip() # ">>>" may or may not always be present
        return response        
        
    def receive_reply(self, max_reply_attempts: int = 1) -> str:
        """Calls receive() repeatedly until a non-zero reply
        is received, up max_reply_times"""
 
        n_attempts = 0
        response = ""
        
        while n_attempts <= max_reply_attempts:
            response = self.receive()
            n_attempts += 1
            if len(response) > 0:
                break
                
        return response

    def set_timeout(self, timeout: float = 1.0) -> None:
        """Change the PySerial timeout - can be useful for commands
        which take a long time to execute"""
        
        self.serial.timeout = timeout

    def send(self, text: str) -> bool:
        """ Encodes text, adds necessary '\r' to end of line,
        reads response and makes sure it matches what was sent.
        It returns True if what was sent matches, or False if it doesn't.
        Note: the True and False have nothing to to with whether
        the instruction sent to the Pi Pico was successfully 
        executed or not - for that an additional read is needed.
        Slow commands which take longer than the timeout may need
        additional later reads. Any unread text from the Pico is 
        discarded first.
        """
        
        # clear any text buffered in the serial line
        self.serial.read_all()
        # print(self.serial.read_all().decode("UTF8"))
        
        line = f"{text}\r"
        self.serial.write(line.encode('UTF8'))
        #check that command is echoed - if not there is a problem
        got_back = self.receive()
        if got_back != text:
            print(f"Error - received text does not match sent: {got_back}")
            return False
        else:
            return True


    def close(self):
        self.serial.close()

