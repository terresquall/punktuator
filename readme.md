Introduction
------------
To use this script, your **Python version that Windows refers to needs to be no newer than 3.9**. 
You can change it in your system environment variables.
This means that if you are using python version 3.10, the following script will not work properly.

Required Packages
-----------------
**Make sure you have the following packages:*

1. pip install numpy=1.20.3 - version is very important
2. pip install punctuator

Downloading Models
------------------
After installing packages, you need to specify the model you are going to use. You can download the models from here.

1. **Demo-Europarl-EN.pcl**: https://drive.google.com/file/d/1ZATMQiuwB8CjuWtIfRnimurwbtUfSNvG/view
2. **INTERSPEECH-T-BRN.pcl**: https://drive.google.com/file/d/148YaSz2JF4DXnwqot-7DwKQKdtB4Uraz/view
3. **INTERSPEECH-T-BRN-pre.pcl**: https://drive.google.com/file/d/1B3WzntZgZEYwF71XUYGvQ3fWOd0fiaZv/view

Put your models in the `models` folder. You will be able to select which model you want to use when running the program.

*Azat, can you update this readme with proper links to download the models?*

File Input and Output
---------------------
Put your files you want to translate into the `input` folder. Samples are included in the folder for you to test out.
Once the files are translated, you will be able to find them in the `output` folder.

Configuration
--------------
You can check out `config.json` to configure the program.

