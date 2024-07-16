import json
import itertools

import sekitoba_library as lib
from sekitoba_psql.psql_control import PsqlControl

class TrainerData:
    def __init__( self ):
        self.pc = PsqlControl()
        self.table_name = "trainer_data"
        self.colums = { "trainer_id": "text" }
        self.additional_colums = { "true_skill": "float(32)", \
                                  "first_passing_true_skill": "float(32)", \
                                  "last_passing_true_skill": "float(32)", \
                                  "up3_true_skill": "float(32)", \
                                  "corner_true_skill": "float(32)", \
                                  "trainer_judgment": "text", \
                                  "trainer_judgment_up3": "text", \
                                  "trainer_judgment_rate": "text", \
                                  "trainer_analyze": "text" }
        self.json_data = [ "trainer_judgment", \
                          "trainer_judgment_rate", \
                          "trainer_analyze", \
                          "trainer_judgment_up3" ]
        self.data = {}

    def get_multi_data( self, trainer_id_list ):
        self.data.clear()
        sql = "SELECT * from {} where ".format( self.table_name )
        
        for i, trainer_id in enumerate( trainer_id_list ):
            sql += "trainer_id = '{}'".format( trainer_id )

            if not i == len( trainer_id_list ) - 1:
                sql += " OR "

        sql += ";"
        get_data = self.pc.select_data( sql )

        for past_data in get_data:
            for key in past_data.keys():
                if key in self.json_data:
                    past_data[key] = json.loads( past_data[key] )
                    
            self.data[past_data["trainer_id"]] = past_data

    def get_select_all_data( self, data_name ):
        result = {}
        sql = "SELECT trainer_id, {} from {};".format( data_name, self.table_name )
        data_list = self.pc.select_data( sql )

        for data in data_list:
            result[data[0]] = data[1]

        return result

    def create_table( self ):
        if not self.pc.exist_table( self.table_name ):
            self.pc.create_table( self.table_name, self.colums )
            self.pc.update_data( "create index on trainer_data(trainer_id);" )

    def add_colum( self, colum_name, init_value ):
        if not self.pc.exist_colum( self.table_name, colum_name ):
            self.pc.add_colum( self.table_name, { "name": colum_name, "type": self.additional_colums[colum_name] }, init_value )

    def update_data( self, colum_name, value, trainer_id ):
        sql = ""
        
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE trainer_id='{}';"\
            .format( self.table_name, colum_name, value, trainer_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE trainer_id='{}';"\
            .format( self.table_name, colum_name, value, trainer_id )
            
        self.pc.update_data( sql )

    def insert_data( self, trainer_id_list ):
        insert_data = []

        for trainer_id in trainer_id_list:
            if not self.pc.exist_data( self.table_name, "trainer_id", trainer_id ):
                insert_data.append( { "trainer_id": trainer_id } )

        if len( insert_data ) == 0:
            return

        self.pc.insert_data( self.table_name, insert_data, self.colums )
