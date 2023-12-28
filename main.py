from plotmaker import PlotMaker
import random

class Model():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.relevance = None
        self.relVal = None

def fitting(population:list, p:PlotMaker):
    """Функция приспособляемости"""
    successCnt = 0
    for model in population: # type: Model
        mx,my = model.x, model.y
        p.print_target(mx,my)

        if f(mx) == my and mx in targetX:
            model.relevance = True
            successCnt +=1
        else:
            p.remove_target()
            model.relevance = False
    return successCnt

def selection(population:list):
    """Функция отбора"""
    for model in population: # type: Model
        mx,my = model.x, model.y
        roMin = 0

        for i in range(targetX.__len__()):
            tx,ty = targetX[i],targetY[i]
            ro = ((tx - mx)**2) + ((ty-my)**2)
            if roMin == 0:
                roMin = ro
            elif ro < roMin:
                roMin = ro
        model.relVal = roMin

    population = sorted(population,key= lambda m: m.relVal)
    # выбрать часть лучших и сделать их успешными
    numOfRelevent = int(RELEVANT_VALID_PART * POPULATION_SIZE)
    for i in range(numOfRelevent):
        model = population[i]
        model.relevance = True

    for i in range(numOfRelevent,POPULATION_SIZE):
        model = population[i]
        mx,my = model.x,model.y
        if f(mx) == my or model.relVal <= 15:
            model.relevance = True
        else:
            model.relevance = False
    return population


def cross_over(population:list):
    """Функция скрещивания"""
    newPopulation = []

    oldRelevant,oldRelevantCnt = int(POPULATION_SIZE * RELEVANT_PART), 0
    oldDead,oldDeadCnt = int(POPULATION_SIZE * DEAD_PART), 0

    oldSize = oldRelevant + oldDead
    crossSize = population.__len__() - oldSize

    # скрещиваем crossSize*2 популяций
    parents = []
    while newPopulation.__len__() != crossSize:
        currentPair = []
        for model in population:
            if model not in parents:
                currentPair.append(model)
                parents.append(Model)
            if currentPair.__len__() == 2:
                parent1 = currentPair[0]
                parent2 = currentPair[1]

                offSpringX = int((parent1.x + parent2.x) / 2)
                offSpringY = int((parent1.y + parent2.y) / 2)


                newPopulation.append(Model(offSpringX, offSpringY))
                currentPair = []

    # набираем особей из предыдущей популяции
    oldCnt = 0
    for model in population:
        if oldCnt == oldSize:
            break
        oldCnt += 1
        newPopulation.append(model)

    return newPopulation

def mutation(population:list):
    """Функция мутации"""
    mutationList = population[population.__len__() - MUTATION_SIZE:]
    for i in range(mutationList.__len__()):
        model = mutationList[i]
        if i % 2 == 0:
            model.x = random_length()
        else:
            model.y = random_length()

    population = population[0:population.__len__() - MUTATION_SIZE:] + mutationList
    return population

###################################################
def random_length():
    randint = random.randint(1,1500) % 200 - 100
    return randint

def count_relevant(population:list):
    cnt = 0
    for m in population:
        if m.relevance == True:
            cnt+=1
    return cnt

def f(x):
    # return (x*x)+1
    return x*x-1

# количество особей в популяции
POPULATION_SIZE = 1000
# доля успешных в отсоритированном списке
RELEVANT_VALID_PART = 0.25
# доли участвующих в скрещивании
RELEVANT_PART = 0.3
DEAD_PART = 0.2
# доля мутировавших
MUTATION_PART = 0.1
MUTATION_SIZE = int(POPULATION_SIZE * MUTATION_PART)

if __name__ == '__main__':
    # область определения
    xmin,xmax = -100, 100+1
    # набор аргументов
    xVal = [i for i in range(xmin, xmax, 1)]
    # уравнение
    yVal = [f(x) for x in xVal]
    # график
    p = PlotMaker([xmin, xmax, -100, 100], [25, 25])
    p.set_main(xVal,yVal)
    # зона попадания - интервал по x
    targetX = [i for i in range(0,10)]
    targetY = [f(x) for x in targetX]

    # первая популяция генерируется случайно
    population = [Model(random_length(),random_length()) for i in range(POPULATION_SIZE)]

    popNum = 1
    while True:
        # оценка
        p.rename(f"Populaton {popNum}")
        successCnt = fitting(population, p) # проверка особей
        print(f"{popNum} population: {successCnt} successfull")
        population = selection(population) # отбор
        population = cross_over(population) # скрещивание
        population = mutation(population) # мутация
        popNum +=1