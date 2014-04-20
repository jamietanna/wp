from abc import ABCMeta, abstractmethod

class ConfigWriter(object):
    __metaclass__ = ABCMeta
    __name = ""

    def __init__(self, name):
        super(ConfigWriter, self).__init__()
        __name = name

    def getName(self):
        return __name

    def writeColoursToFile(self, colours, basePath):
        coloursForFile = self.formatColoursForFile(colours)
        with open(self.getPath(basePath), 'w') as f:
            f.write(coloursForFile)
        self.afterWrite(basePath)

    @abstractmethod
    def formatColoursForFile(self, colours):
        pass

    @abstractmethod
    def getPath(self, basePath):
        pass

    # blank function to be overriden if need to have anything that runs after we've written i.e. symlinks
    def afterWrite(self):
        pass

class ShellColours(ConfigWriter):
    def __init__(self):
        super(ShellColours, self).__init__("Shell Colours")

    def formatColoursForFile(self, colours):
        shcols = ""
        for idx, c in enumerate(colours):
            shcols += """export COLOR{}="{}"\n""".format(idx, c)
        return shcols

    def getPath(self, basePath):
        return config.WP_DIRECTORY + "/." + basePath + ".shcolours"

    def afterWrite(self, basePath):
        # TODO : move to the change functions
        # SYM_PATH = config.HOME_DIR + "/.colours"

        # if os.path.exists(SYM_PATH):
        #     os.remove(SYM_PATH)

        # os.symlink(self.getPath(basePath), SYM_PATH)
        pass