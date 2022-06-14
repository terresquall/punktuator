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

# Enforce Python version before this is run.
import sys
if sys.version_info.major != 3 or sys.version_info.minor != 9:
    print("You need Python 3.9 for this script to work!")
    print("Exiting...")
    exit()


from punctuator import Punctuator
import os
p = Punctuator('Demo-Europarl-EN.pcl') # Defining the model that we want to use.

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
        if subtitles[i] == '\r\n':  # Skipping the new lines
            continue
        subtitles[i] = subtitles[i].replace('\r\n', ' ') # in the end of each line, there is \n, so I am changing it to space
        text += subtitles[i]
    f.close()
print(text) # Just checking the text
corrected_text = p.punctuate(text) # punctuate method is the one who makes punctuation on the text.
print(corrected_text) # Just checking the corrected text
with open('punctuated.txt', 'w') as f:  # Writing to the file
    f.write(corrected_text)
    f.close()
