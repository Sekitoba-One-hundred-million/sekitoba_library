import copy
import json
import itertools

from sekitoba_psql.psql_control import PsqlControl

class RaceData:
    def __init__( self ):
        self.pc = PsqlControl()
        self.table_name = "race_data"
        self.colums = { "race_id": "text" }
        self.additional_colums = { "kind": "int", \
                                  "baba": "int", \
                                  "dist": "int", \
                                  "baba": "int", \
                                  "place": "int", \
                                  "out_side": "boolean", \
                                  "direction": "int", \
                                  "year": "int", \
                                  "month": "int", \
                                  "day": "int", \
                                  "money": "int", \
                                  "standard_time": "text", \
                                  "up3_standard_time": "text", \
                                  "up3_analyze": "text", \
                                  "dist_index": "text", \
                                  "wrap": "text", \
                                  "predict_netkeiba_pace": "text", \
                                  "up_pace_regressin": "text", \
                                  "up_kind_ave": "text", \
                                  "money_class_true_skill": "text", \
                                  "race_ave_true_skill": "float(32)", \
                                  "race_time_analyze": "text", \
                                  "waku_three_rate": "text", \
                                  "corner_horce_body": "text", \
                                  "predict_netkeiba_deployment": "text", \
                                  "first_up3_halon": "text", \
                                  "stride_ablity_analyze": "text", \
                                  "flame_evaluation": "text" }
        self.json_data = [ "standard_time", \
                          "up3_standard_time", \
                          "up3_analyze", \
                          "dist_index", \
                          "wrap", \
                          "up_pace_regressin", \
                          "up_kind_ave", \
                          "money_class_true_skill", \
                          "race_time_analyze", \
                          "waku_three_rate", \
                          "corner_horce_body", \
                          "predict_netkeiba_deployment", \
                          "first_up3_halon", \
                          "stride_ablity_analyze", \
                          "flame_evaluation" ]
        self.data = {}

    def get_all_data( self, race_id ):
        self.data.clear()
        sql = "SELECT * from race_data where race_id = '{}';".format( race_id )
        self.data = self.pc.select_data( sql )[0]

        for k in self.data.keys():
            if k in self.json_data:
                self.data[k] = json.loads( self.data[k] )

    def get_select_data( self, data_name ):
        result = {}
        key_list = data_name.split( "," )
        sql = "SELECT race_id, {} from race_data;".format( data_name )
        data_list = self.pc.select_data( sql )

        for data in data_list:
            race_id = data["race_id"]
            result[race_id] = {}
            
            for key in key_list:
                if data_name in self.json_data:
                    result[race_id][key] = json.loads( data[key] )
                else:
                    result[race_id][key] = data[key]
                
        return result

    def get_all_race_id( self ):
        sql = "SELECT race_id from race_data;"
        return list( itertools.chain.from_iterable( self.pc.select_data( sql ) ) )

    def create_table( self ):
        if not self.pc.exist_table( self.table_name ):
            self.pc.create_table( self.table_name, self.colums )
            self.pc.update_data( "create index on race_data(race_id);" )

    def add_colum( self, colum_name, init_value ):
        if not self.pc.exist_colum( self.table_name, colum_name ):
            self.pc.add_colum( self.table_name, { "name": colum_name, "type": self.additional_colums[colum_name] }, init_value )

    def update_data( self, colum_name, value, race_id ):
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE race_id='{}';"\
            .format( self.table_name, colum_name, value, race_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE race_id='{}';"\
            .format( self.table_name, colum_name, value, race_id )

        self.pc.update_data( sql )

    def update_race_data( self, colum_name, value, race_id ):
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE race_id='{}';"\
            .format( self.table_name, colum_name, value, race_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE race_id='{}';"\
            .format( self.table_name, colum_name, value, race_id )
            
        self.pc.update_data( sql )

    def insert_data( self, race_data ):
        import sekitoba_library as lib
        insert_data = []

        for k in race_data.keys():
            race_id = lib.id_get( k )
            
            if not self.pc.exist_data( self.table_name, "race_id", race_id ):
                insert_data.append( { "race_id": lib.id_get( k ) } )

        if len( insert_data ) == 0:
            return
                
        self.pc.insert_data( self.table_name, insert_data, self.colums )
