Щоб запустити программу підключіться до вашої postrges бази, після цього треба активувати середовище у task і cd web-site 
Далі потрібно виконати міграції, у терміналі : python manage.py makemigrations i python manage.py migrate.
Після цього можна запускати сайт командою python manage.py runserver він запуститься і ось посилання на нього http://127.0.0.1:8000/ .
