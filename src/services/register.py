
import RPi.GPIO as GPIO

class RegisterService:

    gpio_pins = [2, 3, 4, 17, 27, 22, 10, 9] 

    def startup():
        GPIO.setmode(GPIO.BCM)
        for pin in gpio_pins:
            GPIO.setup(pin, GPIO.OUT)

    def write(value):
        for i, pin in enumerate(gpio_pins):
            bit = (value >> i) & 1
            GPIO.output(pin, bit)
        else:
            print(value)

    def shutdown():
        GPIO.cleanup()