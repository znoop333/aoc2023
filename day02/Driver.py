import sys
from antlr4 import *
from gen.day02Lexer import day02Lexer
from gen.day02Parser import day02Parser
from gen.day02Visitor import day02Visitor
from VisitorInterp import VisitorInterp
from typing import List
import subprocess
import pathlib
import pandas as pd
from datetime import datetime
import numpy as np



def main(argv):
    if len(argv) > 1:
        inname = pathlib.Path(argv[1])
        input_stream = FileStream(inname, encoding='utf-8')
    else:
        input_stream = FileStream('input.txt', encoding='utf-8')
    lexer = day02Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = day02Parser(stream)
    tree = parser.start()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp()
        positions = vinterp.visit(tree)
        1


if __name__ == '__main__':
    main(sys.argv)
