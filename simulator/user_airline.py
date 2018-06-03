import csv


all_airline = ['AA', 'DL', 'MU', 'UA']


def gen_weekday_airline_dtb(path_root="data/airline"):
    distribution = {}
    class_prob = {}
    for airline in all_airline:
        for cate in range(1, 6):
            file = "%s/2017_%s_%d.csv" % (path_root, airline, cate)
            with open(file, 'r') as csvfile:
                airline_file = csv.reader(csvfile)
                for row in airline_file:
                    if not row[0].isdigit():
                        continue
                    if int(row[0]) == 0:
                        continue
                    distribution[(cate, int(row[0]), airline)] = int(row[1])
    for cate in range(1, 6):
        for day in range(1, 8):
            sum = 0
            for airline in all_airline:
                sum += distribution[(cate, day, airline)]
            prob = {}
            for airline in all_airline:
                prob[airline] = distribution[(cate, day, airline)]/(sum + 0.0)
            class_prob[(cate, day)] = prob
    return class_prob


if __name__ == "__main__":
    a = gen_weekday_airline_dtb()
    print a
