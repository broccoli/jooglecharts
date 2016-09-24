

		// An AggChart doesn't need a datatable, and doesn't need to be drawn initially.
		// It gets data and drawn in the receiver.

        // Create ChartWrapper
        var {{ agg_chart.name }} = new google.visualization.ChartWrapper({  
            "containerId": "{{ agg_chart._chart.chart_div_id }}",
            "chartType": "{{ agg_chart._chart.display_chart_type }}",
            "options": {{ agg_chart._chart.chart_options|to_json }}
        });
    
		// -------------- Add chartwrapper receivers, if any -------------
          {% include 'js/agg_chart_receivers.js' %}
		// ---------------------------------------------------------------
    