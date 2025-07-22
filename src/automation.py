import pyautogui
import time
import math

# Configurações de segurança
pyautogui.FAILSAFE = True  # Move o mouse para o canto superior esquerdo para parar
pyautogui.PAUSE = 0.1  # Pausa entre comandos

class MouseAutomation:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        
    def move_to_position(self, x, y, duration=0.5):
        """
        Move o mouse para uma posição específica.
        
        :param x: Coordenada X.
        :param y: Coordenada Y.
        :param duration: Duração do movimento em segundos.
        """
        pyautogui.moveTo(x, y, duration=duration)
    
    def click_at_position(self, x, y, button='left'):
        """
        Clica em uma posição específica.
        
        :param x: Coordenada X.
        :param y: Coordenada Y.
        :param button: Botão do mouse ('left', 'right', 'middle').
        """
        pyautogui.click(x, y, button=button)
    
    def drag_to_position(self, start_x, start_y, end_x, end_y, duration=1.0):
        """
        Arrasta o mouse de uma posição para outra.
        
        :param start_x: Coordenada X inicial.
        :param start_y: Coordenada Y inicial.
        :param end_x: Coordenada X final.
        :param end_y: Coordenada Y final.
        :param duration: Duração do arrasto em segundos.
        """
        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(end_x, end_y, duration=duration, button='left')
    
    def adjust_angle(self, current_angle, target_angle, angle_control_region):
        """
        Ajusta o ângulo do carro no jogo.
        
        :param current_angle: Ângulo atual do carro.
        :param target_angle: Ângulo desejado.
        :param angle_control_region: Região onde o controle de ângulo está localizado.
        """
        angle_diff = target_angle - current_angle
        
        # Calcula a posição do controle de ângulo
        control_x = angle_control_region["left"] + angle_control_region["width"] // 2
        control_y = angle_control_region["top"] + angle_control_region["height"] // 2
        
        # Simula o ajuste do ângulo (isso pode variar dependendo da interface do jogo)
        # Exemplo: arrastar horizontalmente para ajustar o ângulo
        if abs(angle_diff) > 1:  # Tolerância de 1 grau
            drag_distance = angle_diff * 2  # Fator de conversão (ajustar conforme necessário)
            self.drag_to_position(control_x, control_y, control_x + drag_distance, control_y, duration=0.5)
    
    def adjust_force(self, target_force, force_bar_region):
        """
        Ajusta a força do tiro.
        
        :param target_force: Força desejada (0-100).
        :param force_bar_region: Região onde a barra de força está localizada.
        """
        # Calcula a posição na barra de força
        bar_start_x = force_bar_region["left"]
        bar_end_x = force_bar_region["left"] + force_bar_region["width"]
        bar_y = force_bar_region["top"] + force_bar_region["height"] // 2
        
        # Calcula a posição X baseada na força desejada
        force_ratio = target_force / 100.0
        target_x = bar_start_x + (bar_end_x - bar_start_x) * force_ratio
        
        # Clica na posição da força desejada
        self.click_at_position(target_x, bar_y)
    
    def fire_shot(self, fire_button_position):
        """
        Dispara o tiro.
        
        :param fire_button_position: Posição do botão de disparo.
        """
        self.click_at_position(fire_button_position["x"], fire_button_position["y"])
    
    def perform_auto_aim(self, current_angle, target_angle, target_force, 
                        angle_control_region, force_bar_region, fire_button_position):
        """
        Executa o processo completo de mira automática.
        
        :param current_angle: Ângulo atual do carro.
        :param target_angle: Ângulo calculado para atingir o alvo.
        :param target_force: Força calculada para atingir o alvo.
        :param angle_control_region: Região do controle de ângulo.
        :param force_bar_region: Região da barra de força.
        :param fire_button_position: Posição do botão de disparo.
        """
        print(f"Ajustando ângulo de {current_angle}° para {target_angle}°")
        self.adjust_angle(current_angle, target_angle, angle_control_region)
        
        time.sleep(0.5)  # Pequena pausa
        
        print(f"Ajustando força para {target_force}")
        self.adjust_force(target_force, force_bar_region)
        
        time.sleep(0.5)  # Pequena pausa
        
        print("Disparando!")
        self.fire_shot(fire_button_position)

class GameControlRegions:
    """
    Classe para armazenar as regiões de controle do jogo.
    Estes valores precisam ser ajustados conforme a interface do jogo.
    """
    def __init__(self):
        # Região do controle de ângulo (exemplo)
        self.angle_control = {
            "left": 300,
            "top": 650,
            "width": 200,
            "height": 30
        }
        
        # Região da barra de força (exemplo)
        self.force_bar = {
            "left": 550,
            "top": 650,
            "width": 200,
            "height": 20
        }
        
        # Posição do botão de disparo (exemplo)
        self.fire_button = {
            "x": 800,
            "y": 650
        }

# Exemplo de uso
if __name__ == '__main__':
    automation = MouseAutomation()
    regions = GameControlRegions()
    
    # Exemplo de uso do sistema de automação
    print("Iniciando teste de automação em 3 segundos...")
    time.sleep(3)
    
    # Simula um cenário de mira automática
    current_angle = 45
    target_angle = 60
    target_force = 75
    
    automation.perform_auto_aim(
        current_angle=current_angle,
        target_angle=target_angle,
        target_force=target_force,
        angle_control_region=regions.angle_control,
        force_bar_region=regions.force_bar,
        fire_button_position=regions.fire_button
    )
    
    print("Teste de automação concluído!")

