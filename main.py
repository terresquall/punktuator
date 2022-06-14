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

from punctuator import Punctuator
import os

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
    
# Read the settings file to get the paths that we want.
try:
    import json
    
    with open("config.json") as config:
        data = json.loads(config)
    
except ModuleNotFoundError:

    print("json module not found.")
    
except FileNotFoundError:
    
    # If the config file doesn't exist, create it.
    data = {
        "models": {
            "directory": "models"
        },
        "inputDirectory": "inputs",
        "outputDirectory": "outputs"
    }
    
    # Write a config file if there isn't one.
    with open("config.json","w") as config:
        config.write(json.dumps(data, indent=4))
        print("Created a config.json file for adjusting which models are to be used.")
    
# If the data array has nothing, ask the user which model he wants to use.


model_found = False  # variable to check whether model is correctly set or not.
try:
    p = Punctuator('Demo-Europarl-EN.pcl')  # Defining the model that we want to use.
    model_found = True
except AssertionError:
    print("-" * 80)
    print("Sorry, but the directory of the model that you are trying to set doesn't exist."
          "\nCheck the directory again, please.")
    print("-" * 80)


if model_found:
    try:
        with open('shader-subscriber.txt', 'r+') as f:
            subtitles = f.readlines()
            f.seek(0)
            text = ''
            timings = []
            lengths = []
            for i in range(len(subtitles)):
                if i % 3 == 0:  # Adding timings for the separate Array
                    subtitles[i] = subtitles[i].strip()
                    timings.append(subtitles[i])
                    continue
                if subtitles[i] == '\n':  # Skipping the new lines
                    continue
                subtitles[i] = subtitles[i].replace('\n',
                                                    ' ')  # in the end of each line, there is \n, so I am changing it to space
                text += subtitles[i]
            f.close()
            print(text)  # Just checking the text
            corrected_text = p.punctuate(text)  # punctuate method is the one who makes punctuation on the text.
            print(corrected_text)  # Just checking the corrected text
            with open('C:/Users/umral/Desktop/captions.sbv', 'w') as f:  # Writing to the file
                f.write(corrected_text)
                f.close()
    except FileNotFoundError:
        print("-" * 43)
        print('Error with directory of the captions file.'
              '\nCheck its location again please.')
        print("-" * 43)
    except:
        print("-" * 100)
        print("Another error occurred, but the current error is not related to the location of the captions file.")
        print("-" * 100)
