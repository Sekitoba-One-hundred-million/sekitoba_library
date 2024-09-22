import psycopg2
from tqdm import tqdm
from psycopg2.extras import DictCursor

class PsqlControl:
    def __init__( self ):
        self.conn = psycopg2.connect( self.create_db_url() )

    def create_db_url( self ):
        host = "100.88.209.66"
        port = "5432"
        dbname = "postgres"
        user = "sekitoba"
        password = self.get_password()
        return "host={} dbname={} port={} user={} password={}".format( host, dbname, port, user, password )

    def remove_conma( self, sql ):
        if sql[-1] == ",":
            sql = sql[:-1]

        return sql

    def get_password( self ):
        f = open( "/Volumes/Gilgamesh/.import/db_pqss", "r" )
        password = f.read()
        f.close()

        return password.replace( "\n", "" )

    def exist_table( self, table_name ):
        sql = "SELECT * FROM information_schema.tables WHERE table_name = '{}';".format( table_name )
        cur = self.conn.cursor( cursor_factory=DictCursor )
        cur.execute( sql )
        row = cur.fetchall()

        if len( row ) == 0:
            return False
        
        return True

    def insert_data( self, table_name, data, colums ):
        sql = [ "INSERT INTO {} (".format( table_name ) ]

        for i, key in enumerate( colums.keys() ):
            sql.append( "{}".format( key ) )

            if not len( colums ) - 1 == i:
                sql.append( "," )

        sql = self.remove_conma( sql )
        sql.append( ") VALUES " )

        for d in tqdm( data ):
            sql.append( '(' )
            
            for i, key in enumerate( colums.keys() ):
                if "[]" in colums[key]:
                    sql.append( "'" + "{}".format(
                        str( d[key] ).replace( "[", "{" ).replace( "]", "}" ) ).replace( "'", "\"" ) + "'" )
                elif colums[key] == "text":
                    sql.append( "'{}'".format( d[key] ) )
                else:
                    sql.append( "{}".format( d[key] ) )

                if not len( colums ) - 1 == i:
                    sql.append( "," )

            sql.append( ')' )
            sql.append( ',' )

        sql = self.remove_conma( sql )
        sql.append( ';' )

        with self.conn.cursor() as cur:
            cur.execute( "".join( sql ) )

        self.conn.commit()
        
    def create_table( self, table_name, colums ):
        sql = 'CREATE TABLE {} ('.format( table_name )

        for key in colums.keys():
            sql += "{} {},".format( key, colums[key] )

        sql = self.remove_conma( sql )
        sql += ');'
        
        with self.conn.cursor() as cur:
            cur.execute( sql )

        self.conn.commit()

    def select_data( self, sql ):
        cur = self.conn.cursor( cursor_factory=DictCursor )
        cur.execute( sql )
        row = cur.fetchall()
        return row
