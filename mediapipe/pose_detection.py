import cv2
import mediapipe as mp
import numpy as np
from collections import deque

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# Function to process video and get reference angles
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    reference_angles = []
    visible_joints = set()  # Set to store visible joints

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                angles = []

                # Calculate angles for key joints with proper naming
                keypoints = [
                    ('Left Elbow', mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
                    ('Right Elbow', mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
                    ('Left Shoulder', mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
                    ('Right Shoulder', mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
                    ('Left Hip', mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
                    ('Right Hip', mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
                    ('Left Knee', mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
                    ('Right Knee', mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
                    ('Left Wrist', mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST, mp_pose.PoseLandmark.LEFT_PINKY),
                    ('Right Wrist', mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST, mp_pose.PoseLandmark.RIGHT_PINKY),
                    ('Left Ankle', mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.LEFT_FOOT_INDEX),
                    ('Right Ankle', mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX)
                ]

                for joint_name, point1, point2, point3 in keypoints:
                    try:
                        a = [landmarks[point1.value].x, landmarks[point1.value].y]
                        b = [landmarks[point2.value].x, landmarks[point2.value].y]
                        c = [landmarks[point3.value].x, landmarks[point3.value].y]
                        angle = calculate_angle(a, b, c)
                        angles.append(angle)
                        visible_joints.add(joint_name)  # Mark joint as visible
                    except:
                        pass  # If points are not visible, skip

                reference_angles.append(angles)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Reference Video', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    return reference_angles, visible_joints

# Function to compare live stream with reference angles
def compare_with_live_stream(reference_angles, visible_joints):
    cap = cv2.VideoCapture(0)

    # Buffer to store angles for smoothening feedback
    angle_buffer = deque(maxlen=10)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                angles = []
                all_joints_visible = True

                # Define keypoints for comparison based on visibility in the reference video
                keypoints = [
                    ('Left Elbow', mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
                    ('Right Elbow', mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
                    ('Left Shoulder', mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
                    ('Right Shoulder', mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
                    ('Left Hip', mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
                    ('Right Hip', mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
                    ('Left Knee', mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
                    ('Right Knee', mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
                    ('Left Wrist', mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST, mp_pose.PoseLandmark.LEFT_PINKY),
                    ('Right Wrist', mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST, mp_pose.PoseLandmark.RIGHT_PINKY),
                    ('Left Ankle', mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.LEFT_FOOT_INDEX),
                    ('Right Ankle', mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX)
                ]

                for joint_name, point1, point2, point3 in keypoints:
                    if joint_name in visible_joints:  # Only process joints that were visible in the reference video
                        try:
                            a = [landmarks[point1.value].x, landmarks[point1.value].y]
                            b = [landmarks[point2.value].x, landmarks[point2.value].y]
                            c = [landmarks[point3.value].x, landmarks[point3.value].y]
                            angle = calculate_angle(a, b, c)
                            angles.append(angle)
                        except:
                            angles.append(None)  # Append None if the joint is not visible in the live stream
                            all_joints_visible = False  # Mark that not all joints are visible

                # Add angles to buffer
                angle_buffer.append(angles)

                # Average angles over the buffer for smooth feedback
                if len(angle_buffer) == angle_buffer.maxlen:
                    avg_live_angles = np.array([np.mean([angle for angle in angle_list if angle is not None])
                                                for angle_list in zip(*angle_buffer)])

                    # Track overall feedback status
                    overall_feedback = True

                    for i, avg_live_angle in enumerate(avg_live_angles):
                        if avg_live_angle is not None:  # Check if the joint was visible
                            # Find the closest reference angle to give feedback
                            closest_angle = min([ref[i] for ref in reference_angles if len(ref) > i], key=lambda x: abs(x - avg_live_angle))
                            angle_diff = abs(closest_angle - avg_live_angle)

                            # Sensitivity threshold for angles
                            sensitivity_threshold = 2  # Very high sensitivity

                            # Individual joint feedback
                            if angle_diff < sensitivity_threshold:
                                feedback = "Good"
                            else:
                                feedback = "Adjust"
                                overall_feedback = False  # If any joint needs adjustment, set overall feedback to False

                            # Visual feedback for individual joints
                            joint_name = list(visible_joints)[i]
                            color = (0, 255, 0) if feedback == "Good" else (0, 0, 255)
                            cv2.putText(image, f'{joint_name}: {feedback}', (10, 50 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
                        else:
                            overall_feedback = False  # If a joint is not visible in the live stream

                    # Overall feedback
                    overall_text = "Good" if overall_feedback and all_joints_visible else "Adjust"
                    overall_color = (0, 255, 0) if overall_text == "Good" else (0, 0, 255)
                    cv2.putText(image, f'Overall: {overall_text}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, overall_color, 2, cv2.LINE_AA)

            else:
                # If no pose landmarks are detected, the feedback should be "Adjust"
                cv2.putText(image, 'Overall: Adjust (No pose detected)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Live Stream', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()

# Main function
def main():
    # Process the reference video to get angles and visible joints
    reference_video_path = './videos/path'
    reference_angles, visible_joints = process_video(reference_video_path)

    # Compare with live stream using only the visible joints
    compare_with_live_stream(reference_angles, visible_joints)

if __name__ == "__main__":
    main()
