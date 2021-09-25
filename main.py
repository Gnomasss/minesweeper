import random
import sys
import os


class Field:
    def __init__(self, n, m, k, load=False):
        self.exit = False
        if load:
            self.loadGame()
            n = self.n
            m = self.m
            k = self.k
        else:
            self.n = n
            self.m = m
            self.k = k
            self.visible = [[False for _ in range(m + 2)] for _ in range(n + 2)]
            self.flags = [[False for _ in range(m + 2)] for _ in range(n + 2)]
            self.bombs = random.sample(list(range(0, n * m)), k)

        self.inside = [[0 for _ in range(m + 2)] for _ in range(n + 2)]
        for i in range(n + 2):
            self.inside[0][i] = 1
            self.inside[i][0] = 1
            self.inside[n + 1][i] = 1
            self.inside[i][n + 1] = 1
        #print(self.bombs)
        for i in self.bombs:
            self.inside[i // m + 1][i % m + 1] = -1
            for g in range(-1, 2):
                for t in range(-1, 2):
                    if g ** 2 + t ** 2 > 0 and self.inside[i // m + 1 + g][i % m + 1 + t] != -1:
                        self.inside[i // m + 1 + g][i % m + 1 + t] += 1


    def openZero(self, y, x):
        self.visible[y][x] = True
        #print('$', self.inside[y][x])
        for g in range(-1, 2):
            for t in range(-1, 2):
                if (g != 0 or t != 0) and self.visible[y + g][x + t] == False:
                    if self.inside[y + g][x + t] == 0:
                        #print(y + g, x + t)
                        self.openZero(y + g, x + t)
                    else:
                        self.visible[y + g][x + t] = True


    def openCell(self, y, x):
        self.visible[y][x] = True
        if self.inside[y][x] == -1:
            self.exit = True
            self.deadField()
            print('Game Over')
            sys.exit()
        else:
            if self.inside[y][x] == 0:
                self.openZero(y, x)


    def setFlag(self, y, x):
        self.flags[y][x] = True
        self.visible[y][x] = True


    def checkFinish(self):
        fl = True
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                if not (True and self.visible[i][j]):
                    fl = False
                    break
            if not fl:
                break
        if fl:
            self.exit = True
        return fl


    def deadField(self):
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if self.inside[i][j] == -1:
                    print('*', end=' ')
                else:
                    print('-', end=' ')
            print()


    def saveGame(self):
        with open('save.txt', 'wt') as f:
            f.write(str(self.n) + ' ' + str(self.m) + ' ' + str(self.k) + '\n')
            for i in range(self.n + 2):
                for j in range(self.m + 2):
                    f.write(str(1 if self.visible[i][j] else 0) + ' ')
                f.write('\n')
            for i in range(self.n + 2):
                for j in range(self.m + 2):
                    f.write(str(1 if self.flags[i][j] else 0) + ' ')
                f.write('\n')
            random.seed(157)
            for i in range(k):
                f.write(str(self.bombs[i] + random.randint(1, 10000000)) + ' ')
            random.seed()


    def loadGame(self):
        with open('save.txt') as f:
            self.n, self.m, self.k = map(int, f.readline().split())
            self.visible = []
            self.flags = []
            for i in range(self.n + 2):
                prom = []
                for j in f.readline().split():
                    prom.append(True if int(j) else False)
                self.visible.append(prom)

            for i in range(self.n + 2):
                prom = []
                for j in f.readline().split():
                    prom.append(True if int(j) else False)
                self.flags.append(prom)

            random.seed(157)
            self.bombs = [i - random.randint(1, 10000000) for i in map(int, f.readline().split())]
            random.seed()



print('Введите размеры поля и кол-во бомб')
print('игра управляется через X Y Action (x, y начинаются 1) (Action = Open или Flag)')
print('Exit - чтобы выйти из игры и, при желании, сохранить ее')

print('Начать новую игру? (y/n)')
ans = input()
if ans == 'n':
    if os.path.exists('./save.txt'):
        pole = Field(0, 0, 0, True)
        n = pole.n
        m = pole.m
        k = pole.k
    else:
        print('Файл сохранения не найден')
        print('Введите n, m, k для новой игры')
        n, m, k = map(int, input().split())
        pole = Field(n, m, k)
else:
    print('Введите n, m, k')
    n, m, k = map(int, input().split())
    pole = Field(n, m, k)

'''for i in range(n + 2):
    for j in range(m + 2):
        if pole.inside[i][j] != -1:
            print(pole.inside[i][j], end=' ')
        else:
            print('*', end=' ')
    print()'''

for i in range(1, n + 1):
    for j in range(1, m + 1):
        if not pole.visible[i][j]:
            if pole.flags[i][j]:
                print('F', end=' ')
            else:
                print('-', end=' ')
        else:
            if pole.flags[i][j]:
                print('F', end=' ')
            else:
                print(pole.inside[i][j], end=' ')
    print()

print('\n', '-----------------------------', '\n')

while not pole.exit:

    s = input()
    if s == 'Exit':
        print('Сохранить игру? (y/n)')
        ans = input()
        if ans == 'y':
            pole.saveGame()
            print('Игра сохраненна')
            sys.exit()
        else:

            pole.deadField()
            sys.exit()
    x, y, act = s.split()
    x = int(x)
    y = int(y)
    if act == 'Open':
        pole.openCell(y, x)
    elif act == 'Flag':
        pole.setFlag(y, x)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if not pole.visible[i][j]:
                if pole.flags[i][j]:
                    print('F', end=' ')
                else:
                    print('-', end=' ')
            else:
                if pole.flags[i][j]:
                    print('F', end=' ')
                else:
                    print(pole.inside[i][j], end=' ')
        print()

    if pole.checkFinish():
        print('Victory!!!')
    else:
        print('\n', '-----------------------------', '\n')








