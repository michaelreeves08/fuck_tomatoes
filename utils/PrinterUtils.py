
def parsePrinterXY(printerData):
    xy = printerData.split('Count')[1].split('Z')[0].strip().replace('Y:', '').split(' ')[1:]
    return (xy[0], xy[1])
        