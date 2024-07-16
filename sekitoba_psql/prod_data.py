import copy
import json
import itertools

from sekitoba_psql.psql_control import PsqlControl

class ProdData:
    def __init__( self ):
        self.pc = PsqlControl()
        self.table_name = "prod_data"
        self.prod_id = 1
        self.colums = { "prod_id": "int" }
        self.additional_colums = { "flame_evaluation": "text",
                                  "up_kind_ave": "text",
                                  "up3_analyze": "text",
                                  "money_class_true_skill": "text",
                                  "waku_three_rate": "text",
                                  "up_pace_regressin": "text",
                                  "flame_evaluation": "text",
                                  "race_time_analyze": "text",
                                  "stride_ablity_analyze": "text",
                                  "dist_index": "text",
                                  "standard_time": "text",
                                  "up3_standard_time": "text" }
        self.json_data = [ "flame_evaluation",
                          "up_kind_ave",
                          "up3_analyze",
                          "money_class_true_skill",
                          "waku_three_rate",
                          "up_pace_regressin",
                          "flame_evaluation",
                          "race_time_analyze",
                          "stride_ablity_analyze",
                          "dist_index",
                          "standard_time",
                          "up3_standard_time" ]
        self.data = {}

    def get_all_data( self ):
        self.data.clear()
        sql = "SELECT * from {} where prod_id = {};".format( self.table_name, self.prod_id )
        self.data = self.pc.select_data( sql )[0]

        for k in self.data.keys():
            if k in self.json_data:
                self.data[k] = json.loads( self.data[k] )

    def create_table( self ):
        if not self.pc.exist_table( self.table_name ):
            self.pc.create_table( self.table_name, self.colums )
            self.pc.update_data( "create index on race_data(race_id);" )

    def add_colum( self, colum_name, init_value ):
        if not self.pc.exist_colum( self.table_name, colum_name ):
            self.pc.add_colum( self.table_name, { "name": colum_name, "type": self.additional_colums[colum_name] }, init_value )

    def update_data( self, colum_name, value ):
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE prod_id={};"\
            .format( self.table_name, colum_name, value, self.prod_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE race_id={};"\
            .format( self.table_name, colum_name, value, self.prod_id )

        self.pc.update_data( sql )

    def insert_data( self ):
        insert_data = []

        if not self.pc.exist_data( self.table_name, "prod_id", self.prod_id ):
            insert_data.append( { "prod_id": self.prod_id } )

        if len( insert_data ) == 0:
            return
                
        self.pc.insert_data( self.table_name, insert_data, self.colums )
