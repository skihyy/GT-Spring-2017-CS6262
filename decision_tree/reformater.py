import csv

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
