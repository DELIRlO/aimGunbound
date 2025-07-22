# Gunbound 2025 Aimbot

Um aimbot completo para Gunbound 2025 que captura dados do jogo, calcula trajetórias balísticas e automatiza a mira.

## ⚠️ AVISO IMPORTANTE

Este projeto foi desenvolvido **exclusivamente para fins educacionais** e demonstração de técnicas de visão computacional, física balística e automação. O uso deste software em jogos online pode violar os termos de serviço e resultar em banimento da conta.

**USE POR SUA PRÓPRIA CONTA E RISCO.**

## Funcionalidades

- 🎯 **Captura de dados em tempo real**: Velocidade do vento, ângulo do carro, posição dos inimigos
- 🧮 **Cálculos de física balística**: Trajetória considerando vento e gravidade
- 🎨 **Overlay visual**: Desenha a trajetória calculada na tela
- 🖱️ **Automação de mouse**: Ajusta ângulo e força automaticamente
- ⚡ **Interface em tempo real**: Atualização contínua dos cálculos

## Requisitos do Sistema

- Python 3.8+
- Sistema operacional: Windows/Linux
- Tesseract OCR instalado
- Resolução de tela: 1280x720 ou superior

## Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd gunbound_aimbot
```

2. Instale as dependências:
```bash
pip install -r docs/requirements.txt
```

3. Instale o Tesseract OCR:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Baixe de https://github.com/UB-Mannheim/tesseract/wiki

## Uso

1. Inicie o Gunbound 2025
2. Execute o aimbot:
```bash
cd src
python main.py
```

3. O overlay aparecerá sobre o jogo mostrando:
   - Trajetória calculada (linha vermelha)
   - Posição do alvo (cruz verde)
   - Posição do jogador (círculo azul)
   - Informações de vento e força

## Configuração

Edite o arquivo `src/config.py` para ajustar:
- Regiões de interesse (ROI) para captura
- Coordenadas dos controles do jogo
- Parâmetros de física

### Exemplo de configuração de ROI:
```python
WIND_ROI = {"left": 100, "top": 50, "width": 150, "height": 50}
PLAYER_ANGLE_ROI = {"left": 300, "top": 600, "width": 80, "height": 30}
```

## Arquitetura

```
gunbound_aimbot/
├── src/
│   ├── main.py          # Módulo principal
│   ├── capture.py       # Captura de tela e reconhecimento
│   ├── physics.py       # Cálculos balísticos
│   ├── overlay.py       # Interface gráfica
│   ├── automation.py    # Automação do mouse
│   └── config.py        # Configurações
├── docs/
│   ├── README.md
│   └── requirements.txt
└── assets/
    └── images/          # Imagens de referência
```

## Como Funciona

1. **Captura**: O sistema captura a tela do jogo em tempo real
2. **Reconhecimento**: Usa OCR e processamento de imagem para extrair:
   - Velocidade e direção do vento
   - Ângulo atual do carro
   - Posição dos inimigos
3. **Cálculo**: Aplica equações de física balística considerando:
   - Gravidade
   - Resistência do vento
   - Ângulo de lançamento
4. **Visualização**: Desenha a trajetória calculada no overlay
5. **Automação**: Controla o mouse para ajustar ângulo e força

## Limitações

- Requer calibração manual das regiões de interesse
- Funciona melhor com resolução fixa
- Pode precisar de ajustes para diferentes versões do jogo
- Performance dependente da velocidade do sistema

## Desenvolvimento

### Estrutura dos Módulos

- **capture.py**: Responsável pela captura de tela e reconhecimento de elementos visuais
- **physics.py**: Implementa as equações de movimento projectil
- **overlay.py**: Cria interface gráfica transparente usando PyQt5
- **automation.py**: Controla mouse e teclado usando PyAutoGUI
- **main.py**: Orquestra todos os módulos

### Adicionando Novos Recursos

1. Para novos elementos de reconhecimento, edite `capture.py`
2. Para ajustes na física, modifique `physics.py`
3. Para mudanças visuais, altere `overlay.py`

## Troubleshooting

### Problemas Comuns

1. **OCR não funciona**: Verifique se o Tesseract está instalado corretamente
2. **Overlay não aparece**: Verifique permissões de janela sempre no topo
3. **Reconhecimento falha**: Ajuste as ROIs no arquivo de configuração
4. **Mouse não funciona**: Desative o failsafe do PyAutoGUI se necessário

### Debug

Execute com debug habilitado:
```bash
python main.py --debug
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é fornecido "como está" para fins educacionais. O autor não se responsabiliza pelo uso inadequado do software.

## Disclaimer

Este software é uma demonstração técnica de conceitos de programação e não deve ser usado para obter vantagens injustas em jogos online. Sempre respeite os termos de serviço dos jogos que você joga.

