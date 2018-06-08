import matplotlib.pyplot as plt


def load_price_range(path_root="data/PVG-LAX"):
    distribution = {}
    for month in range(1, 13):
        file = "%s/2017-%02d.csv" % (path_root, month)
        f = open(file, "r")
        data = f.read().split()[1:]
        for d in data:
            airline = d.split(',')[1]
            class_ = d.split(',')[2]
            px = float(d.split(',')[4])
            if (airline, class_) not in distribution:
                distribution[(airline, class_)] = []
            distribution[(airline, class_)].append(px)
            # if (airline, class_) not in distribution:
            #     distribution[(airline, class_)] = [px, px]
            # if px < distribution[(airline, class_)][0]:
            #     distribution[(airline, class_)][0] = px
            # if px > distribution[(airline, class_)][1]:
            #     distribution[(airline, class_)][1] = px
    return distribution


if __name__ == "__main__":
    a = load_price_range()
    for key, value in a.items():
        print key
        value.sort()
        # plt.scatter([i for i in range(len(value))], value)
        # plt.show()
    print a
