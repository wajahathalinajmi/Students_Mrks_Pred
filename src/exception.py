import sys
from src.logger import logging

def error_detail_info(error_message,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename
    lineno = exc_tb.tb_lineno
    error_message = "an error has occured in file [{0}], with line no [{1}] and detail as [{2}]".format(filename,lineno,str(error_message))

    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_detail_info(error_message=error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
    