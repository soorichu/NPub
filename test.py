import os

for _, __, files in os.walk('.'):
    for fname in files:
        f = fname.split(".")
        if len(f) == 1:
            print(f)
            try:
                if f[0][0:2] == "CH":
                    print("remove {0}".format(f))
                #    os.remove(f)
            except:
                pass