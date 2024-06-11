from contextlib import contextmanager
from config import load_config
from fastapi import HTTPException
from psycopg2 import pool
from pypika import PostgreSQLQuery as Query
from pypika import Tuple
from pypika import Case

pg_pool = pool.ThreadedConnectionPool(1, 50, **load_config())

@contextmanager
def connection():
    try:
        con = pg_pool.getconn()
        cur = con.cursor()
        yield cur
        con.commit()
    except Exception as e:
        con.rollback()
        print("DB Context error: {}".format(e))
        raise HTTPException(status_code=409, detail="db error: {}".format(e))
    finally:
        cur.close()
        pg_pool.putconn(con)

class DBContext():
    instance = None

    @staticmethod
    # pattern singleton
    def get_instance():
        if DBContext.instance == None:
            DBContext.instance = DBContext()
        return DBContext.instance
    
    @staticmethod
    def get_structure():
        if DBContext.structure == None:
            with connection() as cur:
                DBContext.structure = {}  

                query = Query.from_(DBContext.information_schema.columns).select(
                        DBContext.table_schema,
                        DBContext.table_name,
                        DBContext.ordinal_position,
                        DBContext.column_name,
                        DBContext.data_type,
                        Case()
                            .when(DBContext.character_maximum_length.notnull(), DBContext.character_maximum_length)
                            .else_(DBContext.numeric_precision).as_(DBContext.max_length),
                        DBContext.is_nullable,
                        DBContext.column_default
                    ).where(
                        DBContext.table_schema.notin(Tuple("information_schema", "pg_catalog"))
                    ).orderby(
                        DBContext.table_schema, 
                        DBContext.table_name, 
                        DBContext.ordinal_position
                    )

                cur.execute(query.get_sql())
                rows = cur.fetchall()

                for row in rows:
                    if (not(row[0] in DBContext.structure)):
                        DBContext.structure[row[0]] = {}
                    if (not(row[1] in DBContext.structure[row[0]])):
                        DBContext.structure[row[0]][row[1]] = {}

                    DBContext.structure[row[0]][row[1]][row[3]] = None

        return DBContext.structure