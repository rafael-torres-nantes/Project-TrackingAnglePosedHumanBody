import cv2
import time

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


def gerar_fotos_de_video(video_clip, intervalo, pasta):
  """
  Gera fotos a cada um segundo de um vídeo.

  Args:
    video_clip: Um objeto VideoFileClip da biblioteca OpenCV.
    intervalo: O intervalo em segundos entre as fotos.

  Returns:
    Uma lista de imagens.
  """

  # Inicializa uma lista para armazenar as fotos.
  fotos = []
  cont = 0

    # Lê o vídeo frame a frame.
  while True:

    # Captura o frame atual do vídeo.
    ret, frame = video_clip.read()

    # Verifica se o fim do vídeo foi alcançado.
    if not ret:
      break

    # Adiciona o frame atual à lista de fotos.
    fotos.append(frame)

    # Salva a foto na pasta especificada.
    cv2.imwrite(f"{pasta}/{video_clip}{cont}.jpg", frame)

    # Aguarda o intervalo especificado.
    time.sleep(intervalo)

    cont += 1

  # Retorna a lista de fotos.
  return fotos


# Exemplo de uso.
caminho_do_arquivo = './sample_videos/video_test.mp4'
video_clip = importar_video(caminho_do_arquivo)
fotos = gerar_fotos_de_video(video_clip, 0.01, './frame_images')