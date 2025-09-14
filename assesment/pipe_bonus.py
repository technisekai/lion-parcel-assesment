import os
import pandas as pd
import json
from dotenv import load_dotenv
from cores.clickhouse import (
    clickhouse_connection,
    insert_rows_clickhouse,
    clickhouse_execute
)
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
def get_json_data(context):
    json_dir = f"{os.getenv('PROJECT_DATA_DIR')}/bonus_json_files/"

    result_df = pd.DataFrame()
    for x in os.listdir(json_dir):
        with open(f'{json_dir}/{x}', 'r') as file:
            tmp_json = json.load(file)
            tmp_df = pd.DataFrame(tmp_json.get('MetricDataResults', {})[0])
            result_df = pd.concat([result_df, tmp_df])
    result_df = result_df[['Id', 'Timestamps', 'Values', 'StatusCode']]
    result_df.columns = ['id', 'runtime_date', 'load_time', 'message']
    result_df['runtime_date'] = pd.to_datetime(result_df['runtime_date'])
    return result_df

@op
def insert_data(results: pd.DataFrame):
    init_clickhouse()

    conn_dst = clickhouse_connection(
        host='dwh-clickhouse',
        port=int(os.getenv('CLICKHOUSE_PORT')),
        user=os.getenv('CLICKHOUSE_USERNAME'),
        password=os.getenv('CLICKHOUSE_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )
    results = results.to_dict(orient='records')
    insert_rows_clickhouse(conn_dst, 'bonus_json', results)

@graph
def pipeline_bonus():
    insert_data(get_json_data())