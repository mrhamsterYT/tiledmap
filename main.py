
import pygame
import pytmx
from pytmx.util_pygame import load_pygame

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()

# -----------------------------------------
# Константы под карту 1536×864
TILE_SIZE = 16         # Размер одного тайла
MAP_W = 96             # Количество тайлов по ширине (1536 / 16)
MAP_H = 54             # Количество тайлов по высоте (864 / 16)
WINDOW_WIDTH = 1536
WINDOW_HEIGHT = 864

# Создаём окно 1536×864
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Collision detection with Tiled and pytmx")

# Цвет для блока
red = pygame.Color(153, 0, 0)

# Загружаем карту .tmx
pytmx_map = load_pygame("testy/minebatlemap0.1.tmx")

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Скорость движения (2 пикселя за кадр)
        self.movement_dict = {
            'left':  (-2,  0),
            'right': ( 2,  0),
            'down':  ( 0,  2),
            'up':    ( 0, -2),
            'rest':  ( 0,  0)
        }
        self.movement = 'rest'

    def update(self, event):
        """Обновляем положение (реагируем на события клавиатуры)."""
        if event is not None:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_LEFT:
                    self.movement = 'left'
                elif event.key == pygame.K_RIGHT:
                    self.movement = 'right'
                elif event.key == pygame.K_DOWN:
                    self.movement = 'down'
                elif event.key == pygame.K_UP:
                    self.movement = 'up'
            elif event.type == pygame.KEYUP:
                self.movement = 'rest'

        dx, dy = self.movement_dict[self.movement]
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, display):
        display.blit(self.image, self.rect)


# Создаём блок 16×16
block = Block(red, 16, 16)
block.rect.x = 50
block.rect.y = 50

# Поверхность для «фона» (карты)
background = pygame.Surface((MAP_W * TILE_SIZE, MAP_H * TILE_SIZE))

loop = True
event = None

while loop:
    # Обрабатываем события
    for event in pygame.event.get():
        pass

    # Очищаем фон (по желанию)
    background.fill((0, 0, 0))

    # Рисуем карту из tmx
    layer_index = 0
    for layer in pytmx_map.visible_layers:
        # Если это слой тайлов
        if isinstance(layer, pytmx.TiledTileLayer):
            for x in range(MAP_W):  # 0..95
                for y in range(MAP_H):  # 0..53
                    image = pytmx_map.get_tile_image(x, y, layer_index)
                    if image is not None:
                        # Если изначально тайл 32×32, а хотим 16×16, сжимаем:
                        image_16 = pygame.transform.scale(image, (16, 16))
                        background.blit(image_16, (x * TILE_SIZE, y * TILE_SIZE))

        # Если это слой объектов (Object Layer)
        if isinstance(layer, pytmx.TiledObjectGroup):
            if layer.name == "hit block":
                for obj in layer:
                    rect_obj = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

                    # Если нужно масштабировать объекты (например, если .tmx сделан под 32x32),
                    # то нужно делить/2. Но это зависит от твоего исходного проекта!
                    # rect_obj.x //= 2
                    # rect_obj.y //= 2
                    # rect_obj.width //= 2
                    # rect_obj.height //= 2
            if layer.name == "teleport":
                for obj in layer:
                    rect_obj = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    if rect_obj.colliderect(block.rect):
                        print("telrporting...")
# Проверяем столкновение
                    if rect_obj.colliderect(block.rect):
                        print("YOU HIT THE RED BLOCK!!")
                        # Здесь можешь откатывать движение, если нужно:
                        # block.rect.x = old_x
                        # block.rect.y = old_y

        layer_index += 1

    # Двигаем блок
    block.update(event)

    # Рисуем фон и блок
    game_display.blit(background, (0, 0))
    block.draw(game_display)

    clock.tick(60)
    pygame.display.update()