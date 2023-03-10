#!/usr/bin/env python
import os
import argparse
from time import time

import pandas as pd
from sqlalchemy import create_engine


CHUNK_SIZE = 100_000


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    date_cols = params.date_cols

    output_filename = 'output.csv.gz' if url.endswith('.csv.gz') else 'output.csv'

    os.system(f'wget {url} -O {output_filename}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    for df_chunk in pd.read_csv(
        output_filename, iterator=True, chunksize=CHUNK_SIZE,
        parse_dates=date_cols.split(',') if date_cols else []
    ):
        t_start = time()
        df_chunk.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        print(f'Inserted another chunk, took {t_end - t_start:.3f} seconds')

    print('Finished ingesting data into the postgres database')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the csv file')
    parser.add_argument('--date_cols', required=False, help='comma-separated list of date columns')

    args = parser.parse_args()

    main(args)
