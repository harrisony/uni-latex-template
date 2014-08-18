#!/usr/bin/env python3

import subprocess
import re
import sys

RESULT_RE = re.compile(r'(T|F|[^ |])')
BASIC_PROPOSITION_RE = re.compile(r'([A-Za-z]+)')

REPLACEMENTS = {'~': r'\neg', '&': r'\wedge', '|': r'\vee', '<->': r'\leftrightarrow', '->': r'\rightarrow'}

wresult = subprocess.check_output(['hatt', '-e', sys.argv[1]])
result = [line.decode('UTF-8') for line in wresult.splitlines()]
del result[1] #row of --------

header_cols = re.findall(r'([A-Za-z] )+?| (.*)', result.pop(0))

expression  = header_cols.pop()[1]

for k, v in REPLACEMENTS.items():
    expression = expression.replace(k, v)

propositions = ['$' + x[0].strip() + '$' for x in header_cols]

print(str.format("\\begin{{tabular}}[|{0}|c|]", len(propositions) * 'c'))

print(' & '.join(propositions), '& $', expression, r'$ \\')

print(r"\hline")

for line in result:
  print(' & '.join(RESULT_RE.findall(line)), r'\\')

print(r"\hline")
print(r"\end{tabular}")

