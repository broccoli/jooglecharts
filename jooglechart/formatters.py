'''
Created on Nov 5, 2016

@author: richd
'''

from utils import JoogleChartsException, get_joogle_object_counter


class Formatter():

    FORMATTER_TYPES = ['ArrowFormat', 'BarFormat', 'ColorFormat', 'DateFormat', 'NumberFormat', 'PatternFormat']
    FORMATTER_TYPES_LOWER = ['arrow', 'bar', 'color', 'date', 'number', 'pattern']


    def __init__(self, type=None, options=None, cols=None, source_cols=None, dest_col=None, pattern=None):


        # validate formatter type
        try:
            formatter_ix = self.FORMATTER_TYPES.index(type)
        except ValueError:
            try:
                formatter = type.lower()
                formatter_ix = self.FORMATTER_TYPES_LOWER.index(formatter)
            except ValueError:
                message = "Format type submitted is not valid"
                raise JoogleChartsException(message)

        type = self.FORMATTER_TYPES[formatter_ix]

        if type == "ColorFormat":
            message = "ColorFormat is not currently supported"
            raise JoogleChartsException(message)


        if type == 'PatternFormat':
            if source_cols is None or pattern is None:
                message = "PatternFormat requires source_cols and pattern"
                raise JoogleChartsException(message)
        elif cols is None or options is None:
            message = "This format requires options and cols"
            raise JoogleChartsException(message)


        self.type = type
        self.options = options
        if isinstance(cols, int):
            cols = [cols]
        self.cols = cols
        self.source_cols = source_cols
        if self.type == "PatternFormat" and dest_col == None:
            self.dest_col = self.source_cols[0]
        else:
            self.dest_col = dest_col
        self.pattern = pattern

        self.num = get_joogle_object_counter()
        self.name = "formatter" + str(self.num)


