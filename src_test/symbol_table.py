# Copyright (c) Rusted Studio
# Licensed under APGL-3.0 license. Read LiCENSE.txt for more info
#Developers:
# CertifiedRice - Lead Developer
# Rusted Studio - Development Studio

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
