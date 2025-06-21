#!/usr/bin/python3
# missile_control.py
import time
import usb.core


class ThunderMissile():
    idVendor = 0x2123
    idProduct = 0x1010
    idName = "Dream Cheeky Thunder"
    # Protocol control bytes
    bmRequestType = 0x21
    bmRequest = 0x09
    wValue = 0x00
    wIndex = 0x00
    # Protocol command bytes
    CMDFILL = [0, 0, 0, 0, 0, 0]
    DOWN = [0x02, 0x01]
    UP = [0x02, 0x02]
    LEFT = [0x02, 0x04]
    RIGHT = [0x02, 0x08]
    FIRE = [0x02, 0x10]
    STOP = [0x02, 0x20]

    def __init__(self):
        self.dev = usb.core.find(idVendor=self.idVendor,
                                 idProduct=self.idProduct)

    def move(self, cmd, duration):
        print("Move:%s" % cmd)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, cmd+self.CMDFILL)
        time.sleep(duration)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.STOP+self.CMDFILL)


class Missile():
    def __init__(self):
        print("Initialize Missiles")
        self.usbDevice = ThunderMissile()

        if self.usbDevice.dev is not None:
            print("Device Initialized:" +
                  " %s" % self.usbDevice.idName)
            # Detach the kernel driver if active
            if self.usbDevice.dev.is_kernel_driver_active(0):
                print("Detaching kernel driver 0")
                self.usbDevice.dev.detach_kernel_driver(0)
            if self.usbDevice.dev.is_kernel_driver_active(1):
                print("Detaching kernel driver 1")
                self.usbDevice.dev.detach_kernel_driver(1)
            self.usbDevice.dev.set_configuration()
        else:
            raise Exception("Missile device not found")

    def __enter__(self):
        return self

    def left(self, duration=.3):
        self.usbDevice.move(self.usbDevice.LEFT, duration)

    def right(self, duration=.3):
        self.usbDevice.move(self.usbDevice.RIGHT, duration)

    def up(self, duration=.1):
        self.usbDevice.move(self.usbDevice.UP, duration)

    def down(self, duration=.1):
        self.usbDevice.move(self.usbDevice.DOWN, duration)

    def fire(self, duration=1):
        self.usbDevice.move(self.usbDevice.FIRE, duration)

    def stop(self, duration=1):
        self.usbDevice.move(self.usbDevice.STOP, duration)

    def __exit__(self, type, value, traceback):
        print("Exit")


def main():
    try:
        with Missile() as myMissile:
            myMissile.down()
            time.sleep(2)
            myMissile.up()
    except Exception as detail:
        print("Error: %s" % detail)


if __name__ == '__main__':
    main()
# End
