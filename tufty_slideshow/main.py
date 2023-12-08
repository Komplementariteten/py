from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import jpegdec
import pimoroni
import time

button_up = pimoroni.Button(22, invert=False)
button_down = pimoroni.Button(6, invert=False)
button_b = pimoroni.Button(8, invert=False)
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
number_of_slides = 7

def count(up:bool, counter:int) -> int:
    if up:
        counter+=1
    else:
        counter-=1
    if counter > number_of_slides:
        counter = 0
    if counter < 0:
        counter = number_of_slides
    return counter        

def plot(display: PicoGraphics, counter:int):
    j = jpegdec.JPEG(display)
    file = f"slider{counter}.jpeg"
    j.open_file(file)
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
    display.update()
    

counter = 0
update_plot = True
special = False
while True:
    if button_b.is_pressed:
        j = jpegdec.JPEG(display)
        file = f"special.jpeg"
        j.open_file(file)
        j.decode(0, 0, jpegdec.JPEG_SCALE_FULL, dither=True)
        display.update()
        special=True
    elif not button_b.is_pressed and special:
        update_plot=True
        special=False
    elif button_up.is_pressed:
        counter = count(False, counter)
        update_plot=True
    elif button_down.is_pressed:
        counter = count(True, counter)
        update_plot=True
    if update_plot:
        plot(display, counter)
        update_plot=False
    time.sleep(0.1)
