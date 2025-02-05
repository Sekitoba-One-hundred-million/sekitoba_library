import SekitobaLibrary as lib
import SekitobaDataManage as dm

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "wrap_data.pickle" )

class BeforeData:
    def __init__( self ):
        self.race_data = dm.dl.data_get( "race_data.pickle" )
        self.horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
        self.wrap_data = dm.dl.data_get( "wrap_data.pickle" )

    def up3_rank( self, before_cd: lib.CurrentData ):
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
            cd = lib.CurrentData( current_data )

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

    def pace( self, before_race_id, prod_before_wrap = None ):
        score = -1

        if dm.dl.prod:
            before_wrap = prod_before_wrap
        else:
            try:
                before_wrap = self.wrap_data[before_race_id]
            except:
                return score

        wrap_list = []

        for dk in before_wrap.keys():
            if dk == "100":
                wrap_list.append( before_wrap[dk] )
            else:
                wrap_list.append( before_wrap[dk] / 2 )
                wrap_list.append( before_wrap[dk] / 2 )

        n = len( wrap_list )
        p1 = int( n / 2 )
        p2 = p1 + ( n % 2 )
        pace = ( sum( wrap_list[0:p1] ) - sum( wrap_list[p2:n] ) )
        score = 0
        
        if pace < -1:
            score = 1
        elif 1 < pace:
            score = 2

        return score
