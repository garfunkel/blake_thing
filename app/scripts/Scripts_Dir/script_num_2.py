from app.scripts import Script, Boolean_Input, String_Input, Choice_Input, File_Input

from time import sleep


class Script_num_2(Script):
	name="Script Num 2"
	description = "2nd testing  script..."

	string_test_2 = String_Input("string mEW", "String mew mew")
	test_choice = Choice_Input("Choices", "Pick n choose", choices=["A", "Bb", "C"], default="A")
	test_choice_2 = Choice_Input("Choices", "Pick n choose", choices={2: "A", 3: "Bb",  4: "C"})

	def run(self):
		for i in range(0, 100):
			self.update_meta({"progress": i})
			sleep(3)
