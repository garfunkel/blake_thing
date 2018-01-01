$(function() {
	// Max length
	$("[data-b_len]").keypress(function(key) {
		if ($(this).val().length == $(this).data("b_len")) return false;
	});

	$("[data-b_len]").change(function() {
		$(this).val($(this).val().slice(0, $(this).data("b_len")));
	});

	// Integer
	$("[data-b_num]").keypress(function(key) { return isNum(key); });

	$("[data-b_num]").change(function(key) {
		$(this).val().replace(/[^0123456789]/g, "");
	});

	// Character
	$("[data-b_char]").keypress(function(key) { return isChar(key); });

	$("[data-b_char]").change(function() {
		$(this)[0].value = $(this).val().replace(/[^a-zA-Z]/g, "");
	});

	// Character + -
	$("[data-b_charnum-]").keypress(function(key) {
		if (key.charCode == 45) return true;
		return (isChar(key) || isNum(key));
	});

	$("[data-b_charnum-]").change(function() {
		$(this)[0].value = $(this).val().replace(/[^a-zA-Z0123456789\-]/g, "");
	});

	// LanguageCode
	$("[data-b_lancou]").keypress(function(key) {
		if ($(this).val().length == 3 && key.charCode == 97) return true;
		if ($(this).val().length == 3) $(this).val($(this).val() + "_");
		return isChar(key);
	});

	$("[data-b_lancou]").change(function(key) {
		if ($(this).val().length == 6)
			$(this).val([$(this).val().slice(0,3), $(this).val().slice(3,6)].join("_"));
	});
});

function isNum(key) {
	return !((key.charCode < 48 || key.charCode > 57));
};

function isChar(key) {
	return !((key.charCode < 97 || key.charCode > 122) && (key.charCode < 65 || key.charCode > 90));
};
