import time

import matplotlib.pyplot as plt
CREATED = False

xmin,xmax,ymin,ymax = -10,10,-10,10
xstep,ystep = 5,5

BOARDERS = [xmin,xmax,ymin,ymax] # дефолтные интервалы графика
XSIZE = YSIZE = 7 # дефолтные размеры подписей точек на осях


class PlotMaker:
    def __init__(self, boarders:list = BOARDERS, steps:list = None):
        plt.ion()
        # назвать график
        plt.title("Start")
        # включить динамический режим
        plt.ion()
        # задать интервалы графика
        plt.axis(boarders)
        # сдвинуть оси в центр
        ax = plt.gca()
        self.ax = ax
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('center')
        # убрать рамки по границам
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # задать размеры подписей точек на осях
        plt.xticks(size = XSIZE)
        plt.yticks(size = YSIZE)

        # Проставить подписи точек на осях кроме начала координат
        if boarders is not None:
            xmin,xmax,ymin,ymax = boarders[0],boarders[1],\
                                  boarders[2], boarders[3]
        if steps is not None:
            xstep,ystep = steps[0],steps[1]
        else:
            xstep, ystep = 5, 5

        xArr = [i for i in range(xmin,xmax,xstep) if i != 0]
        yArr = [i for i in range(ymin,ymax,ystep) if i != 0]
        ax.axes.get_xaxis().set_ticks(xArr)
        ax.axes.get_yaxis().set_ticks(yArr)

    def __call__(self, *args, **kwargs):
        plt.show()

    def set_main(self,xVal:list, yVal:list):
        '''Добавить график целевой функции'''
        plt.plot(xVal,yVal,'#16e05a')
        plt.pause(1)

    def add(self,xVal:list, yVal:list):
        '''Добавить график попытки'''
        plt.plot(xVal,yVal,'#e0cc16')
        plt.pause(0.00002)

    def print_target(self,x,y):
        "Проставляет мишень по началу x и y"
        xVal = [i for i in range(x-1,x+1,1)] # задать массив из 3 значений x
        yVal = [i for i in range(y-1,y+1,1)]  # задать массив из 3 значений y

        plt.plot(xVal,yVal,'#e0cc16') # нарисовать первую линию

        yVal = list(reversed(yVal)) # значения y для первой линии противоположные

        plt.plot(xVal,yVal, '#e0cc16') # нарисовать вторую линию
        plt.pause(0.00002)

    def remove_target(self):
        """Удалить последнюю попытку"""
        self.ax.lines.pop(-1)
        self.ax.lines.pop(-1)

    def wait(self):
        while True:
            plt.pause(1)

    def rename(self,new):
        plt.title(new)
        plt.pause(0.00001)
