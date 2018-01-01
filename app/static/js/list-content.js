var items = {};
var itemsList;

$(function() {
	$("#content-list-items").on('click', 'li:not(.active)', function(e) {
		$(this).addClass('active').siblings().removeClass('active');
		updateContent($(this).attr('id'));
	});

	getItems();
});

function getItems() {
	$.getJSON($SCRIPT_ROOT + '/api/' + name, function(data) {
		$.each(data, function(i, itemdata) {
			addItem(itemdata);
		});
		itemsList = new List('content-list', {
			valueNames: valueNames
		});
	});
};

function addItem(itemdata) {
	var contentList = $('#content-list-items');
	item = new Item(itemdata);
	contentList.append(item.renderListItem());
	items[item.id] = item;
};

function updateContent(id) {
	var content = $('#content');
	content.children().remove();
	content.append($('<div id="loader" class="loader mx-auto">').hide().delay(500).show(0));
	items[id].renderContent()
	.done(function(data) {
		content.children().remove();
		content.append(data);
	});
};
