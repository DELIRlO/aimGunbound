import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
import math

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.trajectory_points = []
        self.force_info = ""
        self.wind_info = ""
        self.target_position = None
        self.player_position = None
        self.init_ui()

    def init_ui(self):
        # Configurações da janela
        self.setWindowTitle("Gunbound Aimbot Overlay")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)  # Tamanho da tela (ajustar conforme necessário)

        # Timer para atualização
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Atualiza a cada 50ms

    def set_trajectory(self, points):
        """Define os pontos da trajetória a serem desenhados."""
        self.trajectory_points = points

    def set_force_info(self, force):
        """Define a informação de força a ser exibida."""
        self.force_info = f"Força: {force}"

    def set_wind_info(self, wind_speed, wind_direction):
        """Define a informação de vento a ser exibida."""
        self.wind_info = f"Vento: {wind_speed} {wind_direction}"

    def set_target_position(self, x, y):
        """Define a posição do alvo."""
        self.target_position = (x, y)

    def set_player_position(self, x, y):
        """Define a posição do jogador."""
        self.player_position = (x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Desenha a trajetória
        if len(self.trajectory_points) > 1:
            pen = QPen(QColor(255, 0, 0, 180), 3)  # Linha vermelha semi-transparente
            painter.setPen(pen)

            for i in range(len(self.trajectory_points) - 1):
                x1, y1 = self.trajectory_points[i]
                x2, y2 = self.trajectory_points[i + 1]
                # Converte coordenadas do mundo para coordenadas da tela
                # (isso pode precisar de ajustes dependendo do sistema de coordenadas do jogo)
                screen_x1, screen_y1 = self.world_to_screen(x1, y1)
                screen_x2, screen_y2 = self.world_to_screen(x2, y2)
                painter.drawLine(screen_x1, screen_y1, screen_x2, screen_y2)

        # Desenha o alvo
        if self.target_position:
            pen = QPen(QColor(0, 255, 0, 200), 2)  # Verde
            painter.setPen(pen)
            target_x, target_y = self.world_to_screen(*self.target_position)
            painter.drawEllipse(target_x - 10, target_y - 10, 20, 20)
            painter.drawLine(target_x - 15, target_y, target_x + 15, target_y)
            painter.drawLine(target_x, target_y - 15, target_x, target_y + 15)

        # Desenha o jogador
        if self.player_position:
            pen = QPen(QColor(0, 0, 255, 200), 2)  # Azul
            painter.setPen(pen)
            player_x, player_y = self.world_to_screen(*self.player_position)
            painter.drawEllipse(player_x - 8, player_y - 8, 16, 16)

        # Desenha informações de texto
        painter.setPen(QPen(QColor(255, 255, 255, 255)))
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)

        # Informação de força
        if self.force_info:
            painter.drawText(20, 30, self.force_info)

        # Informação de vento
        if self.wind_info:
            painter.drawText(20, 60, self.wind_info)

    def world_to_screen(self, world_x, world_y):
        """
        Converte coordenadas do mundo (física) para coordenadas da tela.
        Esta é uma função placeholder que precisa ser ajustada conforme o sistema de coordenadas do jogo.
        """
        # Exemplo de conversão simples (ajustar conforme necessário)
        screen_x = int(world_x * 2)  # Escala X
        screen_y = int(600 - world_y * 2)  # Escala Y e inverte (tela tem Y crescendo para baixo)
        return screen_x, screen_y

    def closeEvent(self, event):
        """Fecha a aplicação quando a janela é fechada."""
        QApplication.quit()

class OverlayManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.overlay = OverlayWindow()

    def show(self):
        """Mostra o overlay."""
        self.overlay.show()

    def hide(self):
        """Esconde o overlay."""
        self.overlay.hide()

    def update_trajectory(self, trajectory_points):
        """Atualiza a trajetória no overlay."""
        self.overlay.set_trajectory(trajectory_points)

    def update_force(self, force):
        """Atualiza a informação de força no overlay."""
        self.overlay.set_force_info(force)

    def update_wind(self, wind_speed, wind_direction):
        """Atualiza a informação de vento no overlay."""
        self.overlay.set_wind_info(wind_speed, wind_direction)

    def update_target(self, x, y):
        """Atualiza a posição do alvo no overlay."""
        self.overlay.set_target_position(x, y)

    def update_player(self, x, y):
        """Atualiza a posição do jogador no overlay."""
        self.overlay.set_player_position(x, y)

    def run(self):
        """Executa o loop principal da aplicação."""
        return self.app.exec_()

# Exemplo de uso
if __name__ == '__main__':
    overlay_manager = OverlayManager()
    
    # Exemplo de dados de teste
    test_trajectory = [(i * 10, 100 - i * 2) for i in range(20)]
    overlay_manager.update_trajectory(test_trajectory)
    overlay_manager.update_force(75)
    overlay_manager.update_wind(5, "right")
    overlay_manager.update_target(400, 50)
    overlay_manager.update_player(50, 100)
    
    overlay_manager.show()
    overlay_manager.run()


