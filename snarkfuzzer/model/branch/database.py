class VisitStatus(object):
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.hitlist = set()

    def __str__(self):
        return "VisitStatus({}, {}, {})".format(self.name, self.visited, self.hitlist)

    def __repr__(self):
        return str(self)

class Database(object):
    def __init__(self):
        self.datalist = {}

        self.importantall = 0
        self.unimportantall = 0

        self.importantthis = 0
        self.unimportantthis = 0

        self.important = 0
        self.unimportant = 0

        self.newbranch = False

    def __getitem__(self, i):
        return self.datalist[i]

    def __str__(self):
        vslist = []
        for key in self.datalist:
            vslist.append(str(self.datalist[key]))
        return "\n".join(vslist)

    def __repr__(self):
        return str(self)
    
    def add(self, fcr):
        self.datalist[fcr] = VisitStatus(fcr)

        if (fcr.important):
            self.importantall += 1
        else:
            self.unimportantall += 1

    def addvisit(self, fcr, prog):
        if (not self.datalist[fcr].visited):
            if (fcr.important):
                self.important += 1
            else:
                self.unimportant += 1

            self.newbranch = True
        
        if (fcr.important):
            self.importantthis += 1
        else:
            self.unimportantthis += 1
        
        self.datalist[fcr].visited = True
        self.datalist[fcr].hitlist.add(prog)
    
    def resetstat(self):
        self.importantthis = 0
        self.unimportantthis = 0
        self.newbranch = False
    
    def showstat(self):
        print("Hit important function/condition/return(s): {}/{}/{}".format(self.importantthis, self.important, self.importantall))
        print("Hit unimportant function/condition/return(s): {}/{}/{}".format(self.unimportantthis, self.unimportant, self.unimportantall))
        print("Hit all function/condition/return(s): {}/{}/{}".format(self.importantthis + self.unimportantthis, self.important + self.unimportant, self.importantall + self.unimportantall))