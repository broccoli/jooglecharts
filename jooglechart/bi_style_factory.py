



def get_styler(size="medium", legend_position="top", debug=False):
    
    H_WIDTH_SMALL = 350
    H_WIDTH_MEDIUM = 500
    H_WIDTH_LARGE = 1000

    TOP_SPACE_MIN = 10
    TOP_SPACE_TITLE = 25
    TOP_SPACE_LEGEND = 30
    
    H_CHARTAREA_LEFT = 60
    V_CHARTAREA_LEFT = 100
    
    Y_AXIS_TITLE = 40
#     X_AXIS_TITLE = 40
    
    LEFT_SPACE_TITLE = 30
    RIGHT_SPACE_LEGEND = 120
    BOTTOM_SPACE_UNITS = 40
    BOTTOM_SPACE_CATEGORIES = 60
    BOTTOM_SPACE_TITLE = 15
    BASE_HEIGHT = 375

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
    
    
    horizontal_chart_types = ['ColumnChart', 'LineChart', 'AreaChart', 'ComboChart']
    vertical_chart_types = ['BarChart']
    
    def has_units_on_y_axis(chart_type):
        
        if chart_type in horizontal_chart_types:
            return True
    
    def get_width_options(chart, legend_position, size):
        
        
#         print chart_type
        # get width, chartArea.left, chartArea.width
        
        chart_type = chart.chart_type
        chart_opts = chart.chart_options
        
        # check for width
        try:
            width = chart_opts['width']
        except:
            width = h_width_dict[size]
        
        # get chartArea.left
        try:
            # check for custom chartArea.left
            ca_left = chart_opts['chartArea']['left']
        except:
            ca_left = 0
            if has_units_on_y_axis(chart_type):
                ca_left += H_CHARTAREA_LEFT
            elif chart_type in vertical_chart_types:
                ca_left += V_CHARTAREA_LEFT
            try:
                if 'title' in chart_opts['vAxis']:
                    ca_left += LEFT_SPACE_TITLE
            except:
                pass

        if legend_position == 'right':
            right_space = RIGHT_SPACE_LEGEND
        else:
            right_space = 0
        ca_width = width - ca_left - right_space
        
        width_opts = {}
        width_opts['width'] = width
        width_opts['chartArea.left'] = ca_left
        width_opts['chartArea.width'] = ca_width
        
        return width_opts
    
    
    def get_base_height_options(chart):
        
        chart_opts = chart.chart_options
        
        height_opts = {}
        height_opts['height'] = BASE_HEIGHT
        
        chartarea_top = TOP_SPACE_MIN
        if chart_opts.get('title'):
            chartarea_top += TOP_SPACE_TITLE
        try:
            if chart_opts['legend']['position'] == 'top':
                chartarea_top += TOP_SPACE_LEGEND
        except:
            pass
        
        height_opts['chartArea.top'] = chartarea_top
        
        chartarea_height = BASE_HEIGHT - chartarea_top
        try:
            if 'title' in chart_opts['hAxis']:
                chartarea_height -= BOTTOM_SPACE_TITLE
        except:
            pass
        if has_units_on_y_axis(chart.chart_type):
            chartarea_height -= BOTTOM_SPACE_CATEGORIES
        else:
            chartarea_height -= BOTTOM_SPACE_UNITS
    
        height_opts['chartArea.height'] = chartarea_height
            
        return height_opts
    
        
    
    def get_gap_ratio(num_series):
        
        # Determine ratio of bar group width to gap width.  Increase the ratio
        # as series get added.
    
        BASE_GAP_FACTOR = .6    # ratio of bar size to gap size
        SERIES_GAP_FACTOR = .2  # factor by which to decrease gap for each additional series
        modified_gap_ratio = BASE_GAP_FACTOR * ((1 - SERIES_GAP_FACTOR) ** (num_series - 1))
        
        return modified_gap_ratio
    
    def calculate_bar_group_width_for_column_chart(num_rows, num_series, chart):
    
        chart_width = chart.chart_options['chartArea']['width']
        
        MAX_BAR_RATIO = .15     # largest size bar
        MIN_GAP_RATIO = .01     # smallest gap
        
        # 1.  Get unrestricted bar gap width
        gap_ratio = get_gap_ratio(num_series)
        bar_group_width = chart_width / (num_rows * (1 + gap_ratio))
        
        # 2.  Check of bars are too thick
        max_bar_width = MAX_BAR_RATIO * chart_width        
        if bar_group_width > max_bar_width * num_series:
            # if a bar exceeds max size, compute bar group width based on max
            bar_group_width = max_bar_width * num_series
        
        # 3. Check if gap is too small
        else:
            # if gap size is below minimum, compute group width based on minimum gap
            resulting_gap_width = bar_group_width * gap_ratio
            min_gap_width = MIN_GAP_RATIO * chart_width
            if resulting_gap_width < min_gap_width: 
                bar_group_width = (chart_width - (num_rows * min_gap_width)) / num_rows
                
#         return int(round(bar_group_width))

        return bar_group_width
    
    def get_viewable_cols(jc, chart):

        if chart.view_cols:
            viewable_cols = chart.view_cols[:]
        else:
            viewable_cols = range(jc._num_cols)
        
        return viewable_cols
        
        
    def get_num_series(jc, chart):

        viewable_cols = get_viewable_cols(jc, chart)
                
        # remove role cols from series indexes
        if jc.roles:
            role_cols = [role[0] for role in jc.roles]
            for col in role_cols:
                if col in viewable_cols:
                    viewable_cols.remove(col)
        
        # remove the category column -- first remaining series column
        num_series = len(viewable_cols[1:])
        
        return num_series
        
    
    def get_num_series_for_combo_chart(jc, chart):
        
        num_series = get_num_series(jc, chart)
        
        # get the number of other series types
        try:
            other_series = len(chart.chart_options['series'].keys())
            num_series -= other_series
        except:
            pass

        return num_series
    
    def get_column_chart_options(jc, chart):
        
        is_stacked = chart.chart_options.get('isStacked', False)
        num_rows = jc._num_rows
        
        # get a count of the number of series, taking account of view cols and roles
        if is_stacked:
            num_series = 1
        elif chart.chart_type == "ComboChart":
            num_series = get_num_series_for_combo_chart(jc, chart)
        else:
            num_series = get_num_series(jc, chart)

        chart_width = chart.chart_options['chartArea']['width']
        
        MAX_BAR_RATIO = .15     # largest size bar
        MIN_GAP_RATIO = .01     # smallest gap
        
        # 1.  Get unrestricted bar gap width
        gap_ratio = get_gap_ratio(num_series)
        bar_group_width = chart_width / (num_rows * (1 + gap_ratio))
        
        # 2.  Check of bars are too thick
        max_bar_width = MAX_BAR_RATIO * chart_width        
        if bar_group_width > max_bar_width * num_series:
            # if a bar exceeds max size, compute bar group width based on max
            bar_group_width = max_bar_width * num_series
        
        # 3. Check if gap is too small
        else:
            # if gap size is below minimum, compute group width based on minimum gap
            resulting_gap_width = bar_group_width * gap_ratio
            min_gap_width = MIN_GAP_RATIO * chart_width
            if resulting_gap_width < min_gap_width: 
                bar_group_width = (chart_width - (num_rows * min_gap_width)) / num_rows
                
#         return int(round(bar_group_width))

        opts = {}
        opts['bar.groupWidth'] = int(round(bar_group_width))
        return opts

    def get_bar_chart_options(jc, chart):

        chart_opts = chart.chart_options
        
        is_stacked = chart_opts.get('isStacked', False)
        num_rows = jc._num_rows
        
        if is_stacked:
            num_series = 1
        else:
            num_series = get_num_series(jc, chart)

        MAX_BAR_RATIO = .15     # largest size bar
        MIN_LABEL_PX = 20
        CA_LEFT_BAR = 100
        MIN_BAR_WIDTH = 7
        MIN_GAP_WIDTH = 8
    
        opts = {}
        
        ca_height = chart.chart_options['chartArea']['height']

        gap_ratio = get_gap_ratio(num_series)
    
        # 1. Get unrestricted bar group width
        bar_group_width = ca_height / (num_rows * (1 + gap_ratio))
        
        # 2.  Check if bars are too thick
        max_bar_group_width = MAX_BAR_RATIO * ca_height    
                
        if bar_group_width > max_bar_group_width * num_series:
            # if a bar exceeds max size, compute bar group width based on max
            bar_group_width = max_bar_group_width * num_series
        
        resize_height = False
        
        # 3.  Check if bars are too thin
        min_bar_group_width = MIN_BAR_WIDTH * num_series
        if bar_group_width < min_bar_group_width:
            bar_group_width = min_bar_group_width
            ca_height = num_rows * bar_group_width * (1 + gap_ratio)
            resize_height = True
                    
        # 4.  Check if there is enough space for the label
        label_space = ca_height / num_rows
        if label_space < MIN_LABEL_PX:
            bar_group_width = MIN_LABEL_PX / (1 + gap_ratio) 
            ca_height = num_rows * MIN_LABEL_PX
            resize_height = True
    
        # 5.  Check for minimum gap space
        gap_space = (ca_height / num_rows) - bar_group_width
        if gap_space < MIN_GAP_WIDTH:
            ca_height = (bar_group_width + MIN_GAP_WIDTH) * num_rows
            resize_height = True

        if resize_height:
            opts['chartArea.height'] = ca_height
            opts['height'] = ca_height + chart_opts['chartArea']['top']
        opts['bar.groupWidth'] = int(round(bar_group_width))
        opts['chartArea.left'] = CA_LEFT_BAR
        
        return opts    
    
    def get_pie_chart_options(chart):
        # no special options for pies
        return {}
    
    def styler(jc, debug=debug):

        for chart in jc.charts:
            
            chart_type = chart.chart_type
            
#             if chart_type in ['ColumnChart', 'BarChart']:
#                 chart.add_chart_options(get_bar_group_width(jc, chart))
            chart.add_chart_options(legend_position=legend_position)
            chart.add_chart_options(basic_opts)
            chart.add_chart_options(get_width_options(chart, legend_position, size))
            chart.add_chart_options(get_base_height_options(chart))
            
            if chart_type == 'BarChart':
                chart.add_chart_options(get_bar_chart_options(jc, chart))
                
            if chart_type == 'ColumnChart' or (chart_type == 'ComboChart' and
                    chart.chart_options.get('seriesType') == 'bars'):
#                 opts = get_column_chart_options(jc, chart)
                chart.add_chart_options(get_column_chart_options(jc, chart))

            if chart_type == 'PieChart':
                # no special settings for pie chart
                pass
            
            if debug:
                print chart.chart_options
                chart.add_chart_options(backgroundColor="yellow")
                chart.add_chart_options(chartArea_backgroundColor="grey")
        
#         return jc
    
    return styler