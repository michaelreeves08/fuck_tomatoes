import Printer

testPoints = [
(176, 204),
(306, 208),
(354, 159),
(218, 134),
(277, 126),
(335, 126),
(246, 189)
]

p = Printer.Printer('', (200,200))
print(p.sendPackage(testPoints))