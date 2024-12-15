import RPi.GPIO as GPIO
import time

def setup():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)

def output(values):

    GPIO.output(2, GPIO.HIGH if values[0] else GPIO.LOW)
    GPIO.output(3, GPIO.HIGH if values[1] else GPIO.LOW)
    GPIO.output(4, GPIO.HIGH if values[2] else GPIO.LOW)
    GPIO.output(17, GPIO.HIGH if values[3] else GPIO.LOW)
    GPIO.output(27, GPIO.HIGH if values[4] else GPIO.LOW)
    GPIO.output(22, GPIO.HIGH if values[5] else GPIO.LOW)
    GPIO.output(10, GPIO.HIGH if values[6] else GPIO.LOW)
    GPIO.output(9, GPIO.HIGH if values[7] else GPIO.LOW)

def teardown():
    GPIO.cleanup()

try:

    setup()

    while True:

        output([True]*8)
        time.sleep(1)

        output([False]*8)
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    teardown()
