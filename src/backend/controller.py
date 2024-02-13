from .data import Data


class DataController:
    @classmethod
    def merge(cls, df_to_merge, table):
        table.mdl.beginResetModel()
        Data.merge(df_to_merge)
        table.mdl._data = Data.df
        table.mdl.endResetModel()
