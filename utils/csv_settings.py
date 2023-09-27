import pandas as pd

def criar_csv():

    # Cria um DataFrame com as colunas "Frame" e "Angle"
    csv_file = pd.DataFrame({"Frame": [], "Angle": []})

    # Escreve o cabeçalho do DataFrame no arquivo CSV
    csv_file.to_csv("angles1.csv", index=False)

    return csv_file


def write_angulo(csv_file, frame_count, angle):
    """Escreve o frame e o ângulo no DataFrame."""

    # Adiciona uma nova linha ao DataFrame
    csv_file.loc[len(csv_file)] = [frame_count, angle]
    csv_file['Frame'].astype(int)

    # Atualiza o DataFrame no arquivo CSV
    csv_file.to_csv("angles1.csv", index=False)