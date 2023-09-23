import random
import sounddevice as sd
import wavio
import whisper
from typing import List

nome_arquivo = "audio.wav"
idiomas = {'1': 'pt', '2': 'en', '3': 'es'}
idioma = ""

exercicios = {
    'pt': {
        'facil': [
            'Água', 'Sol', 'Amor', 'Casa', 'Azul', 'Flores', 'Gato', 'Família', 'Trabalho', 'Música',
            'Felicidade', 'Verão', 'Computador', 'Livro', 'Escola', 'Praia', 'Amizade', 'Coração', 'Chocolate'
        ],
        'intermediario': [
            'Paralelepípedo', 'Procrastinação', 'Imperturbabilidade', 'Indissolubilidade', 'Antissocial',
            'Inconstitucionalissimamente', 'Esquizofrenia', 'Laboratório',
        ],
        'dificil': [
            'Anticonstitucionalissimamente', 'Excepcional', 'Determinação', 'Palimpsesto',
            'Eletroencefalograma',
            'Incompreensibilidade', 'Hipopotomonstrosesquipedaliofobia'
        ]
    },
    'es': {
        'facil': [
            'Agua', 'Sol', 'Amor', 'Casa', 'Azul', 'Flores', 'Gato', 'Familia', 'Trabajo', 'Música',
            'Felicidad', 'Verano', 'Computadora', 'Libro', 'Escuela', 'Playa', 'Amistad', 'Corazón', 'Chocolate'
        ],
        'intermediario': [
            'Adoquín','Dilación', 'Esquizofrenia', 'Incomprensibilidad'
        ],
        'dificil': [
            'No constitucional', 'ninõ', 'incumbencia', 'cepillo'
        ]
    },
    'en': {
        'facil': [
            'Water', 'Sun', 'Love', 'House', 'Blue', 'Flowers', 'Cat', 'Family', 'Work', 'Music',
            'Happiness', 'Summer', 'Computer', 'Book', 'School', 'Beach', 'Friendship', 'Heart', 'Chocolate'
        ],
        'intermediario': [
            'Supercalifragilisticexpialidocious', 'Pneumonoultramicroscopicsilicovolcanoconiosis',
            'Antiestablishmentarianism',
            'Floccinaucinihilipilification', 'Sesquipedalian', 'Anticonstitutional', 'Exceptional', 'Procrastination',
            'Determination', 'Schizophrenia'
        ],
        'dificil': [
            'Electroencephalographically', 'Incomprehensibilities', 'Antiestablishmentarian', 'Counterdemonstration',
            'Counterproductiveness',
            'Counselorship', 'Hipopotomonstrosesquipedaliofobia', 'Paralelepipedo', 'Anticonstitucionalidad',
            'Neumonoultramicroscopicosilicovolcanoconiosis'
        ]
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
    print("Aperte enter para começar")
    input()
    # Gravar a pronúncia do usuário
    if len(exercicio) < 5:
        duracao = len(exercicio) * 0.7
    elif len(exercicio) < 15:
        duracao = len(exercicio) * 0.5
    else:
        duracao = len(exercicio) * 0.3

    gravar_audio(duracao)
    print("Exercício concluído!")
    print("Aguarde...")
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


def calcular_similaridade_fonetica_en(word1: str, word2: str) -> float:
    def caverphone2(input: str) -> str:
        # Implementação do algoritmo Caverphone 2.0 para o inglês
        __vowels: List[str] = ["a", "e", "i", "o", "u"]

        # Step 1.
        if input.endswith("s"):
            input = input[:-1]

        # Step 2.
        input = input.replace("ce", "se")
        input = input.replace("ci", "si")
        input = input.replace("cy", "sy")
        input = input.replace("tch", "2ch")
        input = input.replace("c", "k")
        input = input.replace("q", "k")
        input = input.replace("x", "k")
        input = input.replace("v", "f")
        input = input.replace("dg", "2g")
        input = input.replace("tio", "sio")
        input = input.replace("tia", "sia")
        input = input.replace("d", "t")
        input = input.replace("ph", "fh")
        input = input.replace("b", "p")
        input = input.replace("sh", "s2")
        input = input.replace("z", "s")

        # Step 3.
        output = ""
        for index, char in enumerate(input):
            if char in __vowels:
                output += "A" if index == 0 else "3"
            else:
                output += char
        input = output

        # Step 4.
        input = input.replace("j", "y")

        # Step 5.
        if input.startswith("y3"):
            input = input.replace("y3", "Y3", 1)
        if input.startswith("y"):
            input = input.replace("y", "A")

        # Step 6.
        input = input.replace("y", "3")

        # Step 7.
        input = input.replace("3gh3", "3kh3")
        input = input.replace("gh", "22")
        input = input.replace("g", "k")

        # Step 8.
        input = input.replace("2", "")

        # Step 9.
        if input.endswith("3"):
            input = input[:-1] + "A"

        # Step 10.
        input = input.replace("3", "")

        # Steps 11-12.
        input = input.ljust(10, "1")

        return input

    code1 = caverphone2(word1)
    code2 = caverphone2(word2)

    num_caracteres_iguais = sum(1 for a, b in zip(code1, code2) if a == b)

    max_length = max(len(code1), len(code2))
    similaridade = (num_caracteres_iguais / max_length) * 100.0

    return similaridade


def calcular_similaridade_fonetica_pt(word1: str, word2: str) -> float:
    __vowels: List[str] = ["a", "e", "i", "o", "u", "á", "â", "ã", "à", "é", "ê", "í", "ó", "ô", "õ", "ú"]

    def caverphone2_pt(input: str) -> str:
        input = input.lower()
        input = ''.join(char for char in input if char.isalpha())

        if input.endswith("e"):
            input = input[:-1]

        replacements = {
            "ch": "X",
            "lh": "L",
            "nh": "N",
            "gu": "G",
            "qu": "Q",
        }
        for pattern, replacement in replacements.items():
            input = input.replace(pattern, replacement)

        output = ""
        for char in input:
            if char in __vowels:
                output += "A"
            else:
                output += char

        output = output.replace("b", "B")
        output = output.replace("c", "C")
        output = output.replace("d", "D")
        output = output.replace("f", "F")
        output = output.replace("g", "G")
        output = output.replace("h", "H")
        output = output.replace("j", "J")
        output = output.replace("k", "K")
        output = output.replace("l", "L")
        output = output.replace("m", "M")
        output = output.replace("n", "N")
        output = output.replace("p", "P")
        output = output.replace("q", "Q")
        output = output.replace("r", "R")
        output = output.replace("s", "S")
        output = output.replace("t", "T")
        output = output.replace("v", "V")
        output = output.replace("w", "W")
        output = output.replace("x", "X")
        output = output.replace("z", "Z")

        output = output.replace("1", "")
        output = output.replace("3", "")
        output = output.ljust(6, "1")

        return output

    code1 = caverphone2_pt(word1)
    code2 = caverphone2_pt(word2)

    num_caracteres_iguais = sum(1 for a, b in zip(code1, code2) if a == b)

    max_length = max(len(code1), len(code2))
    similaridade = (num_caracteres_iguais / max_length) * 100.0

    return similaridade


# Função para calcular similaridade fonética para o Espanhol
def calcular_similaridade_fonetica_es(word1: str, word2: str) -> float:
    __vowels: List[str] = ["a", "e", "i", "o", "u", "á", "é", "í", "ó", "ú"]

    def caverphone2_es(input: str) -> str:
        input = input.lower()
        input = ''.join(char for char in input if char.isalpha())

        if input.endswith("e"):
            input = input[:-1]

        replacements = {
            "ll": "Y",
            "ñ": "N",
            "rr": "R",
            "ch": "X",
            "gu": "G",
            "qu": "Q",
        }
        for pattern, replacement in replacements.items():
            input = input.replace(pattern, replacement)

        output = ""
        for char in input:
            if char in __vowels:
                output += "A"
            else:
                output += char

        output = output.replace("b", "B")
        output = output.replace("c", "C")
        output = output.replace("d", "D")
        output = output.replace("f", "F")
        output = output.replace("g", "G")
        output = output.replace("h", "H")
        output = output.replace("j", "J")
        output = output.replace("k", "K")
        output = output.replace("l", "L")
        output = output.replace("m", "M")
        output = output.replace("n", "N")
        output = output.replace("p", "P")
        output = output.replace("q", "Q")
        output = output.replace("r", "R")
        output = output.replace("s", "S")
        output = output.replace("t", "T")
        output = output.replace("v", "V")
        output = output.replace("w", "W")
        output = output.replace("x", "X")
        output = output.replace("z", "Z")

        output = output.replace("1", "")
        output = output.replace("3", "")
        output = output.ljust(6, "1")

        return output

    code1 = caverphone2_es(word1)
    code2 = caverphone2_es(word2)

    num_caracteres_iguais = sum(1 for a, b in zip(code1, code2) if a == b)

    max_length = max(len(code1), len(code2))
    similaridade = (num_caracteres_iguais / max_length) * 100.0

    return similaridade


# Função que recebe as duas palavras e a string do idioma
def calcular_similaridade_fonetica(word1: str, word2: str, idioma: str) -> float:
    if idioma == "pt":
        return calcular_similaridade_fonetica_pt(word1, word2)
    elif idioma == "en":
        return calcular_similaridade_fonetica_en(word1, word2)
    elif idioma == "es":
        return calcular_similaridade_fonetica_es(word1, word2)
    else:
        raise ValueError("Idioma não suportado")


if __name__ == "__main__":
    idioma = escolher_idioma()
    while True:
        exercicio = treinamento_diccao()
        exercicio = exercicio.lower()
        palavraFalada = transcreverAudio()
        palavraFalada = palavraFalada.lower()
        palavraFalada = ''.join(char for char in palavraFalada if char.isalnum())
        porcentagem = calcular_similaridade_fonetica(exercicio, palavraFalada, idioma)
        print("Palavra falada:", palavraFalada, "Palavra do exercicio:", exercicio)
        print(f"Porcentagem de igualdade seguindo o algoritmo caverphone2:{porcentagem:.2f}%")
        print("\nDeseja continuar treinando dicção? (s/n)")
        continuar = input()
        if continuar.lower() != 's':
            break
