import cv2
import numpy as np
import mediapipe as mp
from skimage import exposure
from mediapipe.framework.formats import landmark_pb2


def denoise(img):
    # Denoise
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    return img


def equalize(image):
    try:
        img_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Split the LAB image into L, A, and B channels
        l_channel, a_channel, b_channel = cv2.split(img_lab)

        # Calculate the histogram of the L channel
        hist_original, _ = np.histogram(l_channel.flatten(), 256, [0, 256])
        cdf_original = hist_original.cumsum()
        percentage_darker_side = (cdf_original[128] / cdf_original[-1]) * 100

        # Check if more than 65% of pixels are on the darker side
        if percentage_darker_side >= 65:
            l_channel_float = l_channel.astype(float)
            l_channel_equalized = exposure.equalize_hist(l_channel_float)
            l_channel_equalized_uint8 = (l_channel_equalized * 255).astype(np.uint8)

            # Merge the equalized L channel with the original A and B channels
            img_lab_equalized = cv2.merge(
                [l_channel_equalized_uint8, a_channel, b_channel]
            )
            img_equalized_bgr = cv2.cvtColor(img_lab_equalized, cv2.COLOR_LAB2BGR)

            return img_equalized_bgr
        else:
            return image
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None


def landmarks(img):
    landmars_data = []
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils
    results = pose.process(img)

    def draw_landmarks_on_image(rgb_image, detection_result):
        annotated_image = np.copy(rgb_image)

        if detection_result.pose_landmarks:
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x, y=landmark.y, z=landmark.z
                    )
                    for landmark in detection_result.pose_landmarks.landmark
                ]
            )
            mp_drawing.draw_landmarks(
                annotated_image,
                pose_landmarks_proto,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),
            )
        return annotated_image

    if results.pose_landmarks:
        img = draw_landmarks_on_image(img, results)
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        landmars_data.append(landmarks)

    return img, landmars_data
