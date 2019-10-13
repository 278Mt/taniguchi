class MyList(object):

    def __init__(self, li):

        self.li = li


    def __add__(self, addend):

        res = MyList(
            list(map(lambda a, b:
                a + b,
                self.li, addend.li
            ))
        )
        return res


    def __str__(self):

        return '{}'.format(self.li)



m0 = MyList([1, 1])
m1 = MyList([2, 3])

print('m0      = {}'.format(m0))
print('     m1 = {}'.format(m0))
print('m0 + m1 = {}'.format(m0 + m1))
