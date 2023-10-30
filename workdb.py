import config  # подключаем файл config.py с данным от БД
import psycopg2
from psycopg2 import Error


class SelectDatabase:
    """ Класс для работы с базой данных """

    def __init__(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            print("Информация о сервере PostgreSQL")
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("Вы подключены к - ", record, "\n")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def connect(self):
        """ Подключение к базе данных """
        connection = psycopg2.connect(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_DATABASE
        )
        return connection

    def get_info(self, time=None, source_id=None, priority=None, weight=None, keyword=None):
        """ Выборка данных из БД """

        raw_info = [time, source_id, priority, weight, keyword]
        info = []
        for i in range(len(raw_info)):
            k = raw_info[i]
            if None is not k:
                if i == 0 and (time[0] and time[1]) is not None:
                    info.append(f"time BETWEEN '{time[0]}' and '{time[1]}'")
                if i == 1 and (source_id[0] and source_id[1]) is not None:
                    info.append(f"source_id BETWEEN {source_id[0]} and {source_id[1]}")
                if i == 2:
                    info.append(f"priority = {priority}")
                if i == 3 and (weight[0] and weight[1]) is not None:
                    info.append(f"weight BETWEEN {weight[0]} and {weight[1]}")
                if i == 4:
                    info.append(f"to_tsvector(text) @@ to_tsquery('{keyword}')")

        try:
            connection = self.connect()
            cursor = connection.cursor()
            info_str = ' and '.join(info)
            select_info = 'SELECT * FROM work WHERE ' + info_str
            cursor.execute(select_info)
            result = cursor.fetchall()
            connection.commit()
            print("Результат успешно возвращен")
            return result
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def get_count(self):
        """ Подсчет всего количества записей в БД """

        try:
            connection = self.coonect()
            cursor = connection.cursor()
            count = 'SELECT count(*) FROM work'
            cursor.execute(count)
            result = cursor.fetchone
            connection.commit()
            print("Результат успешно возвращен")
            return result
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def get_count(self):
        """ Получение количества строк из БД """

        try:
            connection = self.connect()
            cursor = connection.cursor()
            select_info = 'SELECT COUNT(*) FROM work'
            cursor.execute(select_info)
            result = cursor.fetchone()
            connection.commit()
            print("Результат успешно возвращен")
            return result[0]
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")
