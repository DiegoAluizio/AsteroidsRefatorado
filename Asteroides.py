# Jônatas Garcia De OLiveira      RA:10396490
# Diego Oliveira Aluizio          RA:10402412


import math
import pygame
import random

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Asteroids")
font = pygame.font.SysFont(None, 36)


# Classe para desenhar o jogador
class Jogador:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.angle = 0
        self.speed = 0

    def draw(self):
        points = [
            (self.x + 15 * math.cos(math.radians(self.angle)), self.y - 15 * math.sin(math.radians(self.angle))),
            (self.x + 15 * math.cos(math.radians(self.angle + 120)),
             self.y - 15 * math.sin(math.radians(self.angle + 120))),
            (self.x + 15 * math.cos(math.radians(self.angle + 240)),
             self.y - 15 * math.sin(math.radians(self.angle + 240)))]
        pygame.draw.polygon(screen, (255, 255, 255), points)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5  # Gira a nave no sentido horário
        if keys[pygame.K_RIGHT]:
            self.angle -= 5  # Gira a nave no sentido anti-horário
        if keys[pygame.K_UP]:
            self.speed = 5  # Acelera a nave para frente
        elif keys[pygame.K_DOWN]:
            self.speed = -3  # Move a nave para trás
        else:
            self.speed = 0  # Parar a nave se nenhuma tecla for pressionada

        # Atualiza a posição da nave com base na velocidade e ângulo
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        # Verifica os limites da tela para criar o efeito de "loop" de borda a borda
        if self.x < 0: self.x = 800
        if self.x > 800: self.x = 0
        if self.y < 0: self.y = 600
        if self.y > 600: self.y = 0


class Asteroides:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.size = random.randint(20, 50)
        self.angle = random.randint(0, 360)
        self.speed = random.random() * 2 + 1

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        if self.x < 0: self.x = 800
        if self.x > 800: self.x = 0
        if self.y < 0: self.y = 600
        if self.y > 600: self.y = 0


class Balas():
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

    def move(self):
        self.x += 10 * math.cos(math.radians(self.angle))
        self.y -= 10 * math.sin(math.radians(self.angle))


# Função de detecção de colisão corrigida
class Colisao:
    def check_bullet_asteroid(balas,asteroides):
        balas_to_remove = set()
        asteroides_to_remove = set()
        for b in balas:
            for a in asteroides:
                distance = math.hypot(b.x - a.x, b.y - a.y)
                if distance < a.size:
                    balas_to_remove.add(b)
                    asteroides_to_remove.add(a)
        return balas_to_remove, asteroides_to_remove

    def check_player_asteroid(jogador, asteroides):
        for a in asteroides:
            distance = math.hypot(jogador.x - a.x, jogador.y - a.y)
            if distance < a.size:
                return True
        return False


# Função principal do jogo
class Jogo():
    def __init__(self):
        self.jogador = Jogador()
        self.asteroide = []
        self.balas = []
        self.pontuacao = 0

    # Ele vai criando mais asteroides conforme for destruindo
    def criar_asteroide(self):
        if (len(self.asteroide)) < 8:
            self.asteroide.append(Asteroides())

    # Função para atirar balas,DEPENDE DO PLAYER POR ISSO ACOMPLAMOS NA FUNÇÃO PRINCIPAL
    def atirar(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.balas.append(Balas(self.jogador.x, self.jogador.y, self.jogador.angle))

    def run(self):
        screen.fill((0, 0, 0))
        running = True
        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            self.jogador.move()
            self.jogador.draw()
            self.atirar()
            self.criar_asteroide()

            # Movimenta e desenha balas e asteroides
            for b in range(0, len(self.balas)):
                self.balas[b].move()
                self.balas[b].draw()
            for a in range(0, len(self.asteroide)):
                self.asteroide[a].move()
                self.asteroide[a].draw()

            #checa colisoes das balas
            balas_to_remove, asteroids_to_remove = Colisao.check_bullet_asteroid(self.balas, self.asteroide)
            self.balas = [b for b in self.balas if b not in balas_to_remove]
            self.asteroide = [a for a in self.asteroide if a not in asteroids_to_remove]

            # Checa Colisoes Jogador
            if (Colisao.check_player_asteroid(self.jogador, self.asteroide)):
                # score_text = font.render(f'GAME OVER: ', True, (255, 255, 255))
                running = False

            #Atualiza Pontuacao
            self.pontuacao += (len(asteroids_to_remove)) * 10

            # Exibe Pontuacao
            score_text = font.render(f'Score: {self.pontuacao}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            pygame.time.delay(30)
        pygame.quit()


jogo = Jogo()
jogo.run()