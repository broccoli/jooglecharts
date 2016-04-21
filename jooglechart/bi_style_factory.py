



def get_styler(size="medium", legend_position="top"):
    
    CHARTAREA_TOP = 60
    H_CHARTAREA_LEFT = 60
    H_WIDTH_SMALL = 350
    H_WIDTH_MEDIUM = 500
    H_WIDTH_LARGE = 1000
    RIGHT_LEGEND_SPACE = 120

    h_width_dict = {'small': H_WIDTH_SMALL, 'medium': H_WIDTH_MEDIUM, 'large': H_WIDTH_LARGE}
    
    # basic options common to all charts
    basic_opts = {}
    basic_opts['fontName'] = 'Helvetica Neue'
    basic_opts['fontSize'] = 12
    basic_opts['titleTextStyle.fontSize'] = 16
    basic_opts['hAxis.titleTextStyle.bold'] = True
    basic_opts['hAxis.titleTextStyle.italic'] = False
    basic_opts['vAxis.titleTextStyle.bold'] = True
    basic_opts['vAxis.titleTextStyle.italic'] = False
    
    
    horizontal_chart_types = ['ColumnChart', 'LineChart', 'AreaChart']
    
    def has_h_axis(chart_type):
        
        if chart_type in horizontal_chart_types:
            return True
    
    def get_width_options(chart_type, legend_position, size):
        
        # get width, chartArea.left, chartArea.width
        
        width = h_width_dict[size]
        if has_h_axis(chart_type):
            ca_left = H_CHARTAREA_LEFT
        else:
            ca_left = 0
        if legend_position == 'right':
            right_space = RIGHT_LEGEND_SPACE
        else:
            right_space = 0
        ca_width = width - ca_left - right_space
        
        width_opts = {}
        width_opts['width'] = width
        width_opts['chartArea.left'] = ca_left
        width_opts['chartArea.width'] = ca_width
        
        return width_opts
    
    
    def calculate_bar_group_width(num_rows, num_series, chart_width):
    
        MAX_BGW_RATIO = .15     # largest size bar
        BASE_GAP_FACTOR = .6    # ratio of bar size to gap size
        SERIES_GAP_FACTOR = .2  # factor by which to decrease gap for additional series
        MIN_GAP_RATIO = .01     # smallest gap
        
        # modify gap factor for additional series
        modified_gap_factor = BASE_GAP_FACTOR * ((1 - SERIES_GAP_FACTOR) ** (num_series - 1))
        bar_group_width = chart_width / (num_rows * (1 + modified_gap_factor))
        
        
        max_bgw = MAX_BGW_RATIO * chart_width        
        if bar_group_width > max_bgw * num_series:
            # if a bar exceeds max size, compute bar group width based on max
            print "setting bgw to max"
            bar_group_width = max_bgw * num_series
        
        else:
            # if gap size is below minimum, compute group width based on minimum gap
            resulting_gap_width = bar_group_width * modified_gap_factor
            min_gap_width = MIN_GAP_RATIO * chart_width
            print "min_gap_width", min_gap_width
            if resulting_gap_width < min_gap_width: 
                print "resulting_gap_width", resulting_gap_width, " ----- resizing"
                bar_group_width = (chart_width - (num_rows * min_gap_width)) / num_rows
        
        return int(round(bar_group_width))
    
    def get_bar_group_width(jc, chart, size):
        
        is_stacked = chart.chart_options['isStacked']
        chart_width = chart.options['width']
        num_rows = jc._num_rows
        
        # get a count of the number of series, taking account of view cols and roles
        if is_stacked:
            num_series = 1
        else:
            if chart.view_cols:
                series_indexes = chart.view_cols[:]
            else:
                series_indexes = range(jc._num_columns)
            
            # remove role cols from series indexes
            if jc.roles:
                role_cols = [role[0] for role in jc.roles]
                for col in role_cols:
                    if col in series_indexes:
                        series_indexes.remove(col)
            
            # remove the category column -- first remaining series column
            series_indexes.pop(0)

            num_series = len(series_indexes)

        return calculate_bar_group_width(num_rows, num_series, chart_width)
    
    def styler(jc):

        for chart in jc.charts:
            
            chart_type = chart.chart_type
            
#             if chart_type in ['ColumnChart', 'BarChart']:
#                 chart.add_chart_options(get_bar_group_width(jc, chart))
            chart.add_chart_options(legend_position=legend_position)
            chart.add_chart_options(basic_opts)
            chart.add_chart_options(get_width_options(chart_type, legend_position), size)
            
            
#             print chart.chart_options
        
        return jc
    
    return styler