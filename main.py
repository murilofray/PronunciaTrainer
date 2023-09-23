import random
import sounddevice as sd
import wavio
import difflib

nome_arquivo = "audio.wav"
idiomas = {'1': 'pt', '2': 'en', '3': 'es'}
idioma = ""

# Dicionário de palavras e frases para cada nível de dificuldade
exercicios = {
    'pt': {
        'facil': ['água', 'sol', 'amor'],
        'intermediario': ['paralelepípedo', 'hipopotomonstrosesquipedaliofobia', 'anticonstitucionalissimamente'],
        'dificil': ['inconstitucionalissimamente', 'plenissimamente', 'anticonstitucional']
    },
    'en': {
        'facil': ['water', 'sun', 'love'],
        'intermediario': ['supercalifragilisticexpialidocious', 'pneumonoultramicroscopicsilicovolcanoconiosis',
                          'antiestablishmentarianism'],
        'dificil': ['floccinaucinihilipilification', 'sesquipedalian', 'anticonstitutional']
    },
    'es': {
        'facil': ['agua', 'sol', 'amor'],
        'intermediario': ['hipopotomonstrosesquipedaliofobia', 'supercalifragilisticoespialidoso',
                          'anticonstitucionalidad'],
        'dificil': ['neumonoultramicroscopicosilicovolcanoconiosis', 'paralelepipedo', 'anticonstitucional']
    }
}


def escolher_idioma():
    while True:
        print("Escolha o idioma para o treinamento de dicção:")
        print("1 - Português 2 - Inglês 3 - Espanhol")
        escolha = input()
        if escolha in idiomas:
            return idiomas[escolha]
        else:
            print("Opção inválida")


def escolher_nivel_dificuldade():
    niveis = ['facil', 'intermediario', 'dificil']
    while True:
        print("Escolha o nível de dificuldade:")
        print("1 - Fácil 2 - Intermediário 3 - Difícil")
        escolha = input()
        if escolha in ['1', '2', '3']:
            return niveis[int(escolha) - 1]
        else:
            print("Opção inválida")


def treinamento_diccao():
    nivel = escolher_nivel_dificuldade()

    # Selecionar uma palavra ou frase aleatória do nível escolhido
    exercicio = random.choice(exercicios[idioma][nivel])

    print(f"Treinamento de dicção em {idioma} - Nível: {nivel}")
    print(f"Repita a seguinte palavra/frase claramente:")
    print(exercicio)

    # Gravar a pronúncia do usuário
    duracao = len(exercicio) * 0.7
    gravar_audio(duracao)
    print("Exercício concluído!")
    return exercicio


def transcreverAudio():
    modelo = whisper.load_model("small")
    resultado = modelo.transcribe(nome_arquivo, fp16=False, language=idioma)
    transcricao = resultado["text"]
    return transcricao


def gravar_audio(duracao):
    print('Gravando...\n')
    dados_audio = sd.rec(int(duracao * 44100), samplerate=44100, channels=1)
    sd.wait()
    wavio.write(nome_arquivo, dados_audio, 44100, sampwidth=3)


def calcular_porcentagem_similaridade(str1, str2):
    def distancia_edicao(str1, str2):
        len_str1 = len(str1) + 1
        len_str2 = len(str2) + 1

        matriz = [[0] * len_str2 for _ in range(len_str1)]

        for i in range(len_str1):
            matriz[i][0] = i

        for j in range(len_str2):
            matriz[0][j] = j

        for i in range(1, len_str1):
            for j in range(1, len_str2):
                custo = 0 if str1[i - 1] == str2[j - 1] else 1
                matriz[i][j] = min(
                    matriz[i - 1][j] + 1,  # Deleção
                    matriz[i][j - 1] + 1,  # Inserção
                    matriz[i - 1][j - 1] + custo  # Substituição
                )

        return matriz[len_str1 - 1][len_str2 - 1]

    distancia = distancia_edicao(str1, str2)
    max_len = max(len(str1), len(str2))
    similaridade = ((max_len - distancia) / max_len) * 100.0

    return similaridade


if __name__ == "__main__":
    idioma = escolher_idioma()
    while True:
        exercicio = treinamento_diccao()
        palavraFalada = transcreverAudio()
        print("\nDeseja continuar treinando dicção? (s/n)")
        continuar = input()
        porcentagem = calcular_porcentagem_similaridade(exercicio, palavraFalada)
        print(f"Porcentagem de dicção': {porcentagem:.2f}%")
        if continuar.lower() != 's':
            break

