import os
import pickle

import SekitobaDataManage as dm
from concurrent.futures import ThreadPoolExecutor

class data_load():
    def __init__( self ):
        self.file_list = {} #ここに呼び出すファイルをセットする
        self.data = {} #ダウンロードされたデータが入る
        self.dir_name = "./storage"
        self.prod = False

    def file_set( self, file_name ):
        if file_name not in self.data:
            self.file_list[file_name] = False

    def data_get( self, file_name ):
        self.file_set( file_name )
        self.local_download()
        self.multi_load()
        
        try:
            return self.data[file_name]
        except:
            return None

    def prod_on( self ):
        self.prod = True

    def data_clear( self ):
        self.data.clear()

    def local_keep( self ):
        self.multi_load()
        os.makedirs( self.dir_name,  exist_ok = True )
        
        for file_name in self.data.keys():
            f = open( self.dir_name + "/" + file_name, "wb" )
            pickle.dump( self.data[file_name], f )
            f.close()

    def local_download( self ):
        current_load = []

        for k in self.file_list.keys():
            if not self.file_list[k]:
                current_load.append( k )

        for file_name in current_load:
            try:
                f = open( self.dir_name + "/" + file_name, "rb" )
                self.data[file_name] = pickle.load( f )
                f.close()
                self.file_list[file_name] = True
            except:
                continue
            
    def multi_load( self ):
        current_load = []

        for k in self.file_list.keys():
            if not self.file_list[k]:
                current_load.append( [ k ] )

        if len( current_load ) == 0:
            return

        for k_list in current_load:
            name, d = self.jisaku_func( k_list[0] )
            self.data[name] = d
            self.file_list[name] = True

        return
        """
        thread_count = min( len( current_load ), 5 )
        # スレッドプールを作ります。
        # プロセスプールとちがって、スレッドの数は
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            # 『関数』と『引数リスト』を渡して、実行します。
            results = executor.map(
                self.jisaku_func_wrapper, current_load, timeout=None )
            
            for result in results:
                self.data[result[0]] = result[1]
                self.file_list[result[0]] = True
        """

    def jisaku_func_wrapper( self, args ):
        return self.jisaku_func(*args)

    def jisaku_func( self, file_name ):
        result = {}
        
        if file_name == "dist_index.txt":
            result = dm.dist_index_get()
        elif file_name == "straight_dist.txt":
            result = dm.course_data_get();
        else:
            result = dm.pickle_load( file_name, prod = self.prod )

        return ( file_name, result )
