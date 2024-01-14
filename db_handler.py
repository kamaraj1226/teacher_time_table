"sqlite database handler"
import argparse
import inspect
import json
import sqlite3


def create_table(name: str) -> bool:
    "Create new Table in DB"
    # get current function name
    func_name = inspect.stack()[0][3]

    # get all contents from config file
    with open("config.json", mode="r", encoding="utf-8") as conf_file:
        config = json.load(conf_file)

    sql_dir = config.get("SQL_LOCATION", "sql/")
    db_location = config.get("DB_LOCATION", "model/")

    with open(f"{sql_dir}{func_name}.sql", mode="r", encoding="utf-8") as sqlf:
        sql_cmd = sqlf.read()

    # Placing table name
    sql_cmd = sql_cmd % name

    try:
        con = sqlite3.connect(f"{db_location}{name}.db")
        cur = con.cursor()
        cur.execute(sql_cmd)
        con.commit()
        # After successfull commit closing DB connection
        cur.close()
        con.close()
        return True
    except sqlite3.OperationalError:
        return False


parser = argparse.ArgumentParser()
parser.add_argument(
    "-c", "--create_table", help="To create new table usage: -c <table name>"
)
args = parser.parse_args()

if args.create_table:
    table_name = args.create_table
    print(f"Table creation: {create_table(table_name)}")
