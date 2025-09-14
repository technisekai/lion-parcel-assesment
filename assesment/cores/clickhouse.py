import clickhouse_connect
from typing import Literal
import json
from datetime import datetime

def clickhouse_connection(host: str, port: int, user: str, password: str, database: str):
    """
    Create connection to clickhouse database.

    Arg(s):
        host: hostname or ip address database server
        port: port database server
        user: user name to login database server
        pass: password to login database server
        database: database name that will connect

    Return(s):
        clickhouse connection
    """
    conn = clickhouse_connect.get_client(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return conn

def insert_rows_clickhouse(destination_connect:clickhouse_connection, destination_table_name: str, data: list[dict]):
    """
    Insert data into clickhouse database.

    Arg(s):
        destination_connect: connection to destination database
        destination_table_name: table destination to inject data
        data: data to inject
    
    Return(s):
        None, inserted data to table
    """
    columns = list(data[0].keys())
    values = [tuple(row[col] \
                    if not isinstance(row.get(col, None), (dict, list)) \
                        else json.dumps(row[col]) \
                            for col in columns) for row in data]
    destination_connect.insert(
        table=destination_table_name, 
        column_names=columns, 
        data=values
    )

def clickhouse_execute(conn, query: str):
    conn.command(query)

