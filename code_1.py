def ler_video(caminho_do_arquivo):
  """
  Lê um arquivo de vídeo do diretório /home/user/videos.

  Args:
    caminho_do_arquivo: O caminho completo do arquivo de vídeo.

  Returns:
    Um objeto VideoFileClip da biblioteca OpenCV.
  """

  # Importa a biblioteca OpenCV.
  import cv2

  # Abre o arquivo de vídeo no modo de leitura.
  video_clip = cv2.VideoCapture(caminho_do_arquivo)

  # Verifica se o arquivo foi aberto com sucesso.
  if not video_clip.isOpened():
    raise FileNotFoundError(f"O arquivo '{caminho_do_arquivo}' não foi encontrado.")

  # Retorna o objeto VideoFileClip.
  return video_clip


# Exemplo de uso.
caminho_do_arquivo = "/home/user/videos/meu_video.mp4"
video_clip = ler_video(caminho_do_arquivo)