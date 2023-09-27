import cv2
import time

count = 0

PlaceHolder = "PlaceHolder"

def importar_video(caminho_do_arquivo):
  """
  Importa um vídeo de algum diretório.

  Args:
    caminho_do_arquivo: O caminho completo do arquivo de vídeo.

  Returns:
    Um objeto VideoFileClip da biblioteca OpenCV.
  """

  # Abre o arquivo de vídeo no modo de leitura.
  video_clip = cv2.VideoCapture(caminho_do_arquivo)

  # Verifica se o arquivo foi aberto com sucesso.
  if not video_clip.isOpened():
    raise FileNotFoundError(f"O arquivo '{caminho_do_arquivo}' não foi encontrado.")

  # Retorna o objeto VideoFileClip.
  return video_clip


def frames_from_video(frame, pasta, intervalo = 0.01):
  """
  Gera fotos a cada um segundo de um vídeo.

  Args:
    video_clip: Um objeto VideoFileClip da biblioteca OpenCV.
    intervalo: O intervalo em segundos entre as fotos.

  Returns:
    Uma lista de imagens.
  """
  global count
  
  # Salva a foto na pasta especificada.
  cv2.imwrite(f"{pasta}/{PlaceHolder}{count}.jpg", frame)
  count += 1
  
  time.sleep(intervalo)


# # Exemplo de uso.
# caminho_do_arquivo = './sample_videos/video_test.mp4'
# video_clip = importar_video(caminho_do_arquivo)
# gerar_fotos_de_video(video_clip, 0.01, './frame_images')