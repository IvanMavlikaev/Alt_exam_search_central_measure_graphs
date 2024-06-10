import random
delta = 0.00001
COUNT = 0

class Node:
    def __init__(self, number, squares_list, parents, children, layer):
        self.number = number
        self.squares_list = squares_list.copy()
        self.children = children
        self.parents = parents.copy()
        self.layer = layer

    def print(self):
        print(self.number, self.squares_list, self.children, self.parents, self.layer)

    def print_to_file(self, file):
        s = str(self.number) + ' ' + str(self.squares_list) + ' ' + str(
            self.children) + ' ' + str(self.parents) + ' ' + str(self.layer) + '\n'
        file.write(s)


def generate_graf(graf, count_layer):
    global COUNT
    current_layer = 1
    while current_layer < count_layer:
        for i in range(len(graf)):
            if graf[i].layer == current_layer:
                for j in range(len(graf[i].squares_list) + 1):
                    new_node_list = graf[i].squares_list.copy()
                    # weight = float(random.randint(10, 90)) / 100
                    weight = 0.3
                    if j < len(graf[i].squares_list) and (j == 0 or new_node_list[j - 1] > new_node_list[j]):
                        new_node_list[j] += 1
                    else:
                        new_node_list.append(1)
                    flag = 0
                    for k in range(i + 1, len(graf)):
                        if graf[k].squares_list == new_node_list:
                            flag = 1
                            graf[k].parents[i] = weight
                            graf[i].children[k] = weight
                            COUNT += 1
                    if not flag:
                        children = dict()
                        graf[i].children[graf[-1].number + 1] = weight
                        parent = dict()
                        parent[graf[i].number] = weight
                        new_node = Node(graf[-1].number + 1, new_node_list, parent, children, graf[i].layer + 1)
                        graf.append(new_node)
                        COUNT += 1
        current_layer += 1
    return graf


def binomial_paths(Graf):
    summ_change_prob = 0
    rhombs = dict()
    value_dict = dict()
    for elem in Graf:
        for child in elem.children.keys():
            for grandson in Graf[child].children.keys():
                for other_child in Graf[grandson].parents.keys():
                    if Graf[other_child].number > Graf[child].number and other_child in elem.children:
                        if elem.number not in rhombs.keys():
                            rhombs[elem.number] = [
                                [elem.number, Graf[child].number, Graf[grandson].number, Graf[other_child].number]]
                            value_dict[(elem.number, Graf[child].number)] = Graf[elem.number].children[Graf[child].number]
                            value_dict[(elem.number, Graf[other_child].number)] = Graf[elem.number].children[
                                Graf[other_child].number]
                        else:
                            rhombs[elem.number].append(
                                [elem.number, Graf[child].number, Graf[grandson].number, Graf[other_child].number])
                            value_dict[(elem.number, Graf[child].number)] = Graf[elem.number].children[
                                Graf[child].number]
                            value_dict[(elem.number, Graf[other_child].number)] = Graf[elem.number].children[
                                Graf[other_child].number]
    for elem in (rhombs.keys()):
        for i in range(len(rhombs[elem])):
            p1 = Graf[rhombs[elem][i][0]].children[rhombs[elem][i][1]]
            p3 = Graf[rhombs[elem][i][0]].children[rhombs[elem][i][3]]
            p2 = Graf[rhombs[elem][i][1]].children[rhombs[elem][i][2]]
            p4 = Graf[rhombs[elem][i][3]].children[rhombs[elem][i][2]]
            p3 = p1 * p2 / p4
            Graf[rhombs[elem][i][0]].children[rhombs[elem][i][3]] = p3
            Graf[rhombs[elem][i][3]].parents[rhombs[elem][i][0]] = p3
        s = sum(Graf[i].children.values())
        for i in range(len(rhombs[elem])):
            s = sum(Graf[rhombs[elem][i][0]].children.values())
            for ch in Graf[rhombs[elem][i][0]].children.keys():
                # Нормирование
                Graf[rhombs[elem][i][0]].children[ch] /= s
                # добавляем к сумме изменения вероятностей изменение конкретной вероятности
                summ_change_prob += abs(value_dict[(rhombs[elem][i][0], ch)] - Graf[rhombs[elem][i][0]].children[ch])
    return summ_change_prob / COUNT


def add_drain(graf):
    # функция добавляющая сток
    down_layer = graf[-1].layer + 1
    graf.append(Node(len(graf), [], {}, {}, down_layer + 1))
    j = len(graf) - 2
    while graf[j].layer == down_layer - 1:
        graf[-1].parents[j] = 1
        graf[j].children[len(graf) - 1] = 1
        j -= 1
        global COUNT
        COUNT += 1
    return graf


def path(graf, count_layer):
    path = []
    num = 0
    layer = 0
    flag_left = 1
    while layer < count_layer:
        path.append(num)
        if len(graf[num].children.keys()):
            if len(graf[num].children.keys()) > 2:
                half = len(graf[num].children.keys()) // 2 + 1
                for elem in graf[num].children.keys():
                    half -= 1
                    if half == 0:
                        num = elem
                        break
            elif flag_left:
                num = list(graf[num].children.keys())[0]
                flag_left = 0
            else:
                num = list(graf[num].children.keys())[-1]
                flag_left = 1
        layer += 1
    return path


def min_path(graf, p, i, cur_layer, count_layer):
    if i in p:
        return [i]
    prev_i = i
    j = graf[i].layer - 1
    p1 = []
    p1.append(i)
    while j < len(p) and i not in p:
        if i not in p1:
            p1.append(i)
        prev_i = i
        if p[j] in graf[i].children.keys():
            i = j
            j += 1
        elif i > p[j - 1]:
            if len(graf[i].children.keys()):
                i = list(graf[i].children.keys())[0]
                j += 1
            else:
                return []
        else:
            if len(graf[i].children.keys()):
                i = list(graf[i].children.keys())[-1]
                j += 1
            else:
                return []
    if len(p1) != 0 and p1[-1] != i:
        p1.append(i)
    return p1


def reference_path(graf, count_layer):
    value_dict = dict()
    p = path(graf, count_layer)
    change_prob = 0
    for i in range(len(graf)):
        path_i = []
        path_i = min_path(graf, p, i, graf[i].layer, count_layer)
        mult_i = 1
        if len(path_i):
            prev_j = path_i[0]
            for j in path_i[1:]:
                mult_i *= graf[prev_j].children[j]
                prev_j = j

        flag_adjacent_edge = 0
        cur_layer = graf[i].layer
        for ch in graf[i].children.keys():
            if ch in p and i in p:
                value_dict[(i, ch)] = graf[i].children[ch]
                continue
            path_ch = min_path(graf, p, ch, cur_layer, count_layer)
            if path_i == [i] + path_ch:
                flag_adjacent_edge = 1
                for elem in graf[i].children.keys():
                    if elem != ch:
                        path_elem = min_path(graf, p, elem, cur_layer, count_layer)
                        path_i = [i] + path_elem
                        break
            mult_ch = 1
            for j in range(1, len(path_ch)):
                mult_ch *= graf[path_ch[j - 1]].children[path_ch[j]]
            flag = 0
            for j in range(len(p)):
                if not flag_adjacent_edge:
                    if p[j] == path_ch[-1]:
                        if p[j] not in path_i:
                            path_i.append(p[j])
                        if flag:
                            mult_i *= graf[p[j - 1]].children[p[j]]
                        break
                    if p[j] == path_i[-1]:
                        flag = 1
                    if flag:
                        if j != 0:
                            mult_i *= graf[p[j - 1]].children[p[j]]
                elif flag_adjacent_edge:
                    if p[j] == path_i[-1]:
                        path_ch.append(p[j])
                        if flag:
                            mult_ch *= graf[p[j - 1]].children[p[j]]
                        break
                    if p[j] == path_ch[-1]:
                        flag = 1
                    if flag:
                        mult_ch *= graf[p[j - 1]].children[p[j]]
                        if p[j] not in path_ch:
                            path_ch.append(p[j])
            value_dict[(i, ch)] = graf[i].children[ch]
            graf[i].children[ch] = mult_i / mult_ch
        s = sum(graf[i].children.values())
        for elem in graf[i].children.keys():
            graf[i].children[elem] /= s
            change_prob += abs(graf[i].children[elem] - value_dict[(i, elem)])
    return change_prob / COUNT


def choice():
    count_layer = 0
    try:
        count_layer = int(input("Выберите количество этажей в графе, введите цифру\n"))
    except ValueError:
        print("Введена не цифра")
        return
    alg_choice = 0
    try:
        alg_choice = int(input("Выберите алгоритм, введите цифру:\n1 - алгоритм двучленных путей\n2 - алгоритм эталонного пути\n"))
    except ValueError:
        print("Введена не цифра")
        return
    if alg_choice not in [1, 2]:
        print("Неверно введен номер алгоритма")
        return
    choice_iteration = 0
    try:
        choice_iteration = int(
            input("Если вы хотите, чтобы алгоритм работал до того времени, пока среднее изменение вероятности не стало меньше 0.00001, введите 0\nИначе введите цифру не более 20\n"))
    except ValueError:
        print("Введена не цифра")
        return
    if choice_iteration < 0 or choice_iteration > 20:
        print("Не может быть такого количества итераций")
        return
    main(count_layer, alg_choice, choice_iteration)
    return


def main(levels, alg_choice, choice_iteration):
    first = Node(0, [1], {}, {}, 1)
    Graf = [first]
    Graf = generate_graf(Graf, levels)
    d = dict()
    Graf = add_drain(Graf)
    levels += 1
    DELTA = 1
    y = 0
    print("Среднее изменение переходных вероятностей по итерациям:")
    while (DELTA > delta and choice_iteration == 0 or choice_iteration != 0 and y < choice_iteration):
        y += 1
        if alg_choice == 2:
            DELTA = reference_path(Graf, levels)
            print(DELTA)
        else:
            DELTA = binomial_paths(Graf)
            print(DELTA)
        for i in range(len(Graf)):
            Graf[i].number = i
            s = sum(Graf[i].children.values())
            for elem in Graf[i].children.keys():
                Graf[i].children[elem] /= s
                if (i, elem) not in d.keys():
                    d[(i, elem)] = [Graf[i].children[elem]]
                else:
                    d[(i, elem)].append(Graf[i].children[elem])
    print("Вывод ребер графа и переходной вероятности на них")
    for i in d.keys():
        print(i, "{:.2f}".format(d[i][-1]))

choice()