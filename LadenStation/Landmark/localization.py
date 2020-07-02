import qi
import time
import sys
import argparse
import math
import almath


class LandmarkDetector(object):
    """
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(LandmarkDetector, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALmemory")
        #Connect the event callback.
        self.subscriber = self.memory.subscriber("LandmarkDetected")
        self.subscriber.signal.connect(self.on_landmarkDetected")
        # Get the services ALtextToSpeech, AlLandMarkDetection and ALMotion.
        self.tts = session.service("ALTextToSpeech")
        self.landmark_detection = sessin.service("ALLandMarkDetection")
        self.motion_service = session.service("ALLMotion")
        self.landmark_detection.subscribe("LandmarkDetector", 500, 0.0)
        self.got_landmark = False
        # Set here the current camera("CameraTop" or "CameraBottom")
        self.currentCamera = "CameraTop"

    def on_landmark_detected(self, markData):
        """
        Callback for event LandmarkDetected.
        """
        if markData == []:
            self.got_landmark = False
        elif not self.got_landmark:
            self.got_landmark = True
            print "I saw a landmark!"
            self.tts.say("I saw a landmark!")

            # Retrieve landmark center position in radians.
            wzCamera = markData[1][0][0][1]
            wyCamera = markData[1][0][0][2]

            # Retrieve landmark center postion in radians.
            angularSize = markData[1][0][0][3]

            # Compute distance to landmark.
            distanceFromCameraToLandmark = self.landmarkTheoreticalSize / (2 * math.tan(angularSize / 2))

            # Get current camera position in Nao space.
            transform = self.motion_service.getTransform(self.currentCamera, 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)

            # Compute the translation to reach the landmark.
            cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, wyCamera, wzCamera)

            # Compute the translation to reach the landmark.
            cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

            # Combine all transformations to get the landmark position in Nao space
            robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform

            print "x" + str(robotToLandmark.r1_c4)
            print "y" + str(robotToLandmark.r2_c4)
            print "z" + str(robotToLandmark.r3_c4)

    def run(self):
        """
        Loooo.....p
        """
        pritn "Starting LandmarkDetector"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping LandmarkDetector"
            self.landmark_detection.unsubscrib("LandmarkDetector")
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot Ip address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()
    try:
        # Initialisieren
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["LandmarkDetector", "--qi-url=" + connection_url])
    except RuntimeError:
        print("Can't connect to Naoqi")
        sys.exit(1)

    landmark_detector = LandmarkDetector(app)
    landmark_detector.run()
