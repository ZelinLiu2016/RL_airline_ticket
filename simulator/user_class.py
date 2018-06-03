import csv


def gen_weekday_class_dtb(path_root="data/class"):
    distribution = {}
    class_prob = {}
    for class_ in ['Y', 'C', 'F']:
        for cate in range(1, 6):
            file = "%s/2017_%s_%d.csv" % (path_root, class_, cate)
            with open(file, 'r') as csvfile:
                class_file = csv.reader(csvfile)
                for row in class_file:
                    if not row[0].isdigit():
                        continue
                    if int(row[0]) == 0:
                        continue
                    distribution[(cate, int(row[0]), class_)] = int(row[1])
    for cate in range(1, 6):
        for day in range(1, 8):
            sum = 0
            for class_ in ['Y', 'C', 'F']:
                sum += distribution[(cate, day, class_)]
            prob = {}
            for class_ in ['Y', 'C', 'F']:
                prob[class_] = distribution[(cate, day, class_)]/(sum + 0.0)
            class_prob[(cate, day)] = prob
    return class_prob


if __name__ == "__main__":
    a = gen_weekday_class_dtb()
    print a
