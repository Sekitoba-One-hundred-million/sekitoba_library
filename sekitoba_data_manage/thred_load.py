import sekitoba_data_manage as dm
from concurrent.futures import ThreadPoolExecutor

class data_load():
    def __init__( self ):
        self.file_list = {} #ここに呼び出すファイルをセットする
        self.data = {} #ダウンロードされたデータが入る

    def file_set( self, file_name ):
        if file_name not in self.data.keys():
            self.file_list[file_name] = False

    def data_get( self, file_name ):
        self.file_set( file_name )
        self.multi_load()
        
        try:
            return self.data[file_name]
        except:
            return None

    def data_clear( self ):
        self.data.clear()
        
    def multi_load( self ):
        current_load = []

        for k in self.file_list.keys():
            if not self.file_list[k]:
                current_load.append( [ k ] )

        if len( current_load ) == 0:
            return
        
        # スレッドプールを作ります。
        # プロセスプールとちがって、スレッドの数は
        with ThreadPoolExecutor(max_workers=5) as executor:
            # 『関数』と『引数リスト』を渡して、実行します。
            results = executor.map(
                self.jisaku_func_wrapper, current_load, timeout=None )
        
            for result in results :
                self.data[result[0]] = result[1]
                self.file_list[result[0]] = True

    def jisaku_func_wrapper( self, args ):
        return self.jisaku_func(*args)

    def jisaku_func( self, file_name ):
        result = {}
        
        if file_name == "dist_index.txt":
            result = dm.dist_index_get()
        elif file_name == "straight_dist.txt":
            result = dm.course_data_get();
        else:
            result = dm.pickle_load( file_name )

        return ( file_name, result )



