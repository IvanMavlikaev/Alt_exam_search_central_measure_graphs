Описание кода:\
\
**Класс Node** отвечает за хранение вершины графа Юнга.\
Поля Node:\
*number* - номер вершины в графе\
*squares_list* - массив невозрастающих целых чисел (каждое число - количество квадратов в данной вертикали) - внешний вид диаграммы Юнга\
*children* - словарь потомков (ключ - номер потомка данной вершины, значение - вес ребра)\
*parents* - словарь предков данной вершины (ключ - номер предка, значение - вес ребра)\
*layer* - номер слоя вершины\
\
\
**generate_graf** - функция, которая генерируют подграф графа Юнга с заданным количеством этажей\
\
\
**add_drain** - функция, которая добавляет подграфу графа Юнга сток\
\
\
**binomial_paths** - функция, реализующая алгоритм двучленных путей\
\
\
**reference_path** - функция, реализующая алгоритм эталонного пути\
**path** - функция вычисляет эталонный путь, вызывается из функции reference_path\
**min_path** - функция вызывается из функции reference_path, вычисляет минимальный путь на графе от текущей вершины до вершины на эталонном пути\
\
\
**choice** - функция, где происходит выбор алгоритма, который будет применяться и количество итераций алгоритма\
**main** - в функции происходит вызов функций reference_path или binomial_paths, в зависимости от выбора алгоритма, до тех пор, пока среднее изменение переходной вероятности больше 0.00001 или пока не выполнится заданное пользователем количество итераций
