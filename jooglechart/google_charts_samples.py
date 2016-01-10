'''
This module contains sample strings of working js/html that can be put
displayed from an ipython notebook.  They are for reference only.
Several ways to create chartes are represented.
'''


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


dashboard_chartwrapper_sample = """

<!--Load the AJAX API-->
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
        
          google.load('visualization', '1.0', {'packages':['controls'], 'callback': doMyStuff});
    }



      function doMyStuff() {
      

        // Create our data table.
        var data = google.visualization.arrayToDataTable([
          ['Name', 'Donuts eaten'],
          ['Michael' , 5],
          ['Elisa', 7],
          ['Robert', 3],
          ['John', 2],
          ['Jessica', 6],
          ['Aaron', 1],
          ['Margareth', 8]
        ]);


        // Create a chart
        var pieChart = new google.visualization.ChartWrapper({
          'chartType': 'PieChart',
          'containerId': 'chart_div',
          'options': {
            'width': 300,
            'height': 300,
            'pieSliceText': 'value',
            'legend': 'right'
          }
        });

        // Create a dashboard.
        var dashboard = new google.visualization.Dashboard(
            document.getElementById('dashboard_div'));

        // Create controls
        var donutRangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'filter_div',
          'options': {
            'filterColumnLabel': 'Donuts eaten'
            }
        });

        // Establish dependencies.
        dashboard.bind(donutRangeSlider, pieChart);

        // Draw the dashboard.
        dashboard.draw(data);
      }
    </script>

    <!--Div that will hold the dashboard-->
    <div id="dashboard_div">
      <!--Divs that will hold each control and chart-->
      <div id="filter_div"></div>
      <div id="chart_div"></div>
    </div>

"""

