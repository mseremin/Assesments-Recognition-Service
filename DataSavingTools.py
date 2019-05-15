import csv

def create_data(fios, marks):
    data = []
    j = 0
    n = int(len(marks)/len(fios))
    for i in range(len(fios)):
        tmp_data = []
        tmp_data.append(fios[i])
        for j in range(n):
            tmp_data.append(marks[j])
        marks = marks[n:]
        data.append(tmp_data)
    return data

def write_in_csv(data):
    csv_file = open('C:/Users/eremi/Desktop/data1.csv', 'w')
    with csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)
        print("Done")