:: installing ANTLR4 also requires installing a JRE
:: https://stackoverflow.com/a/73070873
:: https://github.com/antlr/antlr4/blob/master/doc/python-target.md

conda create -n aoc2023 -y -c conda-forge python antlr4-tools antlr4-python3-runtime pandas numpy scipy networkx portion

