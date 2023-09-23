# PronunciaTrainer

PronunciaTrainer é um projeto desenvolvido para treinar a dicção e a pronúncia em diferentes idiomas. Foi criado com o objetivo de testar o módulo Whisper e converter o algoritmo Caverphone 2.0 para outros idiomas. É importante observar que este projeto foi desenvolvido em um curto período de tempo e não foi projetado para uso em produção. Portanto, não há garantia de que funcione realmente para treinamento de pronuncia.

## Autor do Algoritmo Caverphone 2.0 usado no projeto

O algoritmo Caverphone 2.0 usado no projeto foi originalmente desenvolvido por Kamau Washington. Você pode encontrar o repositório original do algoritmo no GitHub [aqui](https://github.com/kamauwashington/python-caverphone2-algorithm/tree/main).

## Como Usar

1. Execute o programa e escolha o idioma desejado.
2. Selecione o nível de dificuldade.
3. Repita a palavra ou frase claramente quando solicitado.
4. O programa gravará sua pronúncia.
5. A pronúncia será transcrita e comparada com a palavra original.
6. Você receberá uma porcentagem de igualdade com base no algoritmo Caverphone 2.0.
7. Continue treinando até se sentir satisfeito.

## Requisitos

Certifique-se de que você tenha instalado as bibliotecas necessárias, como Sounddevice, Wavio e Whisper, para executar o programa.


### Uso do Whisper

O Whisper Small foi utilizado neste projeto, mas é possível escolher diferentes modelos de Whisper (mais pesados ou mais leves) alterando a palavra "small" na linha 109 para a versão desejada. Para mais informações sobre os modelos do Whisper, consulte o [Github do Whisper](https://github.com/openai/whisper).

## Limitações

- Este projeto foi desenvolvido em um curto período de tempo e não passou por extensos testes de qualidade.
- Ruídos externos ou microfones de baixa qualidade sonora podem afetar os resultados da transcrição e da comparação fonética.
- A lista de palavras utilizadas no treinamento foi gerada com a ajuda do modelo ChatGPT 3.5 e pode conter erros ou palavras inadequadas para treinamento de dicção.

## Contribuições

Este é um projeto de código aberto, e contribuições são bem-vindas. Sinta-se à vontade para criar problemas, solicitações de recebimento ou contribuir diretamente para o desenvolvimento.
