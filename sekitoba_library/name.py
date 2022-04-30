class Name:
    def __init__( self ):
        self.name = ""

    def set_name( self, name ):
        self.name = name

    def model_name( self ):
        return self.name + "_model.pickle"

    def data_name( self ):
        return self.name + "_learn_data.pickle"

    def simu_name( self ):
        return self.name + "_simu_data.pickle"

    def score_name( self ):
        return self.name + "_score.pickle"

    def memo_name( self ):
        return self.name + "_learn_memo.txt"
