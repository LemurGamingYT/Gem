@echo off
antlr4 -Dlanguage=Python3 -visitor -no-listener -o gem/parser/ gem/Gem.g4
