import qi
import time
import sys
import argparse


class LandmarkDetector(object):
    """
    """

    def __init__(self, app):
        """
        Initalisierung
        """
        super(LandmarkDetector, self).__init()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscribrt("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmark_detected)
        # Get the service ALTextToSpeech and ALLandMarkDetection.
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = session.service("ALLandMarkDetection")
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0)
        self.got_landmark = False

    def on_landmark_detected(self, value):
        """
        Callback for event LandmarkDetected.
        """
        if value == []:
            self.got_landmark = False
        elif not self.got_landmark:  # Only speak the first time a landmark appears
            self.got_landmark = True
            print "I saw a landamrk!"
            self.tts.say("There is a landmark!)
            # First Field = TimeStamp
            timeStamp = value[0]
            print "TimeStamp is:" + str(timeStamp)

            # Second Field = array of mark_Info's.
            markInfoArray = value[1]
            for markInfo in markInfoArray:

                # First Field = Shape info.
                markShapeInfo = markInfo[0]

                # Second Field = Extra info(ie, mark ID)
                markExtraInfo = markInfo[1]
                print "mark ID: %d" % (markShapleInfo)
                print " appha %.3f - beta %.3f" % (markShapeInfo[1], markShapeInfo[2])
                print " width %.3f - height %.3f" % (markShapeInfo[3], markShapeInfo[4])

    def run(self):
        """
        loop on
        """
        print "Starting LandmarkDetector"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping LandmarkDetector"
            self.landmark_detection.unsubscrib("LanmarkDetector")            
            #stop
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str,default="127.0.0.1",
                        help="Robot Ip address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int,default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()
    try:
        # Initialisieren
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi,Application(["LandmarkDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print("Can't connect to Naoqi")
        sys.exit(1)

    landmark_detector = LandmarkDetector(app)
    landmark_detector.run()


