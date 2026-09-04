import os
import cv2
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def importar_video(filename):
  """
  Importa um vídeo de algum diretório.

  Args:
    caminho_do_arquivo: O caminho completo do arquivo de vídeo.

  Returns:
    Um objeto VideoFileClip da biblioteca OpenCV.
  """

  # Caminho absoluto a partir da raiz do repositório, independente do cwd de onde o script roda.
  video_path = os.path.join(BASE_DIR, 'sample_videos', filename)

  # Abre o arquivo de vídeo no modo de leitura.
  video_clip = cv2.VideoCapture(video_path)

  # Verifica se o arquivo foi aberto com sucesso.
  if not video_clip.isOpened():
    raise FileNotFoundError(f"O arquivo '{video_path}' não foi encontrado. Coloque o vídeo em sample_videos/.")

  # Retorna o objeto VideoFileClip.
  return video_clip

def importar_webcam():
  """
  Importa um vídeo de algum diretório.

  Args:
    caminho_do_arquivo: O caminho completo do arquivo de vídeo.

  Returns:
    Um objeto VideoFileClip da biblioteca OpenCV.
  """

  # Abre o arquivo de vídeo no modo de leitura.
  webcam = cv2.VideoCapture(0)

  # Verifica se o arquivo foi aberto com sucesso.
  if not webcam.isOpened():
    raise FileNotFoundError("Webcam não foi encontrada.")

  # Retorna o objeto VideoFileClip.
  return webcam


def frames_from_video(frame, frame_count, filename, folderfile='frame_images'):
  """
  Gera fotos a cada um segundo de um vídeo.

  Args:
    video_clip: Um objeto VideoFileClip da biblioteca OpenCV.
    intervalo: O intervalo em segundos entre as fotos.

  Returns:
    Uma lista de imagens.
  """  
  # Salva a foto na pasta especificada.
  cv2.imwrite(f"{folderfile}/{filename}__{frame_count}.jpg", frame)
  
  time.sleep(0.01)


def remove_files(caminho_pasta = 'frame_images/'):
    """Remove todos os arquivos de uma pasta."""

    # Obtém uma lista de todos os arquivos na pasta
    arquivos = os.listdir(caminho_pasta)

    # Percorre a lista de arquivos
    for arquivo in arquivos:
        # Remove o arquivo JPG
        if arquivo.endswith(".jpg"):
          os.remove(os.path.join(caminho_pasta, arquivo))

# # Exemplo de uso.
# caminho_do_arquivo = './sample_videos/video_test.mp4'
# video_clip = importar_video(caminho_do_arquivo)
# gerar_fotos_de_video(video_clip, 0.01, './frame_images')