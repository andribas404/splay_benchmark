Инструкции по установке
=======================

1. Запустить `docker-compose up -d` в текущей папке.

2. Запуск бенчмарка `docker exec splay_benchmark_app_1 python benchmark.py`

3. Выполнить любую команду `docker exec -it splay_benchmark_app_1 <cmd>`

`docker exec -it splay_benchmark_app_1 st <input1.txt`

`docker exec -it splay_benchmark_app_1 python splay_tree.py <input1.txt`
