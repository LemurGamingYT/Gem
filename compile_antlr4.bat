@echo off
antlr4 -Dlanguage=Python3 -o gem/parser -visitor -no-listener gem/Gem.g4
