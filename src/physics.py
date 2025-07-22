
import math

# Constantes (ajustáveis conforme a física do jogo)
GRAVITY = 9.81  # Gravidade (m/s^2)
# DRAG_COEFFICIENT = 0.01 # Coeficiente de arrasto (simplificado)

def calculate_trajectory(initial_velocity, angle_degrees, wind_speed, wind_direction, time_steps=100):
    """
    Calcula a trajetória de um projétil.

    :param initial_velocity: Velocidade inicial do projétil (m/s).
    :param angle_degrees: Ângulo de lançamento em graus.
    :param wind_speed: Velocidade do vento (m/s).
    :param wind_direction: Direção do vento ("left" ou "right").
    :param time_steps: Número de passos de tempo para a simulação.
    :return: Lista de tuplas (x, y) representando a trajetória.
    """
    angle_radians = math.radians(angle_degrees)
    trajectory = []
    dt = 0.1 # Pequeno incremento de tempo

    # Componentes da velocidade inicial
    vx = initial_velocity * math.cos(angle_radians)
    vy = initial_velocity * math.sin(angle_radians)

    x, y = 0, 0

    for i in range(time_steps):
        # Efeito do vento na velocidade horizontal
        if wind_direction == "right":
            vx_with_wind = vx + wind_speed
        elif wind_direction == "left":
            vx_with_wind = vx - wind_speed
        else:
            vx_with_wind = vx

        # Atualiza posição
        x += vx_with_wind * dt
        y += vy * dt - 0.5 * GRAVITY * dt**2

        # Atualiza velocidade vertical (gravidade)
        vy -= GRAVITY * dt

        if y < 0: # Não permite que o projétil vá abaixo do solo
            y = 0
            break

        trajectory.append((x, y))

    return trajectory

def find_force_for_target(target_x, target_y, angle_degrees, wind_speed, wind_direction, max_force=100, tolerance=1.0):
    """
    Encontra a força (velocidade inicial) necessária para atingir um alvo.
    Isso é uma simplificação e pode precisar de um algoritmo de busca mais robusto (e.g., busca binária).

    :param target_x: Coordenada X do alvo.
    :param target_y: Coordenada Y do alvo.
    :param angle_degrees: Ângulo de lançamento em graus.
    :param wind_speed: Velocidade do vento.
    :param wind_direction: Direção do vento.
    :param max_force: Força máxima a ser testada.
    :param tolerance: Tolerância para acertar o alvo.
    :return: Força necessária ou None se não encontrar.
    """
    best_force = None
    min_distance = float("inf")

    # Busca linear simples (pode ser otimizada com busca binária)
    for force in range(1, max_force + 1):
        trajectory = calculate_trajectory(force, angle_degrees, wind_speed, wind_direction)
        if not trajectory: continue

        # Pega o último ponto da trajetória (onde atinge o solo ou o ponto mais próximo do alvo)
        last_x, last_y = trajectory[-1]

        distance = math.sqrt((last_x - target_x)**2 + (last_y - target_y)**2)

        if distance < min_distance:
            min_distance = distance
            best_force = force

        if distance <= tolerance:
            return force

    # Se não encontrou dentro da tolerância, retorna a melhor força encontrada
    if min_distance <= tolerance * 2: # Retorna se estiver razoavelmente perto
        return best_force
    return None


# Exemplo de uso (para testes internos)
if __name__ == '__main__':
    # Teste de trajetória
    print("\n--- Teste de Trajetória ---")
    traj = calculate_trajectory(initial_velocity=50, angle_degrees=45, wind_speed=0, wind_direction="none")
    print(f"Trajetória (sem vento): {traj[:5]}...{traj[-5:]}")

    traj_wind = calculate_trajectory(initial_velocity=50, angle_degrees=45, wind_speed=10, wind_direction="right")
    print(f"Trajetória (vento à direita): {traj_wind[:5]}...{traj_wind[-5:]}")

    # Teste de encontrar força
    print("\n--- Teste de Encontrar Força ---")
    target_x_val = 200
    target_y_val = 0
    angle_val = 45
    wind_speed_val = 5
    wind_direction_val = "right"

    force_needed = find_force_for_target(target_x_val, target_y_val, angle_val, wind_speed_val, wind_direction_val)
    if force_needed:
        print(f"Força necessária para atingir ({target_x_val}, {target_y_val}) com ângulo {angle_val} e vento {wind_speed_val} {wind_direction_val}: {force_needed}")
    else:
        print(f"Não foi possível encontrar uma força para atingir ({target_x_val}, {target_y_val}) com as condições dadas.")

    # Teste com alvo mais distante
    target_x_val = 500
    force_needed = find_force_for_target(target_x_val, target_y_val, angle_val, wind_speed_val, wind_direction_val)
    if force_needed:
        print(f"Força necessária para atingir ({target_x_val}, {target_y_val}) com ângulo {angle_val} e vento {wind_speed_val} {wind_direction_val}: {force_needed}")
    else:
        print(f"Não foi possível encontrar uma força para atingir ({target_x_val}, {target_y_val}) com as condições dadas.")




