import Printer, time
from utils import Gcode

testPoints = [
    (176, 204),
    (306, 150),
    (176, 204), 
    (306, 150)
]

start_time = time.time()
p = Printer.Printer('COM4', (200,200))

cum = False
while 1:
    if time.time() - start_time > 8:
        if not cum:
            cum = True
            p.sendPackage(testPoints)
            
        res = p.packageIsExecuting()
        if not res:
            print('Is HOmed: ' + str(time.time()))
            p.sendPackage(testPoints)
