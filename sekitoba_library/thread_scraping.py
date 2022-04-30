from concurrent.futures import ThreadPoolExecutor

class thread_scraping():
    def __init__( self, url_list, key_list ):
        self.url_list = url_list
        self.key_list = key_list

    def data_get( self, func ):
        result = {}
        use_data = []

        if not len( self.url_list ) == len( self.key_list ):
            print( "urlとkeyの数が違います" )
            return None

        N = len( self.url_list )
        
        for i in range( 0, N ):
            use_data.append( [ func, self.url_list[i], self.key_list[i], N - i ] )
        
        # スレッドプールを作ります。
        # プロセスプールとちがって、スレッドの数は
        with ThreadPoolExecutor( max_workers = 10 ) as executor:
            # 『関数』と『引数リスト』を渡して、実行します。
            results = executor.map(
                self.jisaku_func_wrapper, use_data, timeout=None )

            for data in results:
                result[data[0]] = data[1]

        return result
            
    def jisaku_func_wrapper( self, args ):
        return self.jisaku_func(*args)

    def jisaku_func( self, func, url, key, num ):
        print( num )
        result = func( url )
        
        return ( key, result )
            
