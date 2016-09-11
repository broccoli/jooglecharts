	var toggle_box = new joogle_globals.ToggleBox({
		"show_text": "{{ toggler._open_prompt }}",
		"hide_text": "{{ toggler._close_prompt }}",
		"icon_type": "{{ toggler._icon }}",
		"div_id": "{{ toggler._div_id }}",
		"is_open": {{ toggler._is_open }},
		"duration": {{ toggler._duration }}
	});
	
	toggle_box.init();
