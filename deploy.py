import sys

from model import DbStore

def main( deploy_script ):
    with DbStore()._conn as conn:
        with conn.cursor() as curs:
            curs.execute(open(deploy_script, "r", encoding="utf8").read())

    print("All done! Rebuilt table/s and initialized seed data.")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please provide name of sql deployment script")
        exit()
    main(sys.argv[1])