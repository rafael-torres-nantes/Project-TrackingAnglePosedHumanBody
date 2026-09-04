import utils.video_settings as utils_video
import utils.csv_settings as utils_csv

import cv2
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculo_angulo(shoulder, elbow, wrist):
    """Calcula o ângulo entre o ombro, cotovelo e punho."""

    shoulder = np.array(shoulder)
    elbow = np.array(elbow)
    wrist = np.array(wrist)

    upper_arm = elbow - shoulder
    forearm = wrist - elbow

    dot_product = np.dot(upper_arm, forearm)
    upper_arm_length = np.linalg.norm(upper_arm)
    forearm_length = np.linalg.norm(forearm)

    cosine_angle = dot_product / (upper_arm_length * forearm_length)
    angle_radians = np.arccos(cosine_angle)
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees


def processa_frame(image, pose):
    """Processa um frame de vídeo e retorna os pontos de referência do corpo."""

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return results


def desenha_landmarks(image, landmarks, connections):
    """Desenha os pontos de referência do corpo na imagem."""

    mp_drawing.draw_landmarks(image, landmarks, connections,
                             mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                             mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))


def main():
    """Função principal do programa."""

    FOLDER_IMAGE_PATH = 'frame_images'
    IMPORT_NAME_VIDEO = 'video_test.mp4'
    
    OUT_FILENAME_CSV = 'angles'
    OUT_FILENAME_VIDEO = 'mulher'

    csv_file = utils_csv.create_csv(OUT_FILENAME_CSV)

    frame_count = 0
    cap = utils_video.importar_video(IMPORT_NAME_VIDEO)

    utils_video.remove_files()

    min_visibility = 0.5

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            results = processa_frame(frame, pose)
            try:
                landmarks = results.pose_landmarks.landmark

                shoulder_lm = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                elbow_lm = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                wrist_lm = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

                if min(shoulder_lm.visibility, elbow_lm.visibility, wrist_lm.visibility) < min_visibility:
                    raise ValueError("braço esquerdo fora de quadro ou oculto")

                # Calcula o ângulo entre o ombro, cotovelo e punho.
                shoulder = [shoulder_lm.x, shoulder_lm.y, shoulder_lm.z]
                elbow = [elbow_lm.x, elbow_lm.y, elbow_lm.z]
                wrist = [wrist_lm.x, wrist_lm.y, wrist_lm.z]

                angle = calculo_angulo(shoulder, elbow, wrist)

                # Escreve o frame e o ângulo no arquivo CSV.
                utils_csv.write_csv_ang(csv_file, frame_count, angle, OUT_FILENAME_CSV)

                # Desenha o ângulo na imagem.
                cv2.putText(frame, str(angle), tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            except (AttributeError, ValueError) as exc:
                print(f"Frame {frame_count}: ângulo não calculado ({exc}).")

            desenha_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            utils_video.frames_from_video(frame, frame_count, OUT_FILENAME_VIDEO, FOLDER_IMAGE_PATH)

            cv2.imshow('Imagem WebCam', frame)

            if cv2.waitKey(10) & 0XFF == ord('q'):
                break

            frame_count += 1  # Incrementa frame

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()