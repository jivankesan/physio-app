import cv2
import mediapipe as mp
import numpy as np
from collections import deque

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class PoseAngleAnalyzer:
    def __init__(self):
        self.reference_angles = []
        self.visible_joints = set()
        self.angle_buffer = deque(maxlen=10)  # Buffer to store angles for smoothening feedback
        self.joint_names = [
            'Left Elbow', 'Right Elbow', 'Left Shoulder', 'Right Shoulder',
            'Left Hip', 'Right Hip', 'Left Knee', 'Right Knee',
            'Left Wrist', 'Right Wrist', 'Left Ankle', 'Right Ankle'
        ]

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def process_frame(self, image, pose):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        angles = []
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
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
                    angle = self.calculate_angle(a, b, c)
                    angles.append(angle)
                    self.visible_joints.add(self.joint_names[keypoints.index((point1, point2, point3))])
                except:
                    angles.append(None)

        return angles, results

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    break

                angles, results = self.process_frame(image, pose)
                self.reference_angles.append(angles)

                # Make image writable to draw on it
                image.flags.writeable = True
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                cv2.imshow('Reference Video', image)
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()

    def process_live_frame(self, image):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            angles, results = self.process_frame(image, pose)
            self.angle_buffer.append(angles)

            avg_live_angles = np.array([np.mean([angle for angle in angle_list if angle is not None])
                                        for angle_list in zip(*self.angle_buffer)])
            
            return avg_live_angles, results

    def compare_with_reference(self, avg_live_angles):
        feedback = []
        for i, avg_live_angle in enumerate(avg_live_angles):
            joint_feedback = "N/A"  # Default feedback if joint data is not available
            if avg_live_angle is not None:
                closest_angle = min([ref[i] for ref in self.reference_angles if len(ref) > i], key=lambda x: abs(x - avg_live_angle))
                angle_diff = abs(closest_angle - avg_live_angle)
                sensitivity_threshold = 2

                if angle_diff < sensitivity_threshold:
                    joint_feedback = "Good"
                else:
                    joint_feedback = "Adjust"
            feedback.append(joint_feedback)

        return feedback

# Usage example
def main():
    analyzer = PoseAngleAnalyzer()

    # Process the reference video
    reference_video_path = '../exercise_videos/thigh_squat.mp4'
    analyzer.process_video(reference_video_path)

    # Open the live stream and process each frame
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        avg_live_angles, results = analyzer.process_live_frame(frame)
        joint_feedback = analyzer.compare_with_reference(avg_live_angles)

        # Display feedback for each joint
        frame.flags.writeable = True  # Make frame writable to draw on it
        for idx, feedback in enumerate(joint_feedback):
            joint_name = analyzer.joint_names[idx]
            color = (0, 255, 0) if feedback == "Good" else (0, 0, 255)
            cv2.putText(frame, f'{joint_name}: {feedback}', (10, 30 + idx * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow('Live Stream', frame)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
