import os
from dotenv import load_dotenv
from cores.mysql import (
    mysql_connection,
    read_from_mysql
)
from cores.clickhouse import (
    clickhouse_connection,
    insert_rows_clickhouse,
    clickhouse_execute
)
import json
from dagster import op, graph

load_dotenv()
def init_clickhouse():
    conn_dst = clickhouse_connection(
        host='dwh-clickhouse',
        port=int(os.getenv('CLICKHOUSE_PORT')),
        user=os.getenv('CLICKHOUSE_USERNAME'),
        password=os.getenv('CLICKHOUSE_PASSWORD'),
        database='default'
    )
    with open(f"{os.getenv('PROJECT_QUERIES_DIR')}/dst/init_dst.sql", 'r') as f:
        query = f.read()

    for statement in query.split(";"):
        stmt = statement.strip()
        if stmt: 
            clickhouse_execute(conn_dst, stmt)

@op
def get_data_from_mysql(context):
    conn_src = mysql_connection(
        host='db-mysql',
        port=int(os.getenv('MYSQL_PORT')),
        user=os.getenv('MYSQL_USERNAME'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    with open(f"{os.getenv('PROJECT_QUERIES_DIR')}/src/get_src_data.sql", 'r') as f:
        query = f.read()
    result = read_from_mysql(conn_src, query)
    conn_src.close()
    return result

@op
def update_data_to_clickhouse(results: list):
    init_clickhouse()

    conn_dst = clickhouse_connection(
        host='dwh-clickhouse',
        port=int(os.getenv('CLICKHOUSE_PORT')),
        user=os.getenv('CLICKHOUSE_USERNAME'),
        password=os.getenv('CLICKHOUSE_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    insert_rows_clickhouse(conn_dst, 'retail_transaction', results)

@graph
def pipeline_task():
    update_data_to_clickhouse(get_data_from_mysql())