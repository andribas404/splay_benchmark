Инструкции по установке
=======================

1. Запустить `docker-compose up -d` в текущей папке.

2. Запуск бенчмарка `docker exec splay_benchmark_app_1 python benchmark.py`

3. Выполнить любую команду `docker exec -i splay_benchmark_app_1 <cmd>`

запуск скомпилированного *C++* `docker exec -i splay_benchmark_app_1 st <input1.txt`

Запуск *Python* `docker exec -i splay_benchmark_app_1 python splay_tree_orig.py <input1.txt`

Запуск *Pypy3* `docker exec -i splay_benchmark_app_1 pypy splay_tree_orig.py <input1.txt`

Запуск *Cython* `docker exec -i splay_benchmark_app_1 python splay_cython.py <input1.txt`

Вывод тоже работает
`docker exec -i splay_benchmark_app_1 st <input1.txt >output.txt`


Картинки
-----------------------

Запуск с генерацией состояний `docker exec -i splay_benchmark_app_1 python splay_tree_trace.py <input1.txt`

после этого создается папка graph, где лежат файлы в формате dot вида

'039- after SplayTree._remove(<Node val=100, counter=2>,).dot'

Скрипт `docker exec -i splay_benchmark_app_1 python convert.py`

преобразовывает всю папку graph в папку final в формате png.

PNG не генерируется сразу в graphviz, чтобы все файлы были одного размера и не нужно было выравнивать кадр.

Также делается файл gif.


Notes
-----------------------

Можно еще попробовать запустить cython в pypy, но для меня это пожалуй слишком, не знаю, стоит ли об этом писать)
