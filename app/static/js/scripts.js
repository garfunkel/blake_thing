var name = 'scripts';
var valueNames = ['name', 'description'];

$(function() {
		$('#content').on("submit", "#ScriptForm", function(e) {
			e.preventDefault();
			onSubmit($("#content-list-items .active").get(0).id);
		});
});

class Item {
	constructor(data) {
		this.id = data.id;
		this.name = data.name;
		this.description = data.description;
	}

	renderListItem() {
		var listItem = $(`<li id="${this.id}" class="list-group-item list-group-item-action flex-column align-items-start">`);
		var listbody = $('<div class="d-flex w-100 justify-content-between">').appendTo(listItem);
		listbody.append($('<h5 class="mb-1">').addClass('name').text(this.name));
		listItem.append($('<p class="mb-1">').addClass('description').text(this.description));
		return listItem;
	}

	renderContent() {
		var d = $.Deferred();
		var content = $('<div>');
		content.append($('<h1>').text(this.name));
		content.append($('<p>').text(this.description));
		content.append($('<hr>'));

		var form = $('<form id="ScriptForm">').appendTo(content);

		var required = $('<div id="required" class="mb-3">').append($('<h5>').text('Required')).appendTo(form);
		var optional = $('<div id="optional" class="mb-3">').append($('<h5>').text('Optional')).appendTo(form);;

		$.getJSON(`${$SCRIPT_ROOT}/api/scripts/${this.id}`, function(data) {
			$.when($.each(data, function(name, input) {
				if (input.required == true)
					required.append(formatInput(name, input));
				else
					optional.append(formatInput(name, input));
				})
			)
			.then(function() {
				if (optional.children().length < 2)
					optional.remove();
			});
		})
		.then( function() {
			$('<button type="submit" class="btn btn-primary" formnovalidate>').text("Submit").appendTo(form);
			d.resolve(content);
		});
		return d.promise();
	}
}

function formatInput(name, input) {
	var formrow = $('<div class="form-group col-6">');

	switch(input.type) {
		case "Boolean_Input":
			var div = $('<div class="form-check">').appendTo(formrow);
			$(`<input type="checkbox" name="${name}" class="form-check-input position-static" id="${name}">`).prop('checked', input.default).appendTo(div);
			$(`<label for="${name}" class="mb-0">`).text(input.name).appendTo(div);
			$(`<small class="form-text mt-0">`).text(input.help).appendTo(div);
			break;

		case "String_Input":
			$(`<label for="${name}">`).text(input.name).appendTo(formrow);
			$(`<input type="text" name="${name}" class="form-control" id="${name}" placeholder="${input.default}">`).val(input.default).appendTo(formrow);
			$(`<small class="form-text">`).text(input.help).appendTo(formrow);
			break;

		case "Choice_Input":
			$(`<label for="${name}">`).text(input.name).appendTo(formrow);
			var select = $(`<select name="${name}" class="form-control" id="${name}">`).appendTo(formrow);
			$('<option selected>').data('value', '').appendTo(select);
			$.each(input.choices, function(i, choice) {
					if (choice == input.default)
						$('<option selected>').data('value', i).text(choice).appendTo(select);
					else
						$('<option>').data('value', i).text(choice).appendTo(select);
			});
			break;
	}
	$('<div class="invalid-feedback">').appendTo(formrow);
	return formrow;
}


function cleanForm() {
	var form = $('#ScriptForm');
	form.find(":input").removeClass("is-invalid is-valid");
	form.find(".invalid-feedback").each(function(index, value) {
		$(this).text("");
	});
};

function parseForm() {
	var d = $.Deferred();
	var data = {};

	$.when(
		$.each($('#ScriptForm').find(":input"), function(index, value) {
			switch (value.type) {
				case "checkbox":
					data[value.name] = $(this).is(':checked');
					break;

				case "text":
					data[value.name] = $(this).val();
					break;

				case "select-one":
					data[value.name] = $(this).find(":selected").data('value');
					break;
			}
		})
	)
	.then( function() {
		d.resolve(data);
	});

	return d.promise();
};

function onSubmit(id) {
	var form = $('#ScriptForm');
	cleanForm();
	parseForm()
	.done(function(data) {
		$.post($SCRIPT_ROOT + "/api/scripts/" + id, JSON.stringify(data, null, '\t'))
			.done(function(data) {

			})
			.fail(function(data) {
				$.each(data.responseJSON, function(key, value) {
					form.find(`:input[name="${key}"]`).addClass("is-invalid").parent().find(".invalid-feedback").text(value);
				});
				form.find("select, input:not([is-invalid])").addClass("is-valid");
			})
			.always(function() {

			});
	});
};
