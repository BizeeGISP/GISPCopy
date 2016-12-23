# -*- encoding: utf-8 -*-
import logging
import configUtilities
from datetime import date


class log:

    logger_path = configUtilities.getProperties('LOGGER', 'PATH')
    CALL_PRINT  = int(configUtilities.getProperties('ENVIRONMENT', 'CALL_PRINT'))
    C_Print     = False

    def __init__(self, filename, level=logging.DEBUG):
        if (self.CALL_PRINT == 1):
            self.C_Print = True

        logging.basicConfig(filename= self.logger_path + filename + "_"+ str(date.today()) + '.log', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=level)

    def error(self, msg, *args, **kwargs):

        if self.CALL_PRINT:
            print(msg, *args, **kwargs)
        else:
            logging.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.CALL_PRINT:
            print(msg, *args, **kwargs)
        else:
            logging.info(msg, *args, **kwargs)

    def warning(self,msg, *args, **kwargs):
        if self.CALL_PRINT:
            print(msg, *args, **kwargs)
        else:
            logging.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.CALL_PRINT:
            print(msg, *args, **kwargs)
        else:
            logging.debug(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.CALL_PRINT:
            print(msg, *args, **kwargs)
        else:
            logging.critical(msg, *args, **kwargs)

    def check_right_slash(self, path):
        if path.rfind('/', 0, 1) > -1:
            path += '/'