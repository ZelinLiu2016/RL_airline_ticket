def calc_price_sim(px, self_px):
    if px <= self_px:
        return 1
    if px <= 2 * self_px:
        return 1/(1.0 + 2.71828**((3 * px-6 * self_px + 0.0) / self_px))
    return 1/(1.0 + 2.71828**((px - 2 * self_px + 0.0) / self_px))


class User:
    def __init__(self, name, type, class_, airline, price):
        self.Name = name
        self.Type = type
        self.Class = class_
        self.Airline = airline
        self.Price = price

    def choice(self, tickets):
        selected = None
        if len(tickets) > 0:
            return tickets[0]
        for t in tickets:
            if self.Airline == t[0] and self.Class == t[1]:  # self.Price > (t[2] + 5000):
                return t
        return selected

    def choice_feature(self, tickets, THRESHOLD=0.5):
        selected = None
        if len(tickets) <=0:
            return selected
        ret = []
        for t in tickets:
            if t[0] == self.Airline:
                a = 1
            else:
                a = 0
            if t[1] == self.Class:
                c = 1
            else:
                c = 0
            p = calc_price_sim(t[2], sum(self.Price)/len(self.Price))
            ret.append(a*0.1 + c*0.3 + p*0.6)
        idx = -1
        value = -1
        for i in range(len(ret)):
            if ret[i] > value:
                idx = i
                value = ret[i]
        if ret[idx] >= THRESHOLD:
            selected = tickets[idx]
        return selected

    def choice_1day(self, tickets, yes_tickets):
        selected = None
        yes_ticket = None
        for t in yes_tickets:
            if yes_ticket is None:
                if self.Airline == t[0] and self.Class == t[1]:
                    yes_ticket = t
            else:
                if self.Airline == t[0] and self.Class == t[1] and yes_ticket[2] > t[2]:
                    yes_ticket = t
        if yes_ticket is None:
            return None
        for t in tickets:
            if self.Airline == t[0] and self.Class == t[1] and t[2] <= yes_ticket[2]:#self.Price > (t[2] + 5000):
                return t
        return selected

    def choice_2days(self, tickets, yes_tickets, yesyes_tickets):
        selected = None
        yes_ticket = None
        yesyes_ticket = None
        for t in yesyes_tickets:
            if yesyes_ticket is None:
                if self.Airline == t[0] and self.Class == t[1]:
                    yesyes_ticket = t
            else:
                if self.Airline == t[0] and self.Class == t[1] and yesyes_ticket[2] > t[2]:
                    yesyes_ticket = t
        for t in yes_tickets:
            if yes_ticket is None:
                if self.Airline == t[0] and self.Class == t[1]:
                    yes_ticket = t
            else:
                if self.Airline == t[0] and self.Class == t[1] and yes_ticket[2] > t[2]:
                    yes_ticket = t
        if yes_ticket is None:
            return None
        if yesyes_ticket is None:
            return None
        for t in tickets:
            if self.Airline == t[0] and self.Class == t[1] and t[2] <= yes_ticket[2] and t[2] <= yesyes_ticket[2]:#self.Price > (t[2] + 5000):
                return t
        return selected

    def show(self):
        print "Name: %s, Type: %d, Class: %s, Airline:%s, Price:%.3f" % (self.Name, self.Type, self.Class,self.Airline, self.Price)

# 1. zhike 2. shanglv 3. santuan 4. daili 5. fenxiaoshang
# 1.Y. economy 2.C. business 3.F. top