import os
import datetime
import pandas as pd
import lightgbm as lgb
import numpy as np
import matplotlib.pyplot as plt

class Logger:
    def __init__( self ):
        dt_now = datetime.datetime.now()
        self.log_dir = os.environ["HOME"] + "/Desktop/sekitoba_data/" + dt_now.strftime('%Y-%m-%d_%H:%M:%S')
        self.w = True

    def set_name( self, log_name ):
        self.log_dir = self.log_dir + log_name

    def set_write( self, w ):
        self.w = w
        
    def write( self, text ):
        if not self.w:
            return
            
        os.makedirs( self.log_dir,  exist_ok = True )
        file_name = "sekitoba.log"
        dt_now = datetime.datetime.now()
        time_str = dt_now.strftime('%Y-%m-%d_%H:%M:%S')
        f = open( self.log_dir + "/" + file_name, "a" )
        f.write( time_str + " " )
        f.write( text )
        f.write( "\n" )
        f.close()

    def write_lightbgm( self, bst ):
        os.makedirs( self.log_dir,  exist_ok = True )
        lgb.plot_tree( bst, figsize=(200, 200) )
        plt.savefig( self.log_dir + "/tree.png" )
        plt.close()
        df = bst.trees_to_dataframe()
        df.to_csv( self.log_dir + "/tree.csv" )
        
        f_importance = np.array( bst.feature_importance() )
        x_list = np.array( range( len( f_importance ) ) )
        f_importance = f_importance / np.sum( f_importance )
        df_importance = pd.DataFrame( { 'feature':x_list, 'importance':f_importance } )
        df_importance = df_importance.sort_values( 'importance', ascending = False )
        df_importance.to_csv( self.log_dir + "/feature_importance.csv" )

    def plot( self, x, y, name ):
        os.makedirs( self.log_dir,  exist_ok = True )        
        plt.plot( x, y )
        plt.savefig( self.log_dir + "/" + name + ".png" )
        plt.close()

    def scatter( self, x, y, name ):
        os.makedirs( self.log_dir,  exist_ok = True )        
        plt.scatter( x, y )
        plt.savefig( self.log_dir + "/" + name + ".png" )
        plt.close()
