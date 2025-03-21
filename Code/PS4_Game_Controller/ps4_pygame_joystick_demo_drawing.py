
"""The joystick sends update events. I guess a bit like the mouse,
if it doesn't emit an event, you must assume the mouse hasn't changed position.
Joystick events are the same, if the joystick says it's at 0.753 and 
there hasn't been an event since, well it's still at that angle.

Your movement code needs to remember the most-recent axis value
and use this as the current position of the stick.
When a new event comes then you update the value, but not otherwise.
That way then the stick is positioned to "full lock" (e.g.: 100% left)
you just keep re-positioning whatever the joystick is moving the maximum amount each frame.

The left directional-keypad on the PS4 controller is a PyGame "hat", 
so not does not generate events, you have to query it independently.
For whatever reason up and down seem to generate reverse values to 
what a normal person would expect (at the time of writing anyway).

I made some example code that moves 3 cross-hairs(sp?) around the window.
One for each stick, and one for the hat. 
It will also show which buttons are pressed.
The code could probably do with a re-organisation.
I don't like the way the hat has to be handled separately to stick-events, etc.
But it's a reasonably good demonstration how it all fits together."""

import pygame

# Window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_SURFACE = pygame.HWSURFACE | pygame.DOUBLEBUF

DARK_BLUE = (3,   5,  54)
YELLOWISH = (255, 245, 145)


class PS4Joystick:
    """ Class that knows about PS4 Controller Buttons, etc. """
    BUTTON_CROSS = 0
    BUTTON_CIRCLE = 1
    BUTTON_TRIANGLE = 2
    BUTTON_SQUARE = 3
    BUTTON_L1 = 4
    BUTTON_R1 = 5
    BUTTON_L2 = 6
    BUTTON_R2 = 7
    BUTTON_SHARE = 8
    BUTTON_OPTIONS = 9
    BUTTON_PS = 10

    AXIS_LEFT_RIGHT = 1
    AXIS_UP_DOWN = 2
    AXIS_LTRIGGER = 3
    AXIS_RTRIGGER = 4

    STICK_LEFT = 1
    STICK_RIGHT = 2
    STICK_LTRIGGER = 3
    STICK_RTRIGGER = 4

    # PS4ButtNames = [ '⨯', '○', '△', '□', 'L1', 'R1', 'L2', 'R2', 'Share', 'Options', 'PS' ]
    PS4ButtNames = ['eX', 'Oh', 'Pointy', 'Square',
                    'L1', 'R1', 'L2', 'R2', 'Share', 'Options', 'PS']
    PS4AxisNames = ['Left E/W', 'Left N/S', 'Left Trig',
                    'Right E/W', 'Right N/S', 'Right Trig']
    PS4AxisDir = [AXIS_LEFT_RIGHT, AXIS_UP_DOWN, AXIS_LTRIGGER,
                  AXIS_LEFT_RIGHT, AXIS_UP_DOWN, AXIS_RTRIGGER]

    @staticmethod
    def buttonName(butt_index):
        """ Convert the button index to human-readable name """
        if (butt_index >= 0 and butt_index < len(PS4Joystick.PS4ButtNames)):
            return PS4Joystick.PS4ButtNames[butt_index]
        else:
            return None  # error

    @staticmethod
    def axisName(axis_index):
        """ Convert the axis index to human-readable name """
        if (axis_index >= 0 and axis_index < len(PS4Joystick.PS4AxisNames)):
            return PS4Joystick.PS4AxisNames[axis_index]
        else:
            return None  # error

    @staticmethod
    def axisDirection(axis_index):
        """ Convert the axis index to x/y indicator """
        if (axis_index >= 0 and axis_index < len(PS4Joystick.PS4AxisDir)):
            return PS4Joystick.PS4AxisDir[axis_index]
        else:
            return None  # error

    @staticmethod
    def getStick(axis_index):
        """ Given an axis, work out if it's from the left or right stick """
        if (axis_index == 0 or axis_index == 1):
            return PS4Joystick.STICK_LEFT
        elif (axis_index == 3 or axis_index == 4):
            return PS4Joystick.STICK_RIGHT
        elif (axis_index == 2):
            return PS4Joystick.STICK_LTRIGGER
        elif (axis_index == 5):
            return PS4Joystick.STICK_RTRIGGER
        else:
            return None  # error


class CursorSprite(pygame.sprite.Sprite):
    SIZE = 48
    SPEED = 5

    def __init__(self, colour=(255, 245, 145)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(
            center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        # Make a centred '+'
        pygame.draw.line(self.image, colour, (self.SIZE//2, 0),
                         (self.SIZE//2, self.SIZE), 3)
        pygame.draw.line(self.image, colour, (0, self.SIZE//2),
                         (self.SIZE, self.SIZE//2), 3)

    def move(self, joy_x, joy_y):
        # Joystick events are
        self.rect.x += round(joy_x * self.SPEED)
        self.rect.y += round(joy_y * self.SPEED)


# initialisation
pygame.init()
pygame.font.init()
pygame.mixer.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), WINDOW_SURFACE)
pygame.display.set_caption("PS4 Joystick Demo")


# Joystick(s) initialisation
joystick_count = pygame.joystick.get_count()
print("Initialising %d Joystick(s)" % (joystick_count))
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    print("Joystick %d:" % (i))
    print("    name ........... [%s]" % (joystick.get_name()))
    print("    axis count ..... [%d]" % (joystick.get_numaxes()))
    print("    button count ... [%d]" % (joystick.get_numbuttons()))
    print("    hat count ...... [%d]" % (joystick.get_numhats()))

# Just deal with Joystick 0 for now
joystick = pygame.joystick.Joystick(0)
left_stick_val_horiz = 0
left_stick_val_vert = 0
right_stick_val_horiz = 0
right_stick_val_vert = 0
hat_val_horiz = 0
hat_val_vert = 0

# cursor to show movement
sprite_group = pygame.sprite.Group()
cursor_sprite_left = CursorSprite((255, 50, 50))
cursor_sprite_right = CursorSprite((50, 255, 50))
cursor_sprite_hat = CursorSprite((50, 55, 255))
sprite_group.add(cursor_sprite_left)
sprite_group.add(cursor_sprite_right)
sprite_group.add(cursor_sprite_hat)
button_text = ''

# Main Loop
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
done = False
while not done:

    # Handle user-input
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            done = True

        # Button pushed
        elif (event.type == pygame.JOYBUTTONDOWN):
            button_name = PS4Joystick.buttonName(event.button)
            button_text += ' ' + button_name
            print("Button %s pressed" % (button_name))

        # Button released
        elif (event.type == pygame.JOYBUTTONUP):
            button_name = PS4Joystick.buttonName(event.button)
            button_text = button_text.replace(' ' + button_name, '')
            print("Button %s released" % (button_name))

        # Position update form PS4-stick(s)
        elif (event.type == pygame.JOYAXISMOTION):
            stick = PS4Joystick.getStick(event.axis)
            axis = PS4Joystick.axisDirection(event.axis)
            # name  = PS4Joystick.axisName( event.axis )

            if (stick == PS4Joystick.STICK_LEFT):
                if (axis == PS4Joystick.AXIS_LEFT_RIGHT):
                    left_stick_val_horiz = event.value
                else:
                    left_stick_val_vert = event.value

            elif (stick == PS4Joystick.STICK_RIGHT):
                if (axis == PS4Joystick.AXIS_LEFT_RIGHT):
                    right_stick_val_horiz = event.value
                else:
                    right_stick_val_vert = event.value

            # The left and right triggers are also relative-positioned sticks
            elif (stick == PS4Joystick.STICK_LTRIGGER):
                pass
            elif (stick == PS4Joystick.STICK_RTRIGGER):
                pass

            # if ( event.value > 0.01 or event.value < -0.01 ):
            # print( "AXIS: %s=%6.8f" % ( name, event.value ) )

    # The Joystick "Hat" is not handled via events
    if (joystick.get_numhats() > 0):
        hat_vals = joystick.get_hat(0)
        hat_val_horiz = hat_vals[0]
        hat_val_vert = -hat_vals[1]  # up/down reversed for some reason

    # Update the on-screen tracker cursors
    cursor_sprite_left.move(left_stick_val_horiz, left_stick_val_vert)
    cursor_sprite_right.move(right_stick_val_horiz, right_stick_val_vert)
    cursor_sprite_hat.move(hat_val_horiz, hat_val_vert)

    # Update the window, but not more than 60fps
    window.fill(DARK_BLUE)
    if (len(button_text) > 0):
        button_display = font.render(
            button_text+' ',  True, DARK_BLUE, YELLOWISH)
        window.blit(button_display, (50, WINDOW_HEIGHT -
                    50-button_display.get_height()))
    sprite_group.update()
    sprite_group.draw(window)
    pygame.display.flip()

    # Clamp FPS
    clock.tick_busy_loop(60)


pygame.quit()
