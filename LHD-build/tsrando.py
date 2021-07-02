
from time import time


class tsrando():
    def mytime(self):
        return time() - float(str(time()).split('.')[0])

    def randoranger(self, start, stop):
        return int(self.mytime() * (stop - start) + start)

    def randolist(self, start, stop, lenth):
        randlist = []
        for i in range(lenth):
            randlist.append(self.randoranger(start, stop))

        return randlist


# ######### Build ends here ##########


# to get a list of random integers try tsrand().randolist(start, stop, lenght of list)
# use
print(tsrando().randolist(10, 25, 5))

# to get a random integer try tsrand().randoranger(start, stop)
# use
print(tsrando().randoranger(100, 105))

# by Tirtharaj Sinha
