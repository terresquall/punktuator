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

import os # OS library
import json # JSON library
import re # Regex library

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
		
		self.run()
		
	def initConfig(self):
		# Read the settings file to get the paths that we want.
		try:		
			with open("config.json") as config:
				return json.loads(config.read())
			
		except ModuleNotFoundError:

			print("json module not found.")
			
		except FileNotFoundError:
			return self.regenerateConfig()
			
		except json.decoder.JSONDecodeError:
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
		with open("config.json","w") as config:
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
					print("{:d}. {:s}".format(index,f))
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
				print("There are no models for Punctuator to use. Please download them and put them in {:s}.".format(os.getcwd() + os.path.sep + self.config["models"]["directory"]))
				
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
			
				print("{:d}. {:s}".format(index,f))
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
		
		path = self.inputPath.replace(self.config["inputDirectory"],self.config["outputDirectory"])
		print("File will be output to {:s}.".format(path))
		return path
			
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
					# NOT DONE. We have to process the output also.
					result = self.processInputTextWithTimings(f.readlines())
					print(result)
					
				else:
					
					result = self.processInputTextWithoutTimings(f.readlines())
					print("Punctuating, please wait...\n")
					punctuated_text = p.punctuate(result).replace(". ",".\n\n")
					
					with open(self.outputPath, 'w') as saved:
						saved.write(punctuated_text)
						print("\nFile successfully output to {:s}.".format(self.outputPath))
					
		except FileNotFoundError:
			print("-" * 43)
			print('Error with directory of the captions file.'
				  '\nCheck its location again please.')
			print("-" * 43)
	
	# Process an array of data and output a string without any newlines.
	def processInputTextWithoutTimings(self, data):
		
		result = ""
		if self.config["debug"]:
			print("\nReading lines without timing:")
			print('-' * 20)
		
		for line in data:
		
			# Ignore empty lines.
			if re.search("^[\s\r\n]$",line) != None:
				continue
			
			result += " " + line.strip()
			if self.config["debug"]: print(line)
			
		if self.config["debug"]: print('-' * 20)
		return result
		
	# Process an array of data and returns a Dictionary with the key being the
	# timing and the value being the lines.
	def processInputTextWithTimings(self, data):
		
		result = {}
		currentTiming = "no-timing"
		if self.config["debug"]: 
			print("\nReading lines with timing:")
			print('-' * 20)
		
		for line in data:
			# Ignore empty lines.
			if re.search("^[\s\n]$",line) == None:
				continue
			
			# Check if this is a timing line.
			if re.search("^[0-9,:\.]*?\n$",line) != None:
				currentTiming = line
				if self.config["debug"]: print("Reading timing {:s}".format(line))
				
			# Otherwise, put the strings into the current timing.
			result[currentTiming] += " " + line
			if self.config["debug"]: print(line)
		
		if(self.config["debug"]): print('-' * 20)
		return result
		
		
Punktuator()   
