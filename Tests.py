import Printer, time

testPoints = [
(176, 204),
(306, 208),
(354, 159),
(218, 134),
(277, 126),
(335, 126),
(246, 189)
]

p = Printer.Printer('COM4', (200,200))
time.sleep(8)

while 1:
    res = p.packageIsExecuting()
    