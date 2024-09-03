"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import argparse

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("PeoplePerception/JustArrived")
        self.subscriber.signal.connect(self.on_human_tracked)
        self.subscriber2 = self.memory.subscriber("PeoplePerception/JustLeft")
        self.subscriber2.signal.connect(self.on_human_left)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.human_detection = session.service("ALPeoplePerception")
        self.human_detection.subscribe("HumanGreeter")

        self.currentName = ""

    def on_human_tracked(self, value):
        """
        Callback for event JustArrived.
        """
        if value != []:
            self.tts.say("Hello, what is your name?")
            open("name.txt", "w").close()
            while True:
                with open("name.txt", "r") as f:
                    text = f.read().replace('\n', '')
                    if(text != ""):
                        self.tts.say("Hello, " + text)
                        self.currentName = text
                        f.close()
                        break
            

    def on_human_left(self, value):
        if value != []:
            self.tts.say("Goodbye " + self.currentName + "!")
            #Clear text file


    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print ("Starting HumanGreeter")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print ("Interrupted by user, stopping HumanGreeter")
            self.human_detection.unsubscribe("HumanGreeter")
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.60.238.195",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()