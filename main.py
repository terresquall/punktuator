"""
IMPORTANT
To use this script, your PYTHON VERSION THAT WINDOWS REFERS TO (you can change it in system environment variables) MUST
BE no newer than 3.9, means that if you are using python version 3.10, the following script will not work properly.

MAKE SURE YOU HAVE THE FOLLOWING PACKAGE:
1. pip install numpy=1.20.3 - version is very important
2. pip install punctuator

After installing packages, you need to specify the model you are going to use.

Firstly, in the gmail message, I sent 3 different models, for this script use 'Demo-Europarl-EN.pcl' model.
Download this model, then find where package 'punctuator' is located on your computer, and just past model to 'punctuator'
package.

Secondly, specify the path to the model in the following line:
p = Punctuator('path/to/the/model'). You can see my example in the code.

NOW, you are ready to use the script.
"""

import os  # OS library
import json	 # JSON library
import re  # Regex library

# Try importing Punctuator.
try:
	from punctuator import Punctuator
except ModuleNotFoundError:
	print("Punctuator module not found! Run pip install punctuator to install it.")

# Enforce Python version before this is run.
import sys

if sys.version_info.major != 3 or sys.version_info.minor != 9:
	print("You need Python 3.9 for this script to work, as we need numpy=1.20.3, which only runs on Python 3.9.")
	print("Exiting...")
	exit()

# Check if the correct version of numpy is installed.
try:
	import numpy
except ModuleNotFoundError:
	print("numpy is not installed. Run pip install numpy=1.20.3 to install it.")
	print("Exiting...")
	exit()


class Punktuator:

	def __init__(self):
		self.config = self.initConfig()
		self.modelPath = self.determineModel()
		self.inputPath = self.determineInputFile()
		self.outputPath = self.determineOutputPath()
		self.dictionary = self.initDictionary()
		self.run()

	def initDictionary(self):
	
		# Do we use the dictionary?
		useDict = input("dictionary.json found. Use dictionary? (y/n) ")
		if useDict.lower() != "y":
			return None
	
		# Retrieve the file.
		try:
			with open("dictionary.json") as dictionary:
				return json.loads(dictionary.read())
		
		except ModuleNotFoundError:
			print("json module not found.")
		
		except FileNotFoundError:
			print("dictionary.json not found. Ignoring...")
			
		except json.decoder.JSONDecodeError:
			print("dictionary.json contains invalid JSON.")

	def initConfig(self):
		# Read the settings file to get the paths that we want.
		try:
			with open("config.json") as config:
				return json.loads(config.read())

		except ModuleNotFoundError:

			print("json module not found.")

		except FileNotFoundError:
			print("config.json not found. Generating file...")
			return self.regenerateConfig()

		except json.decoder.JSONDecodeError:
			print("config.json contains invalid JSON. Regenerating...")
			return self.regenerateConfig()

	def regenerateConfig(self):

		# If the config file doesn't exist or is malformed, recreate it.
		data = {
			"models": {
				"directory": "models"
			},
			"inputDirectory": "inputs",
			"outputDirectory": "outputs",
			"debug": True
		}

		# Write a config file if there isn't one.
		with open("config.json", "w") as config:
			config.write(json.dumps(data, indent=4))
			print("Created a config.json file for adjusting which models are to be used.")

		return data

	# Ask the user which model he wants to use.
	def determineModel(self):
		try:
			files = os.listdir(self.config["models"]["directory"])

			# Select a model to use.
			print("\nSelect a model to use:\n")

			index = 1
			models = []
			for f in files:
				fdat = os.path.splitext(f)
				if fdat[1].lower() == '.pcl':
					print("{:d}. {:s}".format(index, f))
					models.append(f)
					index += 1

			# Get the model to use.
			if len(models) > 0:

				modelSelected = int(input("\nEnter model number: "))

				if modelSelected > len(models):
					print("Invalid model selected!")
					return self.determineModel()

				selectedModel = models[modelSelected - 1]
				print("You've selected {:s}.\n".format(selectedModel))
				return self.config["models"]["directory"] + os.path.sep + selectedModel

			else:
				print("There are no models for Punctuator to use. Please download them and put them in {:s}.".format(
					os.getcwd() + os.path.sep + self.config["models"]["directory"]))

		except FileNotFoundError:
			os.mkdir(self.config["models"]["directory"])
			print("Models directory not found. Created a directory.")

			# Run the function again
			return self.determineModel()

	# Ask the user which model he wants to use.
	def determineInputFile(self):
		try:
			files = os.listdir(self.config["inputDirectory"])

			# Select a model to use.
			print("\nWhich file do you want to punctuate?\n")

			index = 1
			inputs = []
			for f in files:

				# Ignore MD files.
				fdat = os.path.splitext(f)
				if fdat[1] == '.md': continue

				print("{:d}. {:s}".format(index, f))
				inputs.append(f)
				index += 1

			# Get the model to use.
			if len(inputs) > 0:

				fileSelected = int(input("\nSelect a file: "))

				if fileSelected > len(inputs):
					print("Invalid file selected!")
					return self.determineInputFile()

				selectedInput = inputs[fileSelected - 1]
				print("You've selected {:s}.\n".format(selectedInput))
				return self.config["inputDirectory"] + os.path.sep + selectedInput

			else:
				print("There are no input files!")
				exit()

		except FileNotFoundError:
			os.mkdir(self.config["inputDirectory"])
			print("Input directory not found. Created the directory.")

			# Run the function again
			return self.determineInputFile()

	# Get the path to output to from the input path.
	def determineOutputPath(self):
		# Create the folder if it does not exist.
		if not os.path.exists(self.config["outputDirectory"]):
			os.mkdir(self.config["outputDirectory"])

		path = self.inputPath.replace(self.config["inputDirectory"], self.config["outputDirectory"])
		print("File will be output to {:s}.".format(path))
		return path
		
	# Replace text in dictionary.
	# NOT ENTIRELY DONE. STILL SOME ISSUES.
	def processWithDictionary(self, stringToProcess):
		# If dictionary is not valid, move on.
		if type(self.dictionary) is dict:
		
			# Loop through each dictionary and replace words in there.
			for cat, subdict in self.dictionary.items():
				for k, v in subdict.items():
					stringToProcess = stringToProcess.replace(k,v)
				
		return stringToProcess

	def run(self):

		try:

			p = Punctuator(self.modelPath)

			# Check if the program should take inputs into account.
			# And if it should include timings in output.
			input_has_timings = input("Does the input file have timings? (y/n) ").lower() == "y"
			if input_has_timings:
				output_has_timings = input("Should timings be included with the output? (y/n) ").lower == "y"
			else:
				output_has_timings = False

			# Begin reading the file.
			with open(self.inputPath, 'r+') as f:
			
				if input_has_timings:
					
					wholeText = ""
					result_dictionary = self.processInputTextWithTimings(f.readlines())
					
					print("Finished reading the file.")
					
					for timing, text in result_dictionary.items():
						wholeText += text
					
					# Process text with dictionary.
					wholeText = self.processWithDictionary(wholeText)
					
					# Punctuate the text.
					print("\nPunctuating, please wait...\n")
					punctuated_text = p.punctuate(wholeText).replace(". ", ".\n\n")

					# After the text is punctuated, we want to search and replace the
					# dictionary in each section with their punctuated counterparts.					
					self.outputTextWithPatter(result_dictionary, punctuated_text);

					with open(self.outputPath, 'w') as saved:
						saved.write(finalText)
						print("\nFile successfully output to {:s}.".format(self.outputPath))
				else:
					result = self.processWithDictionary( self.processInputTextWithoutTimings(f.readlines()) )
					
					print("Punctuating, please wait...\n")
					punctuated_text = p.punctuate(result).replace(". ", ".\n\n")

					with open(self.outputPath, 'w') as saved:
						saved.write(punctuated_text)
						print("\nFile successfully output to {:s}.".format(self.outputPath))

		except FileNotFoundError:
			print("-" * 43)
			print('Error with directory of the captions file.')
			print('Check its location again please.')
			print("-" * 43)

	# Process an array of data and output a string without any newlines.
	def processInputTextWithoutTimings(self, data):

		result = ""
		if self.config["debug"]:
			print("\nReading lines without timing:")
			print('-' * 20)

		for line in data:

			# Ignore empty lines.
			if re.search("^[\s\r\n]*$", line) != None:
				continue

			result += " " + line.strip()
			if self.config["debug"]: print(line)

		if self.config["debug"]: print('-' * 20)
		return result

	# Process an array of data and returns a Dictionary with the key being the
	# timing and the value being the lines.
	def processInputTextWithTimings(self, data):

		result = {}
		if self.config["debug"]:
			print("\nReading lines with timing:")
			print('-' * 20)

		currentTiming = "no-timing"
		for line in data:
			line = line.replace("Â", "")
			# Ignore empty lines.
			if re.search("^[\s\r\n]*$", line) != None:
				continue

			# Check if this is a timing line.
			# I Changed regex condition, so now it is working properly
			if re.search("([0-9])([:,.]?)", line) != None:
				text = "" # this variable contains text of one timing, it's reset each time when new timing comes
				if self.config["debug"]: print("Reading timing {:s}".format(line))
				currentTiming = line

			else:
				text += line
				result[currentTiming] = text
			
			# Otherwise, put the strings into the current timing.
			if self.config["debug"]: print(line)

		if (self.config["debug"]): print('-' * 20)
		return result
	
	# AZAT'S processing code.
	# THE LAST PART where I am stuck. The problem is that the text of one timing is not complete, meaning
	# text has continuation in another timing, and when punctuating, we are punctuating a whole text at one time.
	# It can be solved if each timing would have the whole complete sentence, so we could have just punctuated
	# the value in the dictionary each time.
	def outputTextWithPatter(self, result_dictionary, punctuated_text):

		patter = re.compile('(\w+)', re.IGNORECASE)
		patter2 = re.compile('([a-z]*,?.?)', re.IGNORECASE)
		checkPoint = 0
		finalText = ""
		count = 1

		# START OF THE ALGORITHM HOW IT SHOULD ADD TIMING TO THE CORRESPONDING VALUE
		# IDEA OF THE WHOLE ALGORITHM:
		"""
		patter takes all words in the punctuated text, ignoring the punctuation, ALSO second patter takes all
		words in the punctuated text considering punctuating, but I noticed that either ways the index of the
		word that affected by the patters are the same, so if we just knew from which index to start
		and when to end, we would past the timings before each value from the dictionary.

		I hope you get my idea, it is hard to explain what is my head, really :D.

		I count every time when the 'match' matches the value, but the prblem here is that other 'match' from other
		timings also can match the word in 'val' and I don't know yet how to say to program to stop when 'match' matched
		the last word in the 'val'. Once I 'count' value counts correctly, I use the second patter, so I know
		how many words to add before each timing.

		There might be some redundant values or lines, cause I think I got confused my head with possible solutions
		and alternative ways.
		"""
		for key, val in result_dictionary.items():
			print(val)
			numberOfSpaces = 0
			splitedVal = val.split(" ")
			for match in patter.finditer(punctuated_text):
				if match.group().strip() == "" or match.group() == '\n':
					continue
				# else:
				#	  textWithoutPunct += match.group().strip() + " "
				if match.group().lower() in val:
					print(match.group())
					count += 1
			i = 0
			print(count)
			print(checkPoint)
			record = 0
			justText = ""
			for match2 in patter2.finditer(punctuated_text):
				if i == 0:
					justText += '\n' + str(key) + '\n'
					i += 1
				if match2.group() == "":
					continue
				if record < checkPoint:
					record += 1
					continue
				if checkPoint < count:
					justText += match2.group() + ' '
					checkPoint += 1
			checkPoint = count
			finalText += justText
		# END OF THE ALGORITHM


Punktuator()