"""python script for returning default logger to be used across modules"""

import logging
import os

PROJECT_DIR = os.getcwd() + "/"

split_str = "/"
log_path =  PROJECT_DIR + "simple_run_logs/simple_run.log"
"""path of log file for simple_run"""
log_path_folder = "".join([x + split_str for x in log_path.split(split_str)[0:-1]]) # get folder path from file path

def return_logger(log_path, logger_write_mode="a"):
    """
    return standard logger to be used across modules
    
    write modes are:
        `'a'` = append to log file

        `'w'` = erase previous log and make new log file
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    split_str = "/"
    logger_folder = "".join([x + split_str for x in log_path.split(split_str)[0:-1]]) # get folder path from file path

    #%(asctime)s:
    formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
    #check if logging folder exists, and if it doesn't, make it exist. 
    if(os.path.exists(logger_folder) != True):
        os.makedirs(logger_folder)
    file_handler = logging.FileHandler(log_path, mode=logger_write_mode)
    
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger