import Printer, time, cv2
import numpy as np
from utils import Gcode, Detector, MaskProcessing, PrinterUtils
from User_Interface import Sliders

tst = [
    (50, 100),
    (175, 10),
    (60, 95)
]

res = PrinterUtils.reverseBoundX(tst, 200)

print(res)