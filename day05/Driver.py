import sys
from antlr4 import *
from gen.day05Lexer import day05Lexer
from gen.day05Parser import day05Parser
from gen.day05Visitor import day05Visitor
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
    lexer = day05Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = day05Parser(stream)
    tree = parser.start()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp()
        vinterp.visit(tree)
        print(vinterp.total)


if __name__ == '__main__':
    main(sys.argv)
