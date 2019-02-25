import json
MaskSettingsName = 'MaskSettings.json'

class MaskSettings:
    def __init__(self):
        with open(MaskSettingsName, 'r') as file:
            data = json.load(file)
            
        self.open = data['open']
        self.close = data['close']
        self.erode = data['erode']
        self.dilate = data['dilate']
        self.saturationMin = data['saturationMin']

    def getSettingsTuple(self):
        return (self.open, self.close, self.erode, self.dilate, self.saturationMin)

    def saveSettings(self):
        jsonDict = {
            'open': self.open,
            'close': self.close,
            'erode': self.erode,
            'dilate': self.dilate,
            'saturationMin': self.saturationMin
        }
        with open(MaskSettingsName, 'w') as file:
            json.dump(jsonDict, file)