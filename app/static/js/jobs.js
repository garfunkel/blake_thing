
$(function() {
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/jobs');

	// Temp -- testing...
	socket.on('ASD', function(msg) {
        $('#jobs').append('<p>Received: ' +JSON.stringify(msg.data) + '</p>');

		var table_body = $("tbody");

		table_body.children().remove();
		$.each(msg.data, function(i, job) {
			var table_row = $('<tr>');
			$('<th scope="row">').text(job.task_id).appendTo(table_row);
			$('<td>').text(job.status).appendTo(table_row);
			$('<td>').text(job.result.progress).appendTo(table_row);
			table_row.appendTo(table_body);
		});
    });
});
