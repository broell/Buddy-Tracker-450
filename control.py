from Tkinter import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

class Controller:

    def __init__(self):

        self.pressed = {}

        self._create_ui()

    def start(self):

        self._animate()
        
        self.root.mainloop()

    def _create_ui(self):

        self.root = Tk()

        self.canvas = Canvas(width=200,height=200)

        self._set_bindings()

    def _animate(self):

        if self.pressed["w"] and not self.pressed["s"]:
            
            GPIO.output(19,1)

        else:

            GPIO.output(19,0)
            
        if self.pressed["a"] and not self.pressed["d"]:

            GPIO.output(21,1)

        else:

            GPIO.output(21,0)
            
        if self.pressed["s"] and not self.pressed["w"]:

            GPIO.output(22,1)

        else:

            GPIO.output(22,0)
            
        if self.pressed["d"] and not self.pressed["a"]:

            GPIO.output(23,1)

        else:

            GPIO.output(23,0)

        self.root.after(10,self._animate)

    def _set_bindings(self):

        for char in ["w", "a", "s", "d" ]:

            self.root.bind("<KeyPress-%s>" % char,self._pressed)
            
            self.root.bind("<KeyRelease-%s>" % char,self._released)

            self.pressed[char] = False

    def _pressed(self,event):

        self.pressed[event.char] = True

    def _released(self,event):

        self.pressed[event.char] = False

if __name__ == "__main__":
    
    p = Controller()

    p.start()
