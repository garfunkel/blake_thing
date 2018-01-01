var name = 'stores';
var valueNames = ['projnamenum', 'lancou', 'descriptor'];

class Item {
	constructor(data) {
		this.id = data.id;
		this.name = data.name;
		this.number = data.number;
		this.descriptor = data.descriptor;
		this.lancou = data.lancou;
	}

	renderListItem() {
		var listItem = $(`<li id="${this.id}"  class="list-group-item list-group-item-action flex-column align-items-start">`);
		var listbody = $('<div class="d-flex w-100 justify-content-between">').appendTo(listItem);
		listbody.append($('<h5 class="mb-1">').addClass('projnamenum').text(`${this.name} ${this.number}`));
		listbody.append($('<small>').addClass('lancou').text(this.lancou));
		listItem.append($('<p class="mb-1">').addClass('descriptor').text(this.descriptor));
		return listItem;
	}

	renderContent() {
		var d = $.Deferred();
		var content = $('<div>');
		content.append($('<h1>').text(`${this.name} ${this.number}`));
		content.append($('<h4>').text(`${this.descriptor} ${this.lancou}`));
		content.append($('<hr>'));

		$.getJSON(`${$SCRIPT_ROOT}/api/stores/${this.id}`, function(data) {
			content.append($('<p>').text(`Path: ${data.path}`));
		})
		.then(function() {
			d.resolve(content);
		});
		return d.promise();
	}
}
