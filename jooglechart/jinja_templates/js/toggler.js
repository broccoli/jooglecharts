	var toggler = new joogle_globals.Toggler({
		"show_text": "{{ toggler._open_prompt }}",
		"hide_text": "{{ toggler._close_prompt }}",
		"icon_type": "{{ toggler._icon }}",
		"div_id": "{{ toggler._div_id }}",
		"is_open": {{ toggler._is_open }},
		"duration": {{ toggler._duration }}
	});
	
	toggler.init();
