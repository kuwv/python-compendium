# -*- coding: utf-8 -*-
import codecs
from jinja2 import Environment, FileSystemLoader
import sys
from lunar.config.config_base import ConfigBase
from lunar.utils import Logger


class Template(object):
    __configuration = None

    def __init__(self, sourceDirectory, templateFile):
        self.__log = Logger(__name__)
        self.sourceDirectory = sourceDirectory
        self.templateFile = templateFile + ".j2"

    def generate(self, vars):
        try:
            environment = Environment(
                loader=FileSystemLoader(self.sourceDirectory), trim_blocks=True
            )
            template = environment.get_template(self.templateFile)
            self.__configuration = template.render(vars)
        except:
            self.__log.error("Error: Unable to generate template file")
            sys.exit(1)

    def save(self, destination, filename):
        if destination is None:
            destination = "/tmp"
        try:
            with open(destination + "/" + filename, "w") as f:
                f.write(self.__configuration)
            f.close()
        except IOError as err:
            if err[0] == errno.EPERM:
                self.__log.error(
                    "Error: You do not have permission to write to this file"
                )
                sys.exit(1)
