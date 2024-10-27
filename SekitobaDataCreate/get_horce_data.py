import SekitobaLibrary as lib

class GetHorceData:
    def __init__( self, cd: lib.CurrentData, pd: lib.PastData ):
        self.cd: lib.CurrentData = cd
        self.pd: lib.PastData = pd
        self.before_cd = pd.beforeCd()
        self.race_id = self.cd.raceId()
        self.limb_math = int( lib.limbSearch( pd ) )
        self.horce_num = int( cd.horceNumber() )
        self.key_day = str( int( self.race_id[9] ) )
        self.key_flame_number = str( int( self.cd.flameNumber() / 2 ) )
        self.key_place = str( int( self.cd.place() ) )
        self.key_kind = str( int( self.cd.raceKind() ) )
        self.key_dist = str( int( cd.dist() * 1000 ) )
        self.key_baba = str( int( cd.babaStatus() ) )
        self.key_limb = str( self.limb_math )
        self.key_horce_num = str( self.horce_num )
        self.key_waku = ""
        self.year = self.race_id[0:4]
        self.before_year = int( self.year ) - 1
        self.key_before_year = str( int( self.before_year ) )
        self.waku_three_key_list = [ "place", "dist", "limb", "baba", "kind" ]

        if cd.horceNumber() < cd.allHorceNum() / 2:
            self.key_waku = "1"
        else:
            self.key_waku = "2"

    def getCurrentPassingRank( self ):
        last_passing_rank = lib.escapeValue
        first_passing_rank = lib.escapeValue

        try:
            last_passing_rank = int( self.cd.passingRank().split( "-" )[-1] )
        except:
            pass

        try:
            first_passing_rank = int( self.cd.passingRank().split( "-" )[0] )
        except:
            pass
        
        return first_passing_rank, last_passing_rank

    def getBeforeDiff( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.before_cd.diff()

    def getBeforeFirstLastDiff( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.before_cd.firstLastDiff()

    def getBeforeIdWeight( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.before_cd.idWeight()

    def getBeforePopular( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.before_cd.popular()

    def getBeforeRank( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.before_cd.rank()

    def getBeforeSpeed( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.before_cd.speed()

    def getPopularRank( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return abs( self.before_cd.rank() - self.before_cd.popular() )

    def getDiffLoadWeight( self ):
        if self.before_cd is None:
            return lib.escapeValue

        return self.cd.burdenWeight() - self.before_cd.burdenWeight()

    def getUp3StandardValue( self ):
        if self.before_cd is None:
            return lib.escapeValue

        p1, p2 = self.before_cd.pace()
        up3 = self.before_cd.upTime()
        return max( min( ( up3 - p2 ) * 5, 15 ), -10 )

    def getWeightScore( self ):
        return self.cd.weight() / 10

    def getBeforePassingRank( self ):
        before_first_passing_rank = lib.escapeValue
        before_last_passing_rank = lib.escapeValue

        if self.before_cd is None:
            return before_first_passing_rank, before_last_passing_rank

        before_passing_list = self.before_cd.passingRank().split( "-" )
        
        try:
            before_first_passing_rank = int( before_passing_list[0] )
        except:
            pass
        
        try:
            before_last_passing_rank = int( before_passing_list[-1] )
        except:
            pass
        
        return before_first_passing_rank, before_last_passing_rank

    def getFlameEvaluation( self, flame_evaluation_data ):
        e_one = -1
        e_two = -1
        e_three = -1

        try:
            e_one = \
              flame_evaluation_data[self.key_place][self.key_day][self.key_flame_number]["one"]
            e_two = \
              flame_evaluation_data[self.key_place][self.key_day][self.key_flame_number]["two"]
            e_three = \
              flame_evaluation_data[self.key_place_num][self.key_day][self.key_flame_number]["three"]
        except:
            pass

        return e_one, e_two, e_three

    def getStraightDist( self, race_cource_info ):
        first_straight_dist = -1000
        last_straight_dist = -1000

        try:
            first_straight_dist = race_cource_info[self.key_place][self.key_kind][self.key_dist]["dist"][0]
            last_straight_dist = race_cource_info[self.key_place][self.key_kind][self.key_dist]["dist"][-1]
        except:
            pass

        return first_straight_dist, last_straight_dist

    def getKindScore( self, waku_three_rate, kind_key_data = {} ):
        score = 0
        count = 0
        kind_key_data = {}

        if len( kind_key_data ) == 0:
            kind_key_data["place"] = self.key_place
            kind_key_data["dist"] = self.key_dist
            kind_key_data["baba"] = self.key_baba
            kind_key_data["kind"] = self.key_kind
            kind_key_data["limb"] = self.key_limb
    
        for i in range( 0, len( self.waku_three_key_list ) ):
            k1 = self.waku_three_key_list[i]
        
            for r in range( i + 1, len( self.waku_three_key_list ) ):
                k2 = self.waku_three_key_list[r]
                key_name = k1 + "_" + k2

                try:
                    score += waku_three_rate[key_name][kind_key_data[k1]][kind_key_data[k2]][self.key_waku]
                    count += 1
                except:
                    continue

        if not count == 0:
            score /= count
        
        return score

    def getFirstHorceBody( self ):
        past_min_first_horce_body = -1000
        past_max_first_horce_body = -1000
        past_ave_first_horce_body = -1000
        past_std_first_horce_body = -1000
        past_first_horce_body_list = self.pd.past_first_horce_body_list()

        if not len( past_first_horce_body_list ) == 0:
            past_min_first_horce_body = lib.minimum( past_first_horce_body_list )
            past_max_first_horce_body = max( past_first_horce_body_list )
            past_ave_first_horce_body = lib.average( past_first_horce_body_list )

            if len( past_first_horce_body_list ) > 1:
                past_std_first_horce_body = lib.stdev( past_first_horce_body_list )

        return past_min_first_horce_body, \
          past_max_first_horce_body, \
          past_ave_first_horce_body, \
          past_std_first_horce_body


    def getLastHorceBody( self ):
        past_min_last_horce_body = -1000
        past_max_last_horce_body = -1000
        past_ave_last_horce_body = -1000
        past_std_last_horce_body = -1000
        past_last_horce_body_list = self.pd.past_last_horce_body_list()

        if not len( past_last_horce_body_list ) == 0:
            past_min_last_horce_body = lib.minimum( past_last_horce_body_list )
            past_max_last_horce_body = max( past_last_horce_body_list )
            past_ave_last_horce_body = lib.average( past_last_horce_body_list )

            if len( past_last_horce_body_list ) > 1:
                past_std_last_horce_body = lib.stdev( past_last_horce_body_list )

        return past_min_last_horce_body, \
          past_max_last_horce_body, \
          past_ave_last_horce_body, \
          past_std_last_horce_body

    def getPredictPace( self, predict_pace ):
        result = {}
        
        for pace_key in lib.predict_pace_key_list:
            if pace_key in predict_pace:
                result["predict_"+pace_key] = predict_pace[pace_key]
            else:
                result["predict_"+pace_key] = lib.escapeValue

        return result
