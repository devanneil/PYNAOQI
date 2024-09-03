import speech_recognition as sr
import time

microphones = sr.Microphone.list_microphone_names()
for index, name in enumerate(microphones):
  print(f"Microphone with index {index} and name \"{name}\" found")

# Initialize the recognizer
r = sr.Recognizer()
def speak(mic,person):
	while True:
		with sr.Microphone(device_index=mic) as source:
			with open("name.txt", "r") as f:
				if(f.read() == ""):
					r.adjust_for_ambient_noise(source)
				
					print("Listening...")
					audio = r.listen(source)
					print("Stop Listening")
				
					try:
						# using google to transcribe the audio file to text
						text = r.recognize_google(audio)
						print("mic " + str(mic) + " " + person + " said: " + text)

						with open("name.txt", "w") as w:
							w.write(text)
							w.close()
					except Exception as e:
						print(f"An error occurred: {e}")

		time.sleep(1)	

speak(0, "Human")