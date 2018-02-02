#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Created by jianbing on 2017-10-30
"""
import sys
import logging.handlers
from colorama import Fore, Style

_logger = logging.getLogger('utx_logger')
_logger.setLevel(logging.DEBUG)
_logger_handler = logging.StreamHandler(sys.stdout)
_logger_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
_logger.addHandler(_logger_handler)


def debug(msg):
    _logger.debug("DEBUG " + str(msg))


def info(msg):
    _logger.info(Fore.GREEN + "INFO " + str(msg) + Style.RESET_ALL)


def error(msg):
    _logger.error(Fore.RED + "ERROR " + str(msg) + Style.RESET_ALL)


def warn(msg):
    _logger.warning(Fore.YELLOW + "WARNING " + str(msg) + Style.RESET_ALL)


def set_level(level):
    """ 设置log级别

    :param level: logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR
    :return:
    """
    _logger.setLevel(level)
