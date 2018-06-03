import csv


number_weekday_map = {
    1: "Mon",
    2: "Tues",
    3: "Wed",
    4: "Thurs",
    5: "Fri",
    6: "Sat",
    7: "Sun",
}


def gen_weekday_category_dtb(path_root="data/category"):
    distuibution = {}
    category_dtb = {}
    for day in range(1, 8):
        file = "%s/%s_category.csv" % (path_root, number_weekday_map[day])
        with open(file) as csvfile:
            category_file = csv.reader(csvfile)
            for row in category_file:
                if not row[2][-1].isdigit():
                    continue
                idx = (day, int(row[1]))
                if idx not in distuibution:
                    distuibution[idx] = 0
                distuibution[idx] += int(row[2])
    for day in range(1, 8):
        sum = 0
        for c in range(1, 6):
            sum += distuibution[(day, c)]
        prob = {}
        for c in range(1, 6):
            prob[c] = distuibution[(day, c)]/(sum + 0.0)
        category_dtb[day] = prob
    return category_dtb


if __name__ == "__main__":
    path_root = "data/category"
    a = gen_weekday_category_dtb(path_root)
    print a


