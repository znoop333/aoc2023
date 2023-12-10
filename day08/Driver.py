import sys
from antlr4 import *
from gen.day08Lexer import day08Lexer
from gen.day08Parser import day08Parser
from gen.day08Visitor import day08Visitor
from VisitorInterp import VisitorInterp
from typing import List
import subprocess
import pathlib
import pandas as pd
from datetime import datetime
import numpy as np


def main(argv):
    # if len(argv) > 1:
    #     inname = pathlib.Path(argv[1])
    #     input_stream = FileStream(inname, encoding='utf-8')
    # else:
    #     input_stream = FileStream('input.txt', encoding='utf-8')
    input_stream = FileStream('test_input3.txt', encoding='utf-8')
    # input_stream = FileStream('input.txt', encoding='utf-8')

    lexer = day08Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = day08Parser(stream)
    tree = parser.start()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp()
        vinterp.visit(tree)
        print(vinterp.answer)


if __name__ == '__main__':
    main(sys.argv)
