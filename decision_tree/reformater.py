import csv

"""
with open('combined.csv', 'rb') as r:
    with open('reformatted.csv', 'wb') as w:
        data = csv.reader(r, delimiter=',')
        for line in data:
            length = len(line)
            for i in range(0, length):
                if 'FALSE' == line[i]:
                    line[i] = 0
                elif 'TRUE' == line[i]:
                    line[i] = 1
        writer = csv.writer(w)
        writer.writerows(data)
    w.close()
r.close()


with open("new-data-set.csv", 'rb') as r:
    with open("new-data-set-refined.csv", 'wb') as w:
        data = []
        for line in csv.reader(r):
            for i in range(len(line)):
                if 0 == len(line[i].strip()):
                    line[i] = '0'
            data.append(line)
        writer = csv.writer(w)
        writer.writerows(data)
    w.close()
r.close()


with open("new-data-set.csv", 'rb') as r:
    for line in csv.reader(r):
        print(line)
r.close()
"""

with open("final_bad.csv", 'rb') as r1:
    with open("final_good.csv", 'rb') as r2:
        with open("final-data.csv", 'wb') as w:
            data = []
            for line in csv.reader(r1):
                data.append(line)
            for line in csv.reader(r2):
                data.append(line)
            writer = csv.writer(w)
            writer.writerows(data)
        w.close()
    r2.close()
r1.close()