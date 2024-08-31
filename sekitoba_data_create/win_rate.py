import copy

import sekitoba_library as lib
import sekitoba_data_manage as dm
import sekitoba_psql as ps

BABA = "baba"
PLACE = "place"
DIST = "dist"
LIMB = "limb"
BABA = "baba"
KIND = "kind"
WAKU = "waku"

class WinRate:
    def __init__( self, race_data: ps.RaceData ):
        self.race_data: ps.RaceData = race_data
        self.base_key_list = sorted( [ "place", "dist", "kind", "baba" ] )
        self.h_key_list = sorted( [ "limb", "waku" ] )
        self.rate_list = [ "one", "two", "three" ]
        self.use_key_list = []
        n = 0

        while 1:
            n += 1
            bit = self.bit_create( n, len( self.base_key_list ) )

            if bit == None:
                break

            key_name = ""
            str_data = ""

            for i in range( 0, len( bit ) ):
                if bit[i] == "0":
                    continue

                key_name += self.base_key_list[i] + "_"

            hn = 0

            while 1:
                hn += 1
                h_bit = self.bit_create( hn, len( self.h_key_list ) )

                if h_bit == None:
                    break

                use_key_name = copy.copy( key_name )

                for i in range( 0, len( h_bit ) ):
                    if h_bit[i] ==  "0":
                        continue

                    use_key_name += self.h_key_list[i] + "_"

                use_key_name = use_key_name[:-1]
                self.use_key_list.append( use_key_name )

    def bit_create( self, n, BN ):
        bit = f'{n:b}'
    
        if BN - len( bit ) < 0:
            return None

        return "0" * ( BN - len( bit ) ) + bit

    def data_get( self, limb, cd: lib.current_data ):
        rate_data = self.race_data.data["win_rate"]
        result = {}
        base_key_data = {}
        base_key_data[PLACE] = str( self.race_data.data["place"] )
        base_key_data[DIST] = str( int( lib.dist_check( self.race_data.data["dist"] ) ) )
        base_key_data[KIND] = str( self.race_data.data["kind"] )
        base_key_data[BABA] = str( self.race_data.data["baba"] )
        base_key_data[LIMB] = str( limb )
        base_key_data[WAKU] = str( int( cd.flame_number() / 4 ) )

        for use_key_name in self.use_key_list:
            split_name_list = use_key_name.split( "_" )
            str_data_name = ""

            for split_name in split_name_list:
                str_data_name += base_key_data[split_name] + "_"

            use_str_data = str_data_name[:-1]

            for rate_key in self.rate_list:
                name = use_key_name + "_" + rate_key
                result[name] = -1000

            if not use_key_name in rate_data or \
              not use_str_data in rate_data[use_key_name]:
                continue

            for rate_key in self.rate_list:
                name = use_key_name + "_" + rate_key
                result[name] = rate_data[use_key_name][use_str_data][rate_key]

        return result
