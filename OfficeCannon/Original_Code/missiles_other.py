class SamMissile():
    idVendor = 0x1130
    idProduct = 0x0202
    idName = "Tenx Technology SAM Missile"
    # Protocol control bytes
    bmRequestType = 0x21
    bmRequest = 0x09
    wValue = 0x02
    wIndex = 0x01
    # Protocol command bytes
    INITA = [ord('U'), ord('S'), ord('B'), ord('C'),
             0,  0,  4,  0]
    INITB = [ord('U'), ord('S'), ord('B'), ord('C'),
             0, 64,  2,  0]
    CMDFILL = [8,  8,
               0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0,
               0,  0,  0,  0,  0,  0,  0,  0]  # 48 zeros
    STOP = [0,  0,  0,  0,  0,  0]
    LEFT = [0,  1,  0,  0,  0,  0]
    RIGHT = [0,  0,  1,  0,  0,  0]
    UP = [0,  0,  0,  1,  0,  0]
    DOWN = [0,  0,  0,  0,  1,  0]
    LEFTUP = [0,  1,  0,  1,  0,  0]
    RIGHTUP = [0,  0,  1,  1,  0,  0]
    LEFTDOWN = [0,  1,  0,  0,  1,  0]
    RIGHTDOWN = [0,  0,  1,  0,  1,  0]
    FIRE = [0,  0,  0,  0,  0,  1]

    def __init__(self):
        self.dev = usb.core.find(idVendor=self.idVendor,
                                 idProduct=self.idProduct)

    def move(self, cmd, duration):
        print("Move:%s %d sec" % (cmd, duration))
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.INITA)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.INITB)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, cmd+self.CMDFILL)
        time.sleep(duration)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.INITA)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.INITB)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.STOP+self.CMDFILL)


class ChesenMissile():
    idVendor = 0x0a81
    idProduct = 0x0701
    idName = "Chesen Electronics/Dream Link"
    # Protocol control bytes
    bmRequestType = 0x21
    bmRequest = 0x09
    wValue = 0x0200
    wIndex = 0x00
    # Protocol command bytes
    DOWN = [0x01]
    UP = [0x02]
    LEFT = [0x04]
    RIGHT = [0x08]
    FIRE = [0x10]
    STOP = [0x20]

    def __init__(self):
        self.dev = usb.core.find(idVendor=self.idVendor,
                                 idProduct=self.idProduct)

    def move(self, cmd, duration):
        print("Move:%s" % cmd)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest,
                               self.wValue, self.wIndex, cmd)
        time.sleep(duration)
        self.dev.ctrl_transfer(self.bmRequestType,
                               self.bmRequest, self.wValue,
                               self.wIndex, self.STOP)
