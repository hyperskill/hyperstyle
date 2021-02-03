def GREETING():
    print('hi!')


class myclass:

    def __init__(self, a, b, C):
        self.A = a
        self.B = b
        self.C = C

    def myFun(self):
        print('hello 1')

    def my_fun(self, QQ):
        print('hello 2' + QQ)

    @classmethod
    def test_fun(first):
        print('hello 3')


valid_variable = 'ok'
invalidVariable = 'invalid'

print(valid_variable)
print(invalidVariable)
