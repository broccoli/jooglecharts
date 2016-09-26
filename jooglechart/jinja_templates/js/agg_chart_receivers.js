		{% for receiver in agg_chart._chart._receivers %}

		function remove_rows(dt, rows) {
			var num_rows = dt.getNumberOfRows();
			for (var i = num_rows - 1; i >= 0; i--) {
				if ($.inArray(i, rows) < 0) {
					dt.removeRow(i);			
				}
			}
		}

		(function(key, chart, chart_div_id) {
			var func = function(data) {
				if (data.sonar_key === key && document.getElementById(chart_div_id) !== null) {
					
					// The sonar message must have the main chart's data table and view.  The view
					// will have the rows visible after filtering.
					// Make of copy of the datatable and trim it by the filtered rows.  Then make
					// an aggregation datatable from it, set the agg chart's data,
					// and draw the agg chart.
					
					var sent_chart = data.sonar_value;
					var source_dt = sent_chart.data_table;
					var source_view = sent_chart.view;
					var dt_copy = new google.visualization.DataTable(source_dt.toJSON());

					// if source_view.rows is null, then the chart is unfiltered, so skip this
					if (source_view !== null && source_view.rows !== null) {
						remove_rows(dt_copy, source_view.rows);
					}
					
					var dt = google.visualization.data.group(dt_copy, [2],
						[{'column': 3, 'aggregation': google.visualization.data.avg, 'type': 'number', 'label': 'avg'},
						{'column': 3, 'aggregation': google.visualization.data.count, 'type': 'number', 'label': 'count'},
						]
					);
					
					chart.setDataTable(dt);
					chart.draw();
				}
			}
			joogle_globals.sonar.add_handler(func);

			// We're not using the one-time ready poller because there's no chart yet to have a ready event.
			// So we're checking the message map here to see if a message has been sent.
			var result = joogle_globals.sonar.poll_message_map(key);
			if (result !== null) {
				func({"sonar_key": key, "sonar_value": result});
			}

		})("{{ receiver.key }}", {{ agg_chart._name }}, "{{ agg_chart._div_id }}");

		{% endfor %}
		