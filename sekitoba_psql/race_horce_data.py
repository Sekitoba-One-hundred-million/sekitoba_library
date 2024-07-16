import copy
import json
import itertools
import sekitoba_library as lib
from sekitoba_psql.psql_control import PsqlControl

class RaceHorceData:
    def __init__( self ):
        self.pc = PsqlControl()
        self.table_name = "race_horce_data"
        self.colums = { "race_id": "text", "horce_id": "text" }
        self.additional_colums = { "jockey_id": "text", \
                                  "trainer_id": "text", \
                                  "horce_true_skill": "float(32)", \
                                  "jockey_true_skill": "float(32)", \
                                  "trainer_true_skill": "float(32)", \
                                  "horce_first_passing_true_skill": "float(32)", \
                                  "jockey_first_passing_true_skill": "float(32)", \
                                  "trainer_first_passing_true_skill": "float(32)", \
                                  "horce_last_passing_true_skill": "float(32)", \
                                  "jockey_last_passing_true_skill": "float(32)", \
                                  "trainer_last_passing_true_skill": "float(32)", \
                                  "horce_up3_true_skill": "float(32)", \
                                  "jockey_up3_true_skill": "float(32)", \
                                  "trainer_up3_true_skill": "float(32)", \
                                  "horce_corner_true_skill": "float(32)", \
                                  "jockey_corner_true_skill": "float(32)", \
                                  "trainer_corner_true_skill": "float(32)", \
                                  "jockey_judgment": "text", \
                                  "jockey_judgment_up3": "text", \
                                  "trainer_judgment": "text", \
                                  "trainer_judgment_up3": "text", \
                                  "jockey_judgment_rate": "text", \
                                  "jockey_judgment_up3_rate": "text", \
                                  "trainer_judgment_rate": "text", \
                                  "next_race": "text" }
        self.json_data = [ "jockey_judgment", \
                          "jockey_judgment_up3", \
                          "trainer_judgment", \
                          "trainer_judgment_up3", \
                          "jockey_judgment_rate", \
                          "jockey_judgment_up3_rate", \
                          "trainer_judgment_rate", \
                          "next_race" ]
        self.data = {}
        self.horce_id_list = []
        self.trainer_id_list = []
        self.jockey_id_list = []

    def get_all_data( self, race_id ):
        self.data.clear()
        self.horce_id_list.clear()
        self.trainer_id_list.clear()
        self.jockey_id_list.clear()
        sql = "SELECT * from {} where race_id = '{}';".format( self.table_name, race_id )
        select_data = self.pc.select_data( sql )
        
        for sd in select_data:
            horce_id = sd["horce_id"]
            self.data[horce_id] = sd
            self.horce_id_list.append( horce_id )
            self.trainer_id_list.append( sd["trainer_id"] )
            self.jockey_id_list.append( sd["jockey_id"] )

            for k in self.data[horce_id].keys():
                if k in self.json_data:
                    self.data[horce_id][k] = json.loads( self.data[horce_id][k] )            

    def get_select_data( self, data_name, distinct = "" ):
        result = {}
        sql = "SELECT {} race_id, {} from {};".format( distinct, data_name, self.table_name )
        return self.pc.select_data( sql )

    def get_horce_id( self, race_id ):
        sql = "SELECT horce_id from {} where race_id = '{}';".format( self.table_name, race_id )
        return list( itertools.chain.from_iterable( self.pc.select_data( sql ) ) )

    def create_table( self ):
        if not self.pc.exist_table( self.table_name ):
            self.pc.create_table( self.table_name, self.colums )
            self.pc.update_data( "create index on race_horce_data(race_id);" )
            self.pc.update_data( "create index on race_horce_data(horce_id);" )

    def add_colum( self, colum_name, init_value ):
        if not self.pc.exist_colum( self.table_name, colum_name ):
            self.pc.add_colum( self.table_name, { "name": colum_name, "type": self.additional_colums[colum_name] }, init_value )

    def update_data( self, colum_name, value, race_id, horce_id, id_name = "horce_id" ):
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE race_id='{}' AND {}='{}';"\
            .format( self.table_name, colum_name, value, race_id, id_name, horce_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE race_id='{}' AND {}='{}';"\
            .format( self.table_name, colum_name, value, race_id, id_name, horce_id )

        self.pc.update_data( sql )

    def insert_data( self, race_data ):
        insert_data = []

        for k in race_data.keys():
            race_id = lib.id_get( k )
            
            if self.pc.exist_data( self.table_name, "race_id", race_id ):
                continue

            for horce_id in race_data[k].keys():
                insert_data.append( { "race_id": race_id, "horce_id": horce_id } )

        self.pc.insert_data( self.table_name, insert_data, self.colums )
