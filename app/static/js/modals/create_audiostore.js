$(function() {
	modal = $("#CreateAudioStoreModal");

	initCreateAudioStoreModal(modal);

	modal.submit(function(e) {
		e.preventDefault();
		submitCreateAudioStoreModal(modal);
	});

	modal.on("show.bs.modal",  function() { showCreateAudioStoreModal(modal) });

	modal.on("hidden.bs.modal", function() { clearCreateAudioStoreModal(modal) });
});

function initCreateAudioStoreModal(modal) {
	modal.focusin(function() {
		$(this).keyup(function() { pathCreateAudioStoreModal(modal); });
		$(this).change(function() { pathCreateAudioStoreModal(modal); });
		modal.find("#share_id").change(function() { pathCreateAudioStoreModal(modal); });
	});

	$.getJSON($SCRIPT_ROOT + '/api/shares', function(data){
		var share_id = modal.find("#share_id");
		$.each(data, function(i, item) {
			if (i == 1)
				share_id.append($("<option selected>", {value: item.id , text: value.path}));
			share_id.append($("<option>", {value: item.id , text: item.path}));
		});
	});
};

function submitCreateAudioStoreModal(modal) {
	cleanCreateAudioStoreModal(modal);
	$("#CreateAudioStoreModal :submit").prop("disabled", true);
	$("#CreateAudioStoreModal .progress").show();
	var data = {};
	modal.find(":input").each(function(index, value) {
		data[$(this)[0].name] = $(this)[0].value;
	});

	$.post($SCRIPT_ROOT + "/api/stores", JSON.stringify(data, null, '\t'))
		.done(function(data) {
			modal.modal("hide");
			addItem(data);
			updateContent(data.id);
		})
		.fail(function(data) {
			$.each(data.responseJSON, function(key, value) {
				if (key == "error") modal.find(".alert-danger").text(value).show();
				modal.find(":input[name=" + key + "]").addClass("is-invalid").parent().find(".invalid-feedback").text(value);
			});
			modal.find("select, input:not([is-invalid]):not([readonly])").addClass("is-valid");
		})
		.always(function() {
			modal.find(":submit").prop("disabled", false);
			modal.find(".progress").hide();
		});
};

function pathCreateAudioStoreModal(modal) {
	modal.find("#path").val(
		modal.find("#share_id option:selected").text()
		+ "/"
		+ modal.find("input:not([readonly])").map(function() {
			if ($(this).val().length != 0)
				return $(this).val();
		}).get().join("_")
	);
};

function showCreateAudioStoreModal(modal) {
	modal.find("#path").val(
		modal.find("#share_id option:selected").text()
	);
};

function cleanCreateAudioStoreModal(modal) {
	modal.find(".alert").hide();
	modal.find(":input").removeClass("is-invalid is-valid");
	modal.find(".invalid-feedback").each(function(index, value) { $(this).text(""); });
};

function clearCreateAudioStoreModal(modal) {
	cleanCreateAudioStoreModal(modal);
	modal.find("input:not([select])").each(function(index, value) { $(this).val(""); });
};
