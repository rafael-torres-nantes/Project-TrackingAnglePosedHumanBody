# Project - Tracking Angle and Human Pose

## Criar Ambiente de Desenvolvimento

Para criar o ambiente, execute o comando a seguir. O comando é responsável por criar um ambiente com as bibliotecas que estão em uso no código:
```
bash create_env/create_env.sh
```

O script cria o ambiente virtual em `.env/` e já instala as dependências. Para reativar numa sessão nova de terminal:
```
source .env/bin/activate
```

|Bibliotecas Utilizadas|
|:------------:|
| Numpy |
| Mediapipe |
| Opencv-Python |
| Pandas |

`mediapipe` está fixado em `0.10.9` de propósito: a partir de versões mais novas (testado até `0.10.35`) o wheel Windows deixou de expor a API legacy `mp.solutions` (`Pose`, `drawing_utils`) usada neste código, migrando para a Tasks API. Não atualize sem migrar o código junto.

## Rodar

`code_ang.py` espera um vídeo de entrada em `sample_videos/video_test.mp4` (o repositório não versiona vídeos — coloque o arquivo manualmente antes de rodar):
```
python code_ang.py
```
