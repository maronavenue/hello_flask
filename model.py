import os
import psycopg2
import sys

from flask import current_app


class DbStore():

    def __init__(self):
        self._conn = self._establish_connection()
        self._sql_deploy_script = current_app.open_resource("deploy.sql")

    def _establish_connection(self):
        # Method 1 --
        # conn = psycopg2.connect(host="localhost", port = 5432,
        #                database="nihongo_flashcards",
        #                user="postgres", password="admin1234")

        # Method 2 --
        # conn = psycopg2.connect("user='postgres' password='admin1234' host='localhost' dbname='nihongo_flashcards'")

        try:
            conn_str = os.environ["DATABASE_URL"]
            conn = psycopg2.connect(conn_str)
            print("Successfully connected to the DB: {}".format(conn.get_dsn_parameters()['dbname']))
            return conn
        except KeyError as e:
            print("Config var must be defined: {}".format(e))
            sys.exit(1)
        except psycopg2.Error as e:
            print("Could not connect to the DB instance: {}}".format(e))
            sys.exit(1)


    def get_all_cards(self):
        res = None
        with self._conn as conn:
            with conn.cursor() as curs:
                curs.execute("select * from flashcards")
                res = curs.fetchall()
        print("Successfully fetched all cards!")
        return res


    def get_card_by_id(self, id):
        query = "select * from flashcards where id = %s"
        with self._conn as conn:
            with conn.cursor() as curs:
                curs.execute(query, (id,))
                res = curs.fetchone()
        print("Successfully fetched card: {}".format(res))
        return res


    def get_total_flashcards(self):
        total = 0
        with self._conn as conn:
            with conn.cursor() as curs:
                curs.execute("select count(*) from flashcards")
                res = curs.fetchone()
        total = res[0]
        print("Total count: {}".format(total))
        return total


    def add_card(self, question, answer):
        query = "insert into flashcards (question, answer) values (%s, %s)"
        with self._conn as conn:
            with conn.cursor() as curs:
                curs.execute(query, (question, answer))
                curs.execute("select max(id) from flashcards")
                res = curs.fetchone()
        new_record = res[0]
        print("Successfully added new flash card: {}".format(new_record))
        return new_record


    def remove_card(self, id):
        query = "delete from flashcards where id = %s"
        with self._conn as conn:
            with conn.cursor() as curs:
                curs.execute(query, (id,))
        print("Successfully deleted flashcard: {}".format(id))


    def reset_db_and_load_seed_data(self):
        with self._conn as conn:
            with conn.cursor() as curs:
                curs.execute(self._sql_deploy_script.read())
        print("Successfully rebuilt table/s and reloaded seed data")
        return True

#db = DbStore()
#db.reset_db_and_load_seed_data()
# foo = db.get_card_by_id(3)
# print(foo)
# foo = db.get_total_flashcards()
# print(foo)
# db.add_card("Test2", "test2")
# db.remove_card(22)
# foo = db.get_all_cards()
# print(foo)