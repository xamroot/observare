import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
	#send data, then frames.append on the client side
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

'''
Play back without saving to a WAV file
''' 

pya = pyaudio.PyAudio()

print('Playing audio...')

byte_stream = frames.tobytes()
stream2 = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=44100, output=True)
stream2.write(byte_stream)
stream2.stop_stream()
stream2.close()
pya.terminate()
 
print('Finished playback')
# repurpose the stream to simply play the data within frames


# Save the recorded data as a WAV file
'''
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
'''