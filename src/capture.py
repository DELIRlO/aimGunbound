
import mss
import numpy as np
import cv2
import pytesseract

def capture_screen(region=None):
    """
    Captura uma região da tela ou a tela inteira.

    :param region: Um dicionário com as chaves 'top', 'left', 'width', 'height' para a região de captura.
                   Se None, captura a tela inteira.
    :return: Uma imagem em formato de array NumPy (BGR).
    """
    with mss.mss() as sct:
        monitor = region if region else sct.monitors[1]
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def save_screenshot(img, path="screenshot.png"):
    """
    Salva uma imagem em um arquivo.

    :param img: A imagem a ser salva (array NumPy).
    :param path: O caminho do arquivo para salvar a imagem.
    """
    cv2.imwrite(path, img)

def recognize_wind_from_image(image, wind_roi):
    """
    Reconhece a velocidade e direção do vento de uma região da imagem.
    :param image: Imagem da tela do jogo.
    :param wind_roi: Região de Interesse (ROI) onde o vento é exibido.
    :return: Tupla (velocidade_vento, direcao_vento) ou None se não reconhecido.
    """
    x, y, w, h = wind_roi["left"], wind_roi["top"], wind_roi["width"], wind_roi["height"]
    wind_region = image[y:y+h, x:x+w]

    gray_wind = cv2.cvtColor(wind_region, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_wind, 200, 255, cv2.THRESH_BINARY_INV)

    speed = 0
    direction = "none"

    try:
        wind_text = pytesseract.image_to_string(thresh, config='--psm 7').strip()
        # Extrair números da string para a velocidade
        speed_str = ''.join(filter(str.isdigit, wind_text))
        if speed_str:
            speed = int(speed_str)

        # Detecção de seta (simplificada - pode precisar de refinamento)
        # Procura por um padrão de cor ou forma que indique a direção do vento
        # Exemplo: verificar pixels em áreas específicas para cores que representem a seta
        # Isso é altamente dependente do design do jogo.
        # Para um exemplo mais robusto, seria necessário template matching para a seta.
        # Por enquanto, um placeholder baseado em uma suposição de design.
        # Se a seta for vermelha e estiver à direita do número:
        if np.mean(wind_region[:, w-10:w, 2]) > 150 and np.mean(wind_region[:, w-10:w, 1]) < 50 and np.mean(wind_region[:, w-10:w, 0]) < 50: # Verifica se há vermelho forte à direita
            direction = "right"
        elif np.mean(wind_region[:, 0:10, 2]) > 150 and np.mean(wind_region[:, 0:10, 1]) < 50 and np.mean(wind_region[:, 0:10, 0]) < 50: # Verifica se há vermelho forte à esquerda
            direction = "left"

    except Exception as e:
        print(f"OCR or wind direction detection error: {e}")

    return speed, direction

def recognize_car_angle(image, is_player=True):
    """
    Reconhece o ângulo do carro (player ou inimigo) na imagem.
    (Esta é uma função placeholder, a implementação real dependerá da análise das imagens do jogo).
    :param image: Imagem da tela do jogo.
    :param is_player: True se for o carro do jogador, False para o inimigo.
    :return: Ângulo em graus ou None se não reconhecido.
    """
    # Implementação futura: usar detecção de características ou template matching para o carro e seu indicador de ângulo.
    # Por enquanto, retorna valores mock para teste.
    if is_player:
        return 45 # Exemplo: ângulo de 45 graus para o jogador
    else:
        return 30 # Exemplo: ângulo de 30 graus para o inimigo

def recognize_enemy_position(image):
    """
    Reconhece a posição do inimigo na imagem.
    (Esta é uma função placeholder, a implementação real dependerá da análise das imagens do jogo).
    :param image: Imagem da tela do jogo.
    :return: Tupla (x, y) das coordenadas do centro do inimigo ou None se não reconhecido.
    """
    # Implementação futura: usar detecção de objetos (Haar cascades, YOLO, etc.) ou template matching.
    # Por enquanto, retorna valores mock para teste.
    return 800, 400 # Exemplo: inimigo na posição (800, 400)






def recognize_car_angle_from_image(image, car_roi):
    """
    Reconhece o ângulo do carro de uma região da imagem.
    (Esta é uma função placeholder, a implementação real dependerá da análise das imagens do jogo).
    :param image: Imagem da tela do jogo.
    :param car_roi: Região de Interesse (ROI) onde o ângulo do carro é exibido.
    :return: Ângulo em graus ou None se não reconhecido.
    """
    x, y, w, h = car_roi["left"], car_roi["top"], car_roi["width"], car_roi["height"]
    angle_region = image[y:y+h, x:x+w]

    gray_angle = cv2.cvtColor(angle_region, cv2.COLOR_BGR2GRAY)
    _, thresh_angle = cv2.threshold(gray_angle, 150, 255, cv2.THRESH_BINARY_INV)

    angle = None
    try:
        angle_text = pytesseract.image_to_string(thresh_angle, config='--psm 7 outputbase digits').strip()
        if angle_text.isdigit():
            angle = int(angle_text)
    except Exception as e:
        print(f"OCR error for car angle: {e}")

    return angle

def recognize_enemy_position_from_image(image, game_area_roi):
    """
    Reconhece a posição do inimigo na imagem.
    (Esta é uma função placeholder, a implementação real dependerá da análise das imagens do jogo).
    :param image: Imagem da tela do jogo.
    :param game_area_roi: Região de Interesse (ROI) da área de jogo.
    :return: Tupla (x, y) das coordenadas do centro do inimigo ou None se não reconhecido.
    """
    x, y, w, h = game_area_roi["left"], game_area_roi["top"], game_area_roi["width"], game_area_roi["height"]
    game_area = image[y:y+h, x:x+w]

    # Implementação futura: usar template matching com imagens dos carros inimigos
    # ou detecção de objetos treinada.
    # Por enquanto, um placeholder que retorna uma posição fixa.
    # Para um reconhecimento real, você precisaria de templates dos carros inimigos.
    # Exemplo de como seria com template matching (requer templates em assets/images/):
    # enemy_template = cv2.imread("assets/images/enemy_car_template.png", 0)
    # if enemy_template is not None:
    #     res = cv2.matchTemplate(gray_game_area, enemy_template, cv2.TM_CCOEFF_NORMED)
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #     if max_val > 0.8: # Threshold de confiança
    #         enemy_x = max_loc[0] + enemy_template.shape[1] // 2 + x
    #         enemy_y = max_loc[1] + enemy_template.shape[0] // 2 + y
    #         return enemy_x, enemy_y

    return 800, 400 # Exemplo: inimigo na posição (800, 400)



