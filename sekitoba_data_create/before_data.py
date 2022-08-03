import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )


class BeforeData:
    def __init__( self ):
        self.race_data = dm.dl.data_get( "race_data.pickle" )
        self.horce_data = dm.dl.data_get( "horce_data_storage.pickle" )

    def up3_rank( self, before_cd: lib.current_data ):
        if before_cd == None:
            return 0
        
        before_race_id = before_cd.race_id()
        race_key = "https://race.netkeiba.com/race/shutuba.html?race_id=" + before_race_id

        try:
            horce_id_dict = self.race_data[race_key]
        except:
            return 0

        year = before_race_id[0:4]
        race_place_num = before_race_id[4:6]
        day = before_race_id[9]
        num = before_race_id[7]
        before_up3_list = []

        for horce_id in horce_id_dict.keys():
            current_data, past_data = lib.race_check( self.horce_data[horce_id],
                                                     year, day, num, race_place_num )
            cd = lib.current_data( current_data )

            if not cd.race_check():
                continue

            before_up3_list.append( cd.up_time() )

        score = 0
        before_my_up3 = before_cd.up_time()

        if not len( before_up3_list ) == 0:
            if not before_my_up3 in before_up3_list:
                before_up3_list.append( before_my_up3 )

            score = before_up3_list.index( before_my_up3 )

        score = max( score, 0 )
        return score
