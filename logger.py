class Logger():
    def __init__(self):
        self.__file = open('log.txt', 'w+')

    def log(self, msg):
        self.__file.write(msg + "\n")

    def __del__(self):
        self.__file.close()