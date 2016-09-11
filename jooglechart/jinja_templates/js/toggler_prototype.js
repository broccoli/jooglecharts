
	window.joogle_globals.Toggler = function(options) {
		this.show_text = options.show_text;
		this.hide_text = options.hide_text;
		this.icon_type = options.icon_type;
		this.div_id = options.div_id;
		this.$div = $("#" + this.div_id);
		this.is_open = options.is_open;
		this.duration = options.duration;
		this.$prompt = this.$div.find(".toggle_prompt");
		this.$i = this.$prompt.find("i");
		this.$text = this.$prompt.find(".toggle_text");
		this.$content = this.$div.find(".toggle_content");
		
		if (this.icon_type === "plus") {
			this.show_icon = "fa-plus";
			this.hide_icon = "fa-minus";
		}
		else if (this.icon_type === "arrow") {
			this.show_icon = "fa-angle-down";
			this.hide_icon = "fa-angle-up";
		}
		else {
			this.show_icon = "";
			this.hide_icon = "";
		}
	};
	
	window.joogle_globals.Toggler.prototype.set_prompt = function() {
		// set the display text and icon in the prompt
		if (this.is_open) {
			this.$i.removeClass(this.show_icon).addClass(this.hide_icon);
			this.$text.html(this.hide_text);
		}
		else {
			this.$i.removeClass(this.hide_icon).addClass(this.show_icon);
			this.$text.html(this.show_text);
		}
	}
	
	window.joogle_globals.Toggler.prototype.init = function() {
		
		// cache toggler for reference in click callback
		var toggler = this;

		if (!toggler.is_open) {
			toggler.$content.hide();
		}
		
		toggler.set_prompt();
		
		toggler.$prompt.click(function(event) {
			event.preventDefault();
			toggler.$content.slideToggle(toggler.duration, function () {
				toggler.is_open = !toggler.is_open;
				toggler.set_prompt();
			});
		})
		
	}
