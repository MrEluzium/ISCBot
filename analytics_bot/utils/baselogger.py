# ISCBot. Telegram school helper for students.
# Copyright (C) 2021 Artem Vorochaev (vorochaev2004@live.ru, github.com/Hymiside)
#                    Artem Voronov (mreluzium@mail.ru, github.com/MrEluzium)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
import sys


FORMATTER = logging.Formatter(
        fmt="[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S")
LOG_FILE = "ISCBot.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
