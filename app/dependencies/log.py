import logging, os, time
from io import StringIO
from typing import List


class LogFilter(logging.Filter):
    """
    Example : 
    adminFilter = CustomFilter(
        logFormat='%(asctime)s - %(name)s - %(filename)s - %(levelname)s line:%(lineno)s - %(user)s - %(status)s - %(message)s',
        user="danang", status="mantap")

    """
    def __init__(self,logFormat,level, saveToFile = False, **AdditionalKeyValues):
        if level:
            if not level in logging._levelToName:
                if level in logging._nameToLevel:
                    level = logging._nameToLevel[level]
                else:
                    level = 0
        else:
            level = 0
        self.levels = list(range(0,level+10,10))
        self._unapplied = ["_logFormat","_unapplied","filter","_applyAttr","_logName"]
        self._logFormat = logFormat
        self._logName = f"./app/.logfiles/log_{int(time.time())}.txt"
        self._saveToFile = saveToFile
        logging.basicConfig(filename=self._logName)
        if AdditionalKeyValues:
            for key in AdditionalKeyValues:
                if not key in self.__dict__:
                    setattr(self, key, AdditionalKeyValues[key])

    def _applyAttr(self, targetObject):
        for attr, value in vars(self).items():
            if (attr not in targetObject.__dict__) and (attr not in self._unapplied):
                setattr(targetObject, attr, value)
    
    def _setLevels(self, *levels):
        self.levels = levels

    def filter(self, record):
        self._applyAttr(record)
        if record.levelno in self.levels and self._saveToFile:
            with open(self._logName, "a") as f:
                sm = vars(record)
                sm.update({
                    "asctime":str(time.asctime()),
                    "message": sm["msg"]
                    })
                s = self._logFormat % sm
                f.write(s+"\n")
        return record.levelno in self.levels

class LogStreamer(logging.StreamHandler):
    def __init__(self, filterObject):
        super(LogStreamer, self).__init__()
        self._filter = filterObject
        self._formatter = logging.Formatter(filterObject._logFormat)
        self.setFormatter(self._formatter)
        self.addFilter(filterObject)

class AppLogger(logging.getLoggerClass()):
    def __init__(self, name: str, disable: bool, filterObject: LogFilter):
        super(AppLogger, self).__init__(name, 0)
        self._streamer = LogStreamer(filterObject)
        self.addHandler(self._streamer)
        self.disabled = bool(disable)
        self._filter = filterObject
    
    def disable(self): 
        self.disabled = True

    def enable(self): 
        self.disabled = False

    def setLevels(self, levels: List[int]):
        self._filter.levels = levels

globalFilter = LogFilter(
    logFormat = '[%(asctime)s][%(levelname)s][%(filename)s][line:%(lineno)s] - %(message)s',
    level = os.getenv('LOG_LEVEL'),
    saveToFile = os.getenv("LOG_SAVE").lower() == "true"
    )

logger = AppLogger(
    name = os.getenv("SERVICE_NAME"),
    disable = os.getenv("LOG_DISABLE").lower() == "true",
    filterObject = globalFilter
    )