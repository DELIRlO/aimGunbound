#!/usr/bin/env python3
"""
Gunbound 2025 Aimbot - Módulo Principal
Integra todos os componentes do aimbot para funcionamento completo.
"""

import sys
import time
import threading
from PyQt5.QtWidgets import QApplication

# Importa os módulos do aimbot
from capture import capture_screen, recognize_wind_from_image, recognize_car_angle_from_image, recognize_enemy_position_from_image
from physics import calculate_trajectory, find_force_for_target
from overlay import OverlayManager
from automation import MouseAutomation, GameControlRegions
from config import WIND_ROI, PLAYER_ANGLE_ROI, ENEMY_ANGLE_ROI, GAME_AREA_ROI

class GunboundAimbot:
    def __init__(self):
        self.running = False
        self.overlay_manager = OverlayManager()
        self.mouse_automation = MouseAutomation()
        self.game_regions = GameControlRegions()
        
        # Dados do jogo
        self.wind_speed = 0
        self.wind_direction = "none"
        self.player_angle = 45
        self.player_position = (100, 400)
        self.enemy_position = (800, 400)
        self.calculated_force = 0
        self.calculated_angle = 45
        
    def start(self):
        """Inicia o aimbot."""
        print("Iniciando Gunbound Aimbot...")
        self.running = True
        
        # Inicia o overlay
        self.overlay_manager.show()
        
        # Inicia o loop principal em uma thread separada
        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.daemon = True
        self.main_thread.start()
        
        # Executa o loop da interface gráfica
        return self.overlay_manager.run()
    
    def stop(self):
        """Para o aimbot."""
        print("Parando Gunbound Aimbot...")
        self.running = False
        self.overlay_manager.hide()
    
    def capture_game_data(self):
        """Captura dados do jogo da tela."""
        try:
            # Captura a tela
            screenshot = capture_screen()
            
            # Reconhece o vento
            wind_data = recognize_wind_from_image(screenshot, WIND_ROI)
            if wind_data:
                self.wind_speed, self.wind_direction = wind_data
            
            # Reconhece o ângulo do jogador
            player_angle = recognize_car_angle_from_image(screenshot, PLAYER_ANGLE_ROI)
            if player_angle is not None:
                self.player_angle = player_angle
            
            # Reconhece a posição do inimigo
            enemy_pos = recognize_enemy_position_from_image(screenshot, GAME_AREA_ROI)
            if enemy_pos:
                self.enemy_position = enemy_pos
                
        except Exception as e:
            print(f"Erro ao capturar dados do jogo: {e}")
    
    def calculate_optimal_shot(self):
        """Calcula o tiro ótimo para atingir o inimigo."""
        try:
            # Calcula a distância até o alvo
            target_x = self.enemy_position[0] - self.player_position[0]
            target_y = self.enemy_position[1] - self.player_position[1]
            
            # Encontra a força necessária para o ângulo atual
            force = find_force_for_target(
                target_x, target_y, 
                self.player_angle, 
                self.wind_speed, 
                self.wind_direction
            )
            
            if force:
                self.calculated_force = force
                self.calculated_angle = self.player_angle
                
                # Calcula a trajetória para visualização
                trajectory = calculate_trajectory(
                    force, self.player_angle, 
                    self.wind_speed, self.wind_direction
                )
                
                # Converte trajetória para coordenadas absolutas da tela
                absolute_trajectory = []
                for x, y in trajectory:
                    abs_x = self.player_position[0] + x
                    abs_y = self.player_position[1] - y  # Inverte Y
                    absolute_trajectory.append((abs_x, abs_y))
                
                return absolute_trajectory
            
        except Exception as e:
            print(f"Erro ao calcular tiro ótimo: {e}")
        
        return []
    
    def update_overlay(self, trajectory):
        """Atualiza o overlay com as informações calculadas."""
        try:
            self.overlay_manager.update_trajectory(trajectory)
            self.overlay_manager.update_force(self.calculated_force)
            self.overlay_manager.update_wind(self.wind_speed, self.wind_direction)
            self.overlay_manager.update_target(*self.enemy_position)
            self.overlay_manager.update_player(*self.player_position)
        except Exception as e:
            print(f"Erro ao atualizar overlay: {e}")
    
    def execute_auto_shot(self):
        """Executa o tiro automático (opcional)."""
        try:
            if self.calculated_force > 0:
                self.mouse_automation.perform_auto_aim(
                    current_angle=self.player_angle,
                    target_angle=self.calculated_angle,
                    target_force=self.calculated_force,
                    angle_control_region=self.game_regions.angle_control,
                    force_bar_region=self.game_regions.force_bar,
                    fire_button_position=self.game_regions.fire_button
                )
        except Exception as e:
            print(f"Erro ao executar tiro automático: {e}")
    
    def main_loop(self):
        """Loop principal do aimbot."""
        print("Loop principal iniciado...")
        
        while self.running:
            try:
                # Captura dados do jogo
                self.capture_game_data()
                
                # Calcula o tiro ótimo
                trajectory = self.calculate_optimal_shot()
                
                # Atualiza o overlay
                self.update_overlay(trajectory)
                
                # Exibe informações no console
                print(f"Vento: {self.wind_speed} {self.wind_direction} | "
                      f"Ângulo: {self.player_angle}° | "
                      f"Força: {self.calculated_force} | "
                      f"Alvo: {self.enemy_position}")
                
                # Pausa antes da próxima iteração
                time.sleep(0.1)  # 10 FPS
                
            except Exception as e:
                print(f"Erro no loop principal: {e}")
                time.sleep(1)
    
    def toggle_auto_shot(self):
        """Alterna o modo de tiro automático."""
        # Esta função pode ser chamada por uma tecla de atalho
        self.execute_auto_shot()

def main():
    """Função principal."""
    print("=== Gunbound 2025 Aimbot ===")
    print("Pressione Ctrl+C para sair")
    print("AVISO: Use apenas para fins educacionais!")
    print()
    
    try:
        # Cria e inicia o aimbot
        aimbot = GunboundAimbot()
        return aimbot.start()
        
    except KeyboardInterrupt:
        print("\nEncerrando aimbot...")
        return 0
    except Exception as e:
        print(f"Erro fatal: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

