from picographics import PicoGraphics, DISPLAY_TUFTY_2040
display = PicoGraphics(display=DISPLAY_TUFTY_2040)

WHITE = display.create_pen(255, 255, 255)

display.set_pen(WHITE)
display.text("Hello Tufty", 0, 0, 320, 4)
display.update()