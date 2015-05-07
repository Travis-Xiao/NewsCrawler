import beautifier
string = "'test_safd' At nearly 7,000 words, you probably don\u2019t want to try</p>sadfsadf"

f = open("tmp.txt", "w+")
print string.decode('unicode-escape')
r = beautifier.beautify(string)
f.write(r)
print r
