from app.scripts import Script, Boolean_Input, String_Input, Choice_Input, File_Input

from time import sleep


class Test_Script(Script):
	name = "Test Script"
	description = "This is a test script"

	#bool_test = Boolean_Input("boolean test", "Help message", False, True)
	string_test = String_Input("string test", "String message help", False)
	string_test_2 = String_Input("string mEW", "String mew mew")
	test_choice = Choice_Input("Choices", "Pick n choose", choices=["A", "Bb", "C"], default="A")
	test_choice_2 = Choice_Input("Choices", "Pick n choose", choices={2: "A", 3: "Bb",  4: "C"})

	def run(self):
		for i in range(0, 100):
			self.update_meta({"progress": i})
			sleep(3)
