import os
import re
from pydub import AudioSegment

def limpar_nome_arquivo(nome):
    # Remove padrões como '[Sej3Uc5kgUo]' incluindo colchetes e o conteúdo dentro
    nome_limpo = re.sub(r'\[[a-zA-Z0-9_-]{11}\]', '', nome)
    # Remove espaços duplos que possam sobrar e remove espaços no início/fim
    nome_limpo = re.sub(r'\s+', ' ', nome_limpo).strip()
    return nome_limpo

def converter_estrutura_pastas():
    pasta_webm_base = "webm"
    pasta_mp3_base = "mp3"
    
    if not os.path.exists(pasta_webm_base):
        print(f"Erro: A pasta '{pasta_webm_base}' não foi encontrada.")
        return

    for album in os.listdir(pasta_webm_base):
        caminho_webm_album = os.path.join(pasta_webm_base, album)
        
        if os.path.isdir(caminho_webm_album):
            caminho_mp3_album = os.path.join(pasta_mp3_base, album)
            
            if not os.path.exists(caminho_mp3_album):
                os.makedirs(caminho_mp3_album)
                print(f"Pasta criada: {caminho_mp3_album}")
            
            for arquivo in os.listdir(caminho_webm_album):
                if arquivo.endswith(".webm"):
                    caminho_entrada = os.path.join(caminho_webm_album, arquivo)
                    
                    # Separa o nome da extensão (.webm)
                    nome_sem_extensao, _ = os.path.splitext(arquivo)
                    
                    # Aplica a limpeza para remover o código do YouTube
                    nome_limpo = limpar_nome_arquivo(nome_sem_extensao)
                    
                    # Define o caminho de saída com o novo nome limpo
                    caminho_saida = os.path.join(caminho_mp3_album, f"{nome_limpo}.mp3")
                    
                    if os.path.exists(caminho_saida):
                        print(f"Pulando (já convertido): {nome_limpo}.mp3")
                        continue
                    
                    try:
                        print(f"Convertendo [{album}]: {nome_limpo}.mp3 ...")
                        audio = AudioSegment.from_file(caminho_entrada, format="webm")
                        audio.export(caminho_saida, format="mp3", bitrate="192k")
                    except Exception as e:
                        print(f"Falha ao converter {arquivo} no {album}: {e}")

    print("\nProcesso de conversão e renomeação concluído!")

if __name__ == "__main__":
    converter_estrutura_pastas()
