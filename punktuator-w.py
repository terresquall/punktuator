from punctuator import Punctuator

p = Punctuator('/Users/azvt/PycharmProjects/pythonProject/venv/lib/python3.9/site-packages/punctuator/Demo-Europarl-EN.pcl')

# works not ideal, because '*' prevents program from doing its work properly
with open('/Users/azvt/Downloads/captions.sbv', 'r+') as f:
    subtitles = f.readlines()
    f.seek(0)
    text = ''
    timings = []
    for i in range(len(subtitles)):
        if i % 3 == 0:
            subtitles[i] = subtitles[i].strip()
            timings.append(subtitles[i])
            continue
        if subtitles[i] == '\n':
            continue
        subtitles[i] = subtitles[i].replace('\n', '')
        text += subtitles[i] + '*'
    f.close()

corrected_text = p.punctuate(text)
print(text)
print(corrected_text)
formatted_text = corrected_text.split('*')
with open('/Users/azvt/Desktop/captions.sbv', 'w') as f:
    for i in range(len(timings)):
        f.write(timings[i] + "\n")
        if i != len(timings) - 1:
            f.write(formatted_text[i] + "\n")
        else:
            f.write(formatted_text[i] + '.')