import cv2
import mediapipe as mp
import numpy as np
import csv

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    reference_angles = []

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * 2)  # Number of frames to skip for 2 seconds

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_count = 0
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            if frame_count % frame_interval == 0:  # Process every 2 seconds
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    angles = []

                    # Calculate angles for key joints
                    keypoints = [
                        (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST),
                        (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST),
                        (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
                        (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
                        (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
                        (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE),
                        (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE),
                        (mp_pose.PoseLandmark.RIGHT_HIP, mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE),
                        (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST, mp_pose.PoseLandmark.LEFT_PINKY),
                        (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST, mp_pose.PoseLandmark.RIGHT_PINKY),
                        (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.LEFT_FOOT_INDEX),
                        (mp_pose.PoseLandmark.RIGHT_KNEE, mp_pose.PoseLandmark.RIGHT_ANKLE, mp_pose.PoseLandmark.RIGHT_FOOT_INDEX)
                    ]

                    for point1, point2, point3 in keypoints:
                        try:
                            a = [landmarks[point1.value].x, landmarks[point1.value].y]
                            b = [landmarks[point2.value].x, landmarks[point2.value].y]
                            c = [landmarks[point3.value].x, landmarks[point3.value].y]
                            angle = calculate_angle(a, b, c)
                            angles.append(angle)
                        except:
                            angles.append(None)  # Append None if the joint is not visible

                    reference_angles.append(angles)
                    
            frame_count += 1

    cap.release()
    return reference_angles

def save_angles_to_file(video_path, output_file):
    print(f'Processing {video_path}...')
    reference_angles = process_video(video_path)
    
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the entire array of arrays as a single entry
        writer.writerow(['Reference Angles'])
        writer.writerow([reference_angles])

if __name__ == "__main__":
    video_path = '../exercise_videos/calf_standing.mp4'  # Your specified video file path
    output_file = 'reference_angles.csv'  # Can be .txt or .csv
    save_angles_to_file(video_path, output_file)
    print(f'Reference angles saved to {output_file}')
