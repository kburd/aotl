
import RPi.GPIO as GPIO

class RegisterService:

    gpio_pins = [2, 3, 4, 17, 27, 22, 10, 9] 

    def startup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.gpio_pins:
            GPIO.setup(pin, GPIO.OUT)

    def write(self, value):
        for i, pin in enumerate(self.gpio_pins):
            bit = (value >> i) & 1
            GPIO.output(pin, bit)
        else:
            print(value)

    def shutdown(self):
        GPIO.cleanup()