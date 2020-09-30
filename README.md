<!--lint disable no-literal-urls-->
<p align="center">
  <a href="https://google.com/">
    <img
      alt="Node.js"
      src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTA6EqN_dV_KyZQH1WvoM9RRNW30Vzi00IxBA&usqp=CAU"
      width="400"
    />
  </a>
</p>

# Инструкция

1. Скачай все используемые библиотеки. Для этого в консоли поочередно напиши следующие команды: 
'pip install Flask', 'pip install requests', 'pip install beautifulsoup4', 'pip install pandas', 'pip install bd-sqlite'.

2. Запусти фаил 'app.py'

3.В браузере набери 'http://127.0.0.1:5000/api/file_handler?rooms={}&pages={}'. Первая {} - количество комнат, Вторая {} - количество страниц для парсинга. Укажи нужные параменты или используй 'http://127.0.0.1:5000/api/file_handler' - по умолчанию будут спаршены 10 страниц с параметром 2 комнаты.

4.В папке с проектом появятся два новых csv фаила. "Cards" - спаршенные данные, "clean_data" - очищенные данные.

5.Запусти фаил 'database.py'. После отработки процесса появится файл auto.db. В нем содержаться таблицы с данными об изменениях в объявлениях (удаление, добавление, изменение параметров)
