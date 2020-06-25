import qi
import time
import sys
import argparse


class LandmarkDetector(object):
    """
    Landmark finden und die Information der Landmark zurueckgeben
    """
    
    def __init__(self, app):
        """
        Veranstaltung erkennen und Initialisierung von qi Framework
        """
        super(LandmarkDetector, self).__init__()
        app.start()
        session = app.session()
        # ALMemory
        self.memory = session.service("ALMemory")
        # Verbinden mit Callbak der Veranstaltung
        self.subscriber = self.memory.subscriber("Landmarkdetected")
        self.subscriber.signal.connect(self.on_landmarkDetected)
        # ALTextToSpeech ALLandMark erkennen
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = session.service("ALLandMarkDetection")
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0)
        self.got_landmark = False

    def on_landmark_detected(self, value):
        """
        Callback fuer die Veranstaltung des LandmarkDetected
        """
        if value == []:
            self.got_landmark = False
        elif not self.got_landmark:
            self.got_landmark = True
            print "I saw a lanmark!"
            self.tts.say("I saw a landmark!")
            # Timestamp ist der erste Parameter der Value
            timeStamp = value[0]
            print "TimeStamp ist:" + str(timeStamp)

            # Zweite ist array of mark_Info's
            markInfoArray = value[1]
            for markInfo in markInfoArray:
                # Information des Form von Landmark
                markShapeInfo = markInfo[0]

                # zusaetzlichen Informationen
                markExtraInfo = markInfo[1]

                print "  mark  ID: %d" % (markExtraInfo[0])
                print "  alpha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                print "  width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])
    
    def run(self):
        """
        Loop on, wait for events until manual interuption
        """
        print "Starting LandmarkDetector"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping LandmarkDetector"
            self.landmark_detection.unsubscribe("LandmarkDetector")
            #stop
            sys.exit(0)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                            help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=2768,
                            help="Naoqi port number")
    
    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["LandmarkDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
            "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    landmark_detector = LandmarkDetector(app)
    landmark_detector.run()
