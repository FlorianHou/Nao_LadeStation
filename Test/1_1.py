import qi
import argparse
import sys

def main(session):
    """do Something"""
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    motion_service.moveTo(0.5, 0, 90)
    posture_service.goToPosture("StandZero", 0.5)
    # motion_service.rest()
    names = "Body"
    stiffnessLists = 0.0
    timeLists = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    # print motion state
    print motion_service.getSummary()
    
if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--ip", type=str, default="127.0.0.1", help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    # parser.add_argument("--port", type=int, default=9559, help="Naoqi port number")
    # args = parser.parse_args()
    session = qi.Session()
    try:
        # session.connect("tcp://" + args.ip + ":" + str(args.port))
        session.connect("tcp://" + raw_input("--ip:") + ":" + raw_input("--port"))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit()
    main(session)