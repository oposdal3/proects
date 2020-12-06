import sqlite3
import hashlib

db = sqlite3.connect('server.db')
sql = db.cursor()
sql_work_continue = True

#sql.execute("""DROP TABLE IF EXISTS users""")
#db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login varchar(50),
    password_hash varchar(50)
    )""")
db.commit()

while sql_work_continue == True:
    print('Для работы с таблицы можно вводить команды: \n'
          'Зарегистрироваться - Добавляет пользователя \n'
          'Стоп - завершение работы с программой \n')
    comand = input('Введите команду: ')
    if comand == 'Зарегистрироваться':
        user_login = input('Login: ')
        user_password = input('Password: ')
        h = hashlib.md5(user_password.encode())
        sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?, ?)", (user_login, h.hexdigest()))
            db.commit()
            print('Пользователь зарегистрирован.')
        else:
            print('Данный пользователь уже сушествует!!')
    elif comand == 'Стоп':
        sql_work_continue = False
    elif comand == 'Вход':
        login = input('Login: ')
        end = False
        while end == False:
            for value in sql.execute(f"SELECT * FROM users WHERE login = '{login}'"):
                user_login = value[0]
                user_password = value[1]
            password = input('Password: ')
            p = hashlib.md5(password.encode())
            if user_password == p.hexdigest():
                print('Был произведён вход в систему!')
                end = True
                sql_work_continue = False
            elif password == '':
                end = True
            else:
                print('Пароль был введён неправильно!!')
    elif comand == 'SELECT ALL':
        if input('Password: ') == '7535':
            for value in sql.execute("SELECT * FROM users"):
                print(value)
