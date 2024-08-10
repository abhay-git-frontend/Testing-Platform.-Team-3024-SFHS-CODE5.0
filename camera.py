import cv2
import face_recognition
import numpy as np

def get_gaze_direction(eye_landmarks, frame_width):
    eye_left = np.array(eye_landmarks[0])
    eye_right = np.array(eye_landmarks[1])
    eye_center = (eye_left + eye_right) / 2

    if eye_center[0] < frame_width * 0.4:
        return "left"
    elif eye_center[0] > frame_width * 0.6:
        return "right"
    else:
        return "center"

def is_gaze_out_of_screen(eye_landmarks, frame_width):
    eye_left = np.array(eye_landmarks[0])
    eye_right = np.array(eye_landmarks[1])
    eye_center = (eye_left + eye_right) / 2

    if eye_center[0] < frame_width * 0.1 or eye_center[0] > frame_width * 0.9:
        return True
    return False

def is_face_out_of_frame(face_coords, frame_width, frame_height):
    x, y, w, h = face_coords
    if x < 0.1 * frame_width or x + w > 0.9 * frame_width or y < 0.1 * frame_height or y + h > 0.9 * frame_height:
        return True
    return False

# Start video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera could not be opened.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Check if the face is out of frame
            face_coords = (left, top, right - left, bottom - top)
            if is_face_out_of_frame(face_coords, frame.shape[1], frame.shape[0]):
                cv2.putText(frame, "Alert: Face out of frame!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Extract facial landmarks
            face_landmarks = face_recognition.face_landmarks(rgb_frame)
            for landmarks in face_landmarks:
                # Extract eye landmarks
                left_eye = landmarks.get('left_eye', [])
                right_eye = landmarks.get('right_eye', [])

                if len(left_eye) > 0 and len(right_eye) > 0:
                    # Calculate the mean center of eyes
                    eye_centers = [np.mean(left_eye, axis=0), np.mean(right_eye, axis=0)]
                    gaze_direction = get_gaze_direction(eye_centers, frame.shape[1])
                    cv2.putText(frame, f"Gaze Direction: {gaze_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Check if gaze is out of screen
                    if is_gaze_out_of_screen(eye_centers, frame.shape[1]):
                        cv2.putText(frame, "Alert: Gaze out of screen!", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show the frame
        cv2.imshow('Face & Gaze Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    print("Releasing camera and closing windows...")
    cap.release()
    cv2.destroyAllWindows()
    print("Camera released and windows closed.")
