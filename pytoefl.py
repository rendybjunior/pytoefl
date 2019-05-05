import pyaudio
import wave
import random
import datetime
import time


f = open("speaking_questions.txt","r+")
questions = f.readlines()
current_question_idx = random.randint(0, len(questions)-1)
current_question = questions[current_question_idx]

print("Question:")
print(current_question)
raw_input("Read the question and press Enter to continue...")

print("")
print("You now have 15 seconds to prepare your answer")
delay = 15
for i in range (0, delay):
    print("Time remaining: {} seconds".format(delay - i))
    time.sleep(1)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 45

now = datetime.datetime.now()
WAVE_OUTPUT_FILENAME = now.strftime("%Y-%m-%d") + " " + ('%03d' % current_question_idx) + " " + current_question[:50] + ".wav"

print("")
print("You now have 45 seconds to record your answer")
time.sleep(1)
print("* recording")

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []
current_sec = 0
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    new_sec = int(i * CHUNK / RATE) + 1
    if new_sec != current_sec:
        current_sec = new_sec
        print(("Time remaining: {} seconds").format(RECORD_SECONDS - current_sec + 1))

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()