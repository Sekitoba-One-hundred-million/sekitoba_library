def dist_check( di ):
    if di < 1400:#短距離
        return 1
    elif di < 1800:#マイル
        return 2
    elif di < 2200:#中距離
        return 3
    elif di < 2800:#中長距離
        return 4
    else:#長距離
        return 5

def weather( we ):
    if we == "晴":
        return 1
    elif we == "曇":
        return 2
    elif we == "雨":
        return 3
    elif we == "小雨":
        return 4
    else:
        return 0

def baba_index( baba ):
    if len( baba ) == 0:
        return 0
    elif baba == "良":
        return -10
    elif baba == "稍":
        return -5
    elif baba == "重":
        return 5
    elif baba == "不":
        return 10

    return 0

def sex_num( str_sex ):
    if str_sex == "牡":
        return 1
    elif str_sex == "牝":
        return 2

    return 0

def money_class_get( money ):
    money_class = 0

    if money <= 501:
        money_class = 1
    elif money < 1000:
        money_class = 2
    elif money < 1600:
        money_class = 3
    else:
        money_class = 4

    return money_class    

def k_dist( kd ):
    str_d = ""
    d = 0.0

    for i in range( 0, len( kd ) ):
        if str.isdecimal( kd[i] ):
            str_d += kd[i]
            
    if not len( str_d ) == 0:
        d = float( str_d ) / 1000
        
    return d

def dist( d ):
    if d == "":
        return 0, 0
    
    d_type = d[0]
    di = ""#float( d[1:len(d)] )

    for i in range( 0, len( d ) ):
        if str.isdecimal( d[i] ):
            di += d[i]

    if len( di ) == 0:
        return 0, 0

    di = float( di )

    t = 0#芝は1

    if d_type == "ダ":#ダートかどうかの判断
        t = 2#ダートなら2
    elif d_type == "障":
        t = 3
    elif d_type == "芝":
        t = 1

    if di < 1400:#短距離
        return 1, t
    elif di < 1800:#マイル
        return 2, t
    elif di < 2200:#中距離
        return 3, t
    elif di < 2800:#中長距離
        return 4, t
    else:#長距離
        return 5, t

def time( t ):
    if t == "":
        return 0
    
    tt = t.split( ":" )

    if not str.isdecimal( tt[0] ):
        return 0
    m = float( tt[0] )
    m += float( tt[1] ) / 60
    m = round( m, 4 )
    return m

def place_num( place ):
    pl = ""
    
    for i in range( 0, len( place ) ):
        if not str.isdecimal( place[i] ):
            pl += place[i]

    if pl == "札幌":
        return 1
    elif pl == "函館":
        return 2
    elif pl == "福島":
        return 3
    elif pl == "新潟":
        return 4
    elif pl == "東京":
        return 5
    elif pl == "中山":
        return 6
    elif pl == "中京":
        return 7
    elif pl == "京都":
        return 8
    elif pl == "阪神":
        return 9
    elif pl == "小倉":
        return 10
    else:
        return 0

def stright_slope( place_num ):
    if place_num == 1 or place_num == 2 or place_num == 3 or \
      place_num == 4 or place_num == 8 or place_num == 10:
        return 1 # 平坦
    elif place_num == 5:
        return 2 # やや坂
    elif place_num == 6 or place_num == 7 or place_num == 9:
        return 2 # 急坂

    return 0

def baba( b ):
    if b == "良":
        return 1
    elif b == "重":
        return 2
    elif b == "稍":
        return 3
    elif b == "不":
        return 4
    else:
        return 0

def weight( w ):
    w = w.replace( ")", "" )
    ww = w.split( "(" )

    if len( ww ) != 2:
        return 0

    if ww[1][0] == "0":
        return 0
    
    if str.isdecimal( ww[1][1] ):
        return float( ww[1] )

    return 0

def data_check( d ):
    try:
        return float( d )
    except:
        return 0

def netkeiba_pace( str_pace ):
    if str_pace == "S":
        return 1
    elif str_pace == "M":
        return 2
    elif str_pace == "H":
        return 3
    
    return -1
