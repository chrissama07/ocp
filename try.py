# import random
#
#
# class X:
#     delta = []
#
#     def get_fit(self, delta):
#         self.delta = delta
#
#     def put_fit(self):
#         return self.delta
#
#
# x_list = []
# for i in range(3):
#     p = X()
#     rand = [random.random() for _ in range(3)]
#     p.get_fit(rand)
#     x_list.append(p)
#     print(x_list[i].delta)


for i in range(3):
    if i == 1:
        i -= 1
    print(i)