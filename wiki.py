import wikipedia as wp
from textstat.textstat import textstat as ts
import json

def calc(content):
    return ts.flesch_reading_ease(content)

ref = {}
for i in range(100):
    a = wp.random()
    ref[wp.random] = calc(wp.page(a).content)

# for k, v in ref:
#     ref{k} = mean(v)

print(ref)
