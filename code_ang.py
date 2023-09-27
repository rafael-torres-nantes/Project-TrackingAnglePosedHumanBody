import cv2
import mediapipe as mp
import numpy as np
import csv


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


def processa_frame(image):
    """Processa um frame de vídeo e retorna os pontos de referência do corpo."""

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    return results


def desenha_landmarks(image, landmarks, connections):
    """Desenha os pontos de referência do corpo na imagem."""

    mp_drawing.draw_landmarks(image, landmarks, connections,
                             mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                             mp_drawing.DrawingSpec(color=(245, 66, 280), thickness=2, circle_radius=2))


def escreve_angulo_csv(csv_writer, frame_count, angle):
    """Escreve o frame e o ângulo no arquivo CSV."""

    csv_writer.writerow([frame_count, angle])


def main():
    """Função principal do programa."""

    cap = cv2.VideoCapture('video_manager/video_test.mp4')

    # Abre o arquivo CSV para escrita
    with open('angles.csv', mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Frame', 'Angle'])  # Escreve o cabeçalho das colunas

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            results = processa_frame(frame)
            try:

                landmarks = results.pose_landmarks.landmark

                # Calcula o ângulo entre o ombro, cotovelo e punho.
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y, 
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]

                angle = calculo_angulo(shoulder, elbow, wrist)

                # Escreve o frame e o ângulo no arquivo CSV.
                escreve_angulo_csv(csv_writer, frame_count, angle)

                # Desenha os pontos de referência do corpo na imagem.

                cv2.putText(frame, str(angle), tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            except:
                pass

            desenha_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.imshow('Imagem WebCam', frame)

            if cv2.waitKey(10) & 0XFF == ord('q'):
                break

            frame_count += 1  # Incrementa frame

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()