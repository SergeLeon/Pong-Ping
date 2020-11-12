from random import randint, sample

import pygame

import sound

pygame.init()

# размер окна
size = [1280, 720]
window = pygame.display.set_mode(size)

screen = pygame.Surface(size)

font = pygame.font.Font("AtariClassic-Regular.ttf", 36)


def show_score_time(score1, score2, time):
    text = font.render(f"{str(score1).zfill(2)} |{str(time).zfill(3)}| {str(score2).zfill(2)}", 1, (0, 0, 0))
    text_pos = (442, 20)

    screen.blit(text, text_pos)


class Rocket:
    def __init__(self, x_cord, y_cord, weight, height):
        self.x: int = x_cord
        self.y: int = y_cord
        self.size = [weight, height]
        self.surf = pygame.Surface(self.size)
        self.surf.fill([0, 0, 0])
        self.speed = 3
        self.score = 0

    def get_cords(self):
        return [self.x, self.y]

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def render(self):
        screen.blit(self.surf, (self.x, self.y))


class Player(Rocket):
    def move_mouse(self):
        """Движение к курсору"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.y + 12 >= mouse_y - 80 <= self.y - 12:
            self.y -= self.speed
        elif self.y + 12 <= mouse_y - 80 >= self.y - 12:
            self.y += self.speed

        if self.y <= 0:
            self.y += self.speed
        if self.y >= 560:
            self.y -= self.speed

    def move_keyboard(self, k_up: str = "w", k_down: str = "s"):
        """Движение по кнопкам
        Принимает 2 аргумента, кнопка для движения вверхи и кнопка для движения вниз"""
        pushed_keys = pygame.key.get_pressed()
        k_up = eval("pygame.K_" + k_up)
        k_down = eval("pygame.K_" + k_down)
        if pushed_keys[k_up]:
            self.y -= self.speed
        elif pushed_keys[k_down]:
            self.y += self.speed

        if self.y <= 0:
            self.y += self.speed
        if self.y >= 560:
            self.y -= self.speed

    def move(self, ball1, k_up, k_down):
        self.move_keyboard(k_up, k_down)


class AI(Rocket):
    def __init__(self, x_cord, y_cord, weight, height):
        super().__init__(x_cord, y_cord, weight, height)

        self.speed -= 1

    def move(self, ball1, k_up, k_down):
        ball_cords = ball1.get_cords()

        # движение за мячом
        if self.y + 20 <= ball_cords[1] - (self.size[1] / 2) >= self.y - 20 and abs(ball_cords[0] - self.x) < 620:
            self.y += self.speed
        elif self.y + 20 >= ball_cords[1] - (self.size[1] / 2) <= self.y - 20 and abs(ball_cords[0] - self.x) < 620:
            self.y -= self.speed

        # возвращение на исходную позицию
        elif self.y > 280:
            self.y -= self.speed
        elif self.y < 280:
            self.y += self.speed

        if self.y <= 0:
            self.y += self.speed
        if self.y >= 560:
            self.y -= self.speed


class Ball:
    def __init__(self, x_cord, y_cord, ball_size):
        self.x: float = float(x_cord)
        self.y: float = float(y_cord)
        self.size = ball_size
        self.color = [0, 0, 0]
        self.vector = pygame.Vector2()
        self.vector.xy = [-5, 5][randint(0,1)], 0
        self.vector.rotate_ip(randint(-30, 30))

    def get_cords(self):
        return [self.x, self.y]

    def render(self):
        """Отрисовка мяча"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def move(self, rocket1, rocket2):
        """Движение мяча"""
        rocket1_cords = rocket1.get_cords()
        rocket2_cords = rocket2.get_cords()

        # оражение по x
        #   от 1 рокетки
        if (rocket1_cords[0] + 20 + self.size) >= self.x > (rocket1_cords[0] + 10) \
                and (rocket1_cords[1] < (self.y + self.size) and (self.y - self.size) < (rocket1_cords[1] + 160)):
            sound.play_bounce_sound()
            self.x = (rocket1_cords[0] + 20 + self.size)
            self.vector[0] = -self.vector[0]
            self.vector.rotate_ip(randint(-30, 30))

        #   от 2 рокетки
        if (rocket2_cords[0] - self.size) <= self.x < (rocket2_cords[0] + 10) \
                and (rocket2_cords[1] < (self.y + self.size) and (self.y - self.size) < (rocket2_cords[1] + 160)):
            sound.play_bounce_sound()
            self.x = rocket2_cords[0] - self.size
            self.vector[0] = -self.vector[0]
            self.vector.rotate_ip(randint(-30, 30))

        # оражение по y
        #   от стен
        #       от нижней
        if self.y >= 720 - self.size:
            sound.play_bounce_sound()
            self.y = 720 - self.size
            self.vector[1] = -self.vector[1]
            self.vector.rotate_ip(randint(-15, 15))

        #       от верхней
        elif self.y <= self.size:
            sound.play_bounce_sound()
            self.y = self.size
            self.vector[1] = -self.vector[1]
            self.vector.rotate_ip(randint(-15, 15))

        self.x += self.vector[0]
        self.y += self.vector[1]

        self.check_location_in_area(rocket1, rocket2)

    def check_location_in_area(self, rocket1, rocket2):
        """Проверка на нахождение в поле игры"""
        if self.x > 1280 + self.size:
            sound.play_death_sound()
            self.x, self.y = 640, 360
            self.vector.xy = +5, 0
            self.vector.rotate_ip(randint(-30, 30))
            rocket1.set_score(rocket1.get_score() + 1)

        if self.x < 0 - self.size:
            sound.play_death_sound()
            self.x, self.y = 640, 360
            self.vector.xy = -5, 0
            self.vector.rotate_ip(randint(-30, 30))
            rocket2.set_score(rocket2.get_score() + 1)


def start_game(player_count):
    pygame.display.set_caption("Ping-Pong game")

    if player_count == 1:
        rocket1 = Player(60, 280, 20, 160)
        rocket2 = AI(1200, 280, 20, 160)
    elif player_count == 2:
        rocket1 = Player(60, 280, 20, 160)
        rocket2 = Player(1200, 280, 20, 160)
    elif player_count == 0:
        rocket1 = AI(60, 280, 20, 160)
        rocket2 = AI(1200, 280, 20, 160)

    ball1 = Ball(640, 360, 20)

    center = pygame.Surface((2, 720))
    center.fill([120, 190, 120])

    #  Таймер не более 999
    time = 120
    time_temp = 0

    rockets_for_render = {rocket1: ['w', 's'], rocket2: ['UP', 'DOWN']}
    balls_for_render = [ball1]
    balls_count = 1

    running = True
    while running:
        # обработка событий
        for e in pygame.event.get():
            if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False

        screen.fill([144, 238, 144])

        if time > 0:

            screen.blit(center, (639, 0))

            time_temp += 1
            if time_temp >= 150:
                time_temp = 0
                time -= 1

            for rocket in rockets_for_render.keys():
                rocket.move(ball1, *rockets_for_render[rocket])
                rocket.render()

            for ball in balls_for_render:
                ball.move(*rockets_for_render)
                ball.render()

            show_score_time(rocket1.score, rocket2.score, time)
        else:

            if rocket1.score > rocket2.score:
                text = font.render("Player1 WIN!", 1, (0, 0, 0))
                screen.blit(text, (445, 300))

            elif rocket1.score < rocket2.score:
                text = font.render("Player2 WIN!", 1, (0, 0, 0))
                screen.blit(text, (445, 300))

            else:
                text = font.render("Draw", 1, (0, 0, 0))
                screen.blit(text, (568, 300))

        # отображение окна
        window.blit(screen, [0, 0])
        pygame.display.flip()
        pygame.time.delay(5)

    pygame.display.set_caption("Pong-Ping menu")


if __name__ == "__main__":
    start_game(0)
