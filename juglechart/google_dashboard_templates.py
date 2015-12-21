'''
Created on Dec 12, 2015

@author: richd
'''


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

dashboard_chartwrapper_template = """<script type="text/javascript">
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
          google.load('visualization', '1.0', {'packages':['controls'], 'callback': doMyStuff});
    }

    function doMyStuff() {

        // ***** Insert dataTable method -- DataTable constructor or arrayToDatable()
        var data = new google.visualization.%(data_method)s

        // ***** Insert formatters, if any
        %(formatters)s
        
        // Create a chart
        var wrapper = new google.visualization.ChartWrapper({      
            "containerId": "%(chart_div_id)s",    // ***** Insert chart div id
            "dataTable": data,
            "chartType": "%(chart_type)s",        // ***** Insert name of chart constructor
            "options": %(chart_options)s          // ***** Insert chart options
        });

        // Create a dashboard.
        // ***** Insert dashboard div id
        var dashboard = new google.visualization.Dashboard(document.getElementById('%(dashboard_div_id)s')); 

        // ***** Insert filters
        %(filters)s
        
        // ***** Insert binders 
        %(binders)s

        // Draw the dashboard.
        dashboard.draw(data);
      }
</script>
<!--Div that will hold the dashboard-->
<div id="%(dashboard_div_id)s">  <!-- ***** Insert dashboard div id -->
    <!--Divs that will hold each control and chart-->
        <!-- ***** Insert filter divs -->
    %(filter_divs)s
        <!-- ***** Insert chart div id and div_styles into the html -->
    <div id="%(chart_div_id)s" %(div_styles)s></div>
</div>"""