import json
import time

# Read JSON file
with open('test.json', 'r') as file:
    data = json.load(file)

# Initialize variables with "good" status
lShoulder = "good"
rShoulder = "good"
lElbow = "good"
rElbow = "good"
lWrist = "good"
rWrist = "good"
lHip = "good"
rHip = "good"
lKnee = "good"
rKnee = "good"
lAnkle = "good"
rAnkle = "good"
i = 0

# While camera is on
while i < 60:  # Placeholder for camera
    message_printed = False 

    for point in data:
        time.sleep(1)
        joint_info = point["joint"] + " " + point["good_or_adjust"]

        if "left_shoulder" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != lShoulder:
                if not message_printed: 
                    print(f"Voiceflow: {joint_info}") # Placeholder for Voiceflow API
                    message_printed = True
                lShoulder = point["good_or_adjust"]
                continue 
            lShoulder = point["good_or_adjust"]

        elif "right_shoulder" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != rShoulder:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                rShoulder = point["good_or_adjust"]
                continue
            rShoulder = point["good_or_adjust"]

        elif "left_elbow" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != lElbow:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                lElbow = point["good_or_adjust"]
                continue
            lElbow = point["good_or_adjust"]

        elif "right_elbow" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != rElbow:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                rElbow = point["good_or_adjust"]
                continue
            rElbow = point["good_or_adjust"]

        elif "left_wrist" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != lWrist:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                lWrist = point["good_or_adjust"]
                continue
            lWrist = point["good_or_adjust"]

        elif "right_wrist" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != rWrist:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                rWrist = point["good_or_adjust"]
                continue
            rWrist = point["good_or_adjust"]

        elif "left_hip" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != lHip:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                lHip = point["good_or_adjust"]
                continue
            lHip = point["good_or_adjust"]

        elif "right_hip" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != rHip:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                rHip = point["good_or_adjust"]
                continue
            rHip = point["good_or_adjust"]

        elif "left_knee" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != lKnee:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                lKnee = point["good_or_adjust"]
                continue
            lKnee = point["good_or_adjust"]

        elif "right_knee" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != rKnee:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                rKnee = point["good_or_adjust"]
                continue
            rKnee = point["good_or_adjust"]

        elif "left_ankle" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != lAnkle:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                lAnkle = point["good_or_adjust"]
                continue
            lAnkle = point["good_or_adjust"]

        elif "right_ankle" in point["joint"]:
            if point["good_or_adjust"] == "adjust" or point["good_or_adjust"] != rAnkle:
                if not message_printed:
                    print(f"Voiceflow: {joint_info}")
                    message_printed = True
                rAnkle = point["good_or_adjust"]
                continue
            rAnkle = point["good_or_adjust"]

    i += 1 #placeholder for camera
    time.sleep(2)