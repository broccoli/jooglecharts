
{% for chart in jg.charts %}
{% if chart._download_position %}

		(function(chart, chart_name, datatable) {
			$('#download_' + chart_name).click(function () {
				
				/*
					The download should have the subset of the datatable that hasn't been filtered.
				
					The columns to be downloaded should exclude columns
					that have been filtered by a series filter and any role columns.
				*/
				
				var num_columns = datatable.getNumberOfColumns();
				
				var view_cols = chart.getView().columns;
				if (view_cols === null) {
					// if view columns is null, get list of all column indexes
					view_cols = [];
					for (var i = 0; i < num_columns; i++) {
						view_cols.push(i);
					}
				}
				
				var download_columns = view_cols.slice(0); // make copy of array
	
				// remove role columns from current view columns
				var role_cols = chart['__role_columns'].slice(0);
				for (var i = 0; i < role_cols.length; i++) {
					var arr_index = download_columns.indexOf(role_cols[i]);
					if (arr_index > -1) {
						download_columns.splice(arr_index, 1);
					}	
				}
	
				// make a copy of the datatable, remove all columns but the current view columns and role columns
				var download_dt = datatable.clone();
				for (var i = num_columns - 1; i >= 0; i--) {
					if (download_columns.indexOf(i) < 0) {
						download_dt.removeColumn(i);
					}
				}
				
				// Remove filtered rows from dt copy if rows have been filtered.					
				// The viewable rows are retrieved differently for native Google filters and sonar filters.
				var view_rows;
				try {
					// native filter
					view_rows = chart.getDataTable().getViewRows();
				}
				catch(err) {
					// sonar filter
					view_rows = chart.getView().rows;
				}
				
				if (view_rows !== null) {
					// view_rows will be null if there is no native filter and no sonar filters have
					// been applied.  If there is a native filter, the array will always have values.
					for (var i = datatable.getNumberOfRows() - 1; i >= 0; i--) {
						if (view_rows.indexOf(i) < 0) {
							download_dt.removeRow(i);
						}
					}
				}
				
				var csv = google.visualization.dataTableToCsv(download_dt);
	
				// get column headers
				var headers = [];
				download_columns.forEach(function(el) {
					// check if the list of columns has an object in it.  The column list will
					// have an object if the non-Table chart has a filtered column.
					if (typeof el === "number") {
						headers.push(datatable.getColumnLabel(el));						
					}
				});
				csv = headers.join(",") + "\n" + csv;
				
				// download the csv
				var encodedUri = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);
				this.href = encodedUri;
				this.download = 'table-data.csv';
				this.target = '_blank';
			});  
		
		})({{ chart.name }}, "{{ chart.name }}", {{ jg.data_name }});

{% endif %}
{% endfor %}
