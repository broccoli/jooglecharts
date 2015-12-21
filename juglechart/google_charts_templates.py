'''
Created on Dec 12, 2015

@author: richd

This module is just a container for the strings that can be used
to generate the chart code.  Only one string me be used to render
charts.  Other strings are included for reference or as possible
options to use at some point.

The naming of these strings is admittedly confusing.  Here is the naming
scheme.  The name indicates three things.
    1.  chart vs. dashboard
    2.  method of drawing the chart. Currently there are three methods
        to draw a chart:  chart.draw, ChartWrapper, and drawChart.
    3.  sample vs. template.  A sample is fully formed string that is
        here for development, to use as an example or to test displaying
        in notebooks.  A template is a sample with pieces substituted
        with  %()s for string interpolation.
'''

from jinja2 import Template


# a well-functioning javascript string for use in a notebook
chart_chartdraw_sample = """
<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        alert("asdf");
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': drawChart, 'packages': ['corechart']});
    }
    
    function drawChart() {
        // Insert dataTable var, created by DataTable constructor or arrayToDatable()
        var data = new google.visualization.arrayToDataTable([["Year", "Visitations"], ["2010", 10], ["2010", 14], ["2020", 16], ["2040", 22], ["2040", 28]]);
        
        
        // Here is where formatters are inserted, if any
        
        // Insert name of chart constructor and chart div id
        var chart = new google.visualization.BarChart(document.getElementById('ishbook_google_chart_id_1'));
        
        // Insert chart options
        var options = {};
        
        chart.draw(data, options);
}</script>
                        <!-- Insert chart div id again into the html -->
<div id="ishbook_google_chart_id_1" style="width: 900px; height: 500px;"></div>

"""

chart_drawchart_sample = """
<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        alert("asdf");
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': drawChart});
    }
    
    function drawChart() {
      var data = new google.visualization.arrayToDataTable([["Year", "Visitations"], ["2010", 10], ["2010", 14], ["2020", 16], ["2040", 22], ["2040", 28]]);
      google.visualization.drawChart({
         "containerId": "ishbook_google_chart_id_1",
         "dataTable": data,
         "chartType": "BarChart",
         "options": {}
       });
    }
</script>
                        <!-- Insert chart div id again into the html -->
<div id="ishbook_google_chart_id_1" style="width: 900px; height: 500px;"></div>
"""


chart_chartwrapper_sample = """
<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        //alert("asdf");
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': doMyStuff});
    }
    
    function doMyStuff() {
    
        var data = new google.visualization.arrayToDataTable([["Year", "Visitations"], ["2010", 10], ["2010", 14], ["2020", 16], ["2040", 22], ["2040", 28]]);
      
        var wrapper = new google.visualization.ChartWrapper({      
            "containerId": "ishbook_google_chart_id_1",
            "dataTable": data,
            "chartType": "BarChart",
            "options": {}
        });
        
        wrapper.draw();
    }
    
</script>
                        <!-- Insert chart div id again into the html -->
<div id="ishbook_google_chart_id_1" style="width: 900px; height: 500px;"></div>
"""

chart_drawchart_template = """<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': doMyStuff});
    }
    
    function doMyStuff() {
        // ***** Insert dataTable method -- DataTable constructor or arrayToDatable()
        var data = new google.visualization.%(data_method)s

        // ***** Insert formatters, if any
        %(formatters)s
        
        google.visualization.drawChart({
            "containerId": "%(chart_div_id)s",    // ***** Insert chart div id
            "dataTable": data,
            "chartType": "%(chart_type)s",        // ***** Insert name of chart constructor
            "options": %(chart_options)s          // ***** Insert chart options
       });
    }
</script>
        <!-- ***** Insert chart div id and div_styles into the html -->
<div id="%(chart_div_id)s" %(div_styles)s></div>"""


chart_chartwrapper_template = """
<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': doMyStuff});
    }
    
    function doMyStuff() {
        // ***** Insert dataTable method -- DataTable constructor or arrayToDatable()
        var data = new google.visualization.%(data_method)s

        // ***** Insert formatters, if any
        %(formatters)s
        
        var wrapper = new google.visualization.ChartWrapper({      
            "containerId": "%(chart_div_id)s",    // ***** Insert chart div id
            "dataTable": data,
            "chartType": "%(chart_type)s",        // ***** Insert name of chart constructor
            "options": %(chart_options)s          // ***** Insert chart options
        });
        wrapper.draw();
    }
</script>
        <!-- ***** Insert chart div id and div_styles into the html -->
<div id="%(chart_div_id)s" %(div_styles)s></div>
"""


chart_chartwrapper_template2 = """
<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': doMyStuff});
    }
    
    
    function doMyStuff() {
        // ***** Insert dataTable method -- DataTable constructor or arrayToDatable()
        var data = new google.visualization.%(data_method)s

        // ***** Insert formatters, if any
        %(formatters)s
        
        var wrapper = new google.visualization.ChartWrapper({      
            "containerId": "%(chart_div_id)s",    // ***** Insert chart div id
            "dataTable": data,
            "chartType": "%(chart_type)s",        // ***** Insert name of chart constructor
            "options": %(chart_options)s          // ***** Insert chart options
        });
        wrapper.draw();
    }
</script>
        <!-- ***** Insert chart div id and div_styles into the html -->
<div id="%(chart_div_id)s" %(div_styles)s></div>
"""

chart_chartdraw_template = """
<script type="text/javascript">

    // Check if google jsapi is already loaded.  If not, load it.
    if (typeof window.google == 'undefined') {
        alert("asdf");
        jQuery.getScript('https://www.google.com/jsapi', function( data, textStatus, jqxhr) {
            google_loader();
        });
    } else {
        google_loader();
    }

    // load visualization library
    function google_loader() {
        // ***** Insert list of packages with Python
        google.load('visualization', '1.0', {'callback': drawChart, 'packages': %(packages)s});
    }
    
    function drawChart() {
        // ***** Insert dataTable method -- DataTable constructor or arrayToDatable()
        var data = new google.visualization.%(data_method)s
        
        
        // ***** Insert formatters, if any
        %(formatters)s
        
        // ***** Insert name of chart constructor and chart div id
        var chart = new google.visualization.%(chart_type)s(document.getElementById('%(chart_div_id)s'));
        
        // ***** Insert chart options
        var options = %(chart_options)s;
        
        chart.draw(data, options);
}</script>
        <!-- ***** Insert chart div id and div_styles into the html -->
<div id="%(chart_div_id)s" %(div_styles)s></div>

"""
