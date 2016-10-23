# -*- coding: utf-8 -*-
import yaml
import sys

class Configuration(object):

    def __init__(self, path):
        self.config = self.readConfig(path)
    #Path to configuration file received as argument - so pop first argument and read as yaml file.
    def readConfig(self, path):
        with open(path, 'r') as f:
            return yaml.load(f)







