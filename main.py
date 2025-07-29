import pygame
import random
import time
from pokemon_class import Pokemon, display_message
from utils import create_button

pygame.init()

game_width = 500
game_height = 500
screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Pokemon Battle")

WHITE = (255,255,255)
BLACK = (0,0,0)

level = 30
bulbasaur = Pokemon('Bulbasaur', level, 25, 150)
charmander = Pokemon('Charmander', level, 175, 150)
squirtle = Pokemon('Squirtle', level, 325, 150)
pokemons = [bulbasaur, charmander, squirtle]

player_pokemon = None
rival_pokemon = None
game_status = 'select pokemon'

def display_message(message):
    pygame.draw.rect(screen, WHITE, (10, 350, 480, 140))
    pygame.draw.rect(screen, BLACK, (10, 350, 480, 140), 3)
    font = pygame.font.Font(pygame.font.get_default_font(), 20)
    text = font.render(message, True, BLACK)
    screen.blit(text, (30, 410))
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y and game_status == 'gameover':
                # Перезапуск гри
                bulbasaur = Pokemon('Bulbasaur', level, 25, 150)
                charmander = Pokemon('Charmander', level, 175, 150)
                squirtle = Pokemon('Squirtle', level, 325, 150)
                pokemons = [bulbasaur, charmander, squirtle]
                player_pokemon = None
                rival_pokemon = None
                game_status = 'select pokemon'
            elif event.key == pygame.K_n and game_status == 'gameover':
                pygame.quit()
                exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if game_status == 'select pokemon':
                for i, pkmn in enumerate(pokemons):
                    if pkmn.get_rect().collidepoint(mouse_pos):
                        player_pokemon = pkmn
                        rival_pokemon = pokemons[(i + 1) % len(pokemons)]
                        rival_pokemon.level = int(rival_pokemon.level * 0.75)

                        player_pokemon.hp_x, player_pokemon.hp_y = 275, 250
                        rival_pokemon.hp_x, rival_pokemon.hp_y = 50, 50

                        game_status = 'prebattle'

            elif game_status == 'player turn':
                if fight_button.collidepoint(mouse_pos):
                    game_status = 'player move'
                elif potion_button.collidepoint(mouse_pos):
                    if player_pokemon.num_potions == 0:
                        display_message("No more potions left")
                        time.sleep(2)
                        game_status = 'player move'
                    else:
                        player_pokemon.use_potion()
                        display_message(f"{player_pokemon.name} used potion")
                        time.sleep(2)
                        game_status = 'rival turn'

            elif game_status == 'player move':
                for i, btn in enumerate(move_buttons):
                    if btn.collidepoint(mouse_pos):
                        move = player_pokemon.moves[i]
                        player_pokemon.perform_attack(rival_pokemon, move)
                        if rival_pokemon.current_hp == 0:
                            game_status = 'fainted'
                        else:
                            game_status = 'rival turn'

    # Екран вибору покемона
    if game_status == 'select pokemon':
        screen.fill(WHITE)
        for pkmn in pokemons:
            pkmn.draw(screen)
        mouse_pos = pygame.mouse.get_pos()
        for pkmn in pokemons:
            if pkmn.get_rect().collidepoint(mouse_pos):
                pygame.draw.rect(screen, BLACK, pkmn.get_rect(), 2)
        pygame.display.update()

    # Підготовка перед боєм
    if game_status == 'prebattle':
        screen.fill(WHITE)
        player_pokemon.draw(screen)
        pygame.display.update()

        player_pokemon.set_moves()
        rival_pokemon.set_moves()

        player_pokemon.x, player_pokemon.y = -50, 100
        rival_pokemon.x, rival_pokemon.y = 250, -50

        player_pokemon.size = 300
        rival_pokemon.size = 300

        player_pokemon.set_sprite('back_default')
        rival_pokemon.set_sprite('front_default')

        game_status = 'start battle'

    # Початок бою з анімацією появи покемонів
    if game_status == 'start battle':
        alpha = 0
        while alpha < 255:
            screen.fill(WHITE)
            rival_pokemon.draw(screen, alpha)
            display_message(f'Rival sent out {rival_pokemon.name}!')
            alpha += 0.4
            pygame.display.update()

        time.sleep(1)

        alpha = 0
        while alpha < 255:
            screen.fill(WHITE)
            rival_pokemon.draw(screen)
            player_pokemon.draw(screen, alpha)
            display_message(f'Go {player_pokemon.name}!')
            alpha += 0.4
            pygame.display.update()

        player_pokemon.draw_hp(screen)
        rival_pokemon.draw_hp(screen)

        if rival_pokemon.speed > player_pokemon.speed:
            game_status = 'rival turn'
        else:
            game_status = 'player turn'

        pygame.display.update()
        time.sleep(1)

    # Хід гравця
    if game_status == 'player turn':
        screen.fill(WHITE)
        player_pokemon.draw(screen)
        rival_pokemon.draw(screen)
        player_pokemon.draw_hp(screen)
        rival_pokemon.draw_hp(screen)

        fight_button = create_button(screen, 240, 140, 10, 350, 130, 412, 'Fight')
        potion_button = create_button(screen, 240, 140, 250, 350, 370, 412, f'Use Potion ({player_pokemon.num_potions})')

        pygame.draw.rect(screen, BLACK, (10, 350, 480, 140), 3)
        pygame.display.update()

    # Вибір атаки
    if game_status == 'player move':
        screen.fill(WHITE)
        player_pokemon.draw(screen)
        rival_pokemon.draw(screen)
        player_pokemon.draw_hp(screen)
        rival_pokemon.draw_hp(screen)

        move_buttons = []
        for i, move in enumerate(player_pokemon.moves):
            left = 10 + (i % 2) * 240
            top = 350 + (i // 2) * 70
            btn = create_button(screen, 240, 70, left, top, left + 120, top + 35, move.name.capitalize())
            move_buttons.append(btn)

        pygame.draw.rect(screen, BLACK, (10, 350, 480, 140), 3)
        pygame.display.update()

    # Хід суперника
    if game_status == 'rival turn':
        screen.fill(WHITE)
        player_pokemon.draw(screen)
        rival_pokemon.draw(screen)
        player_pokemon.draw_hp(screen)
        rival_pokemon.draw_hp(screen)

        display_message('')
        time.sleep(2)

        move = random.choice(rival_pokemon.moves)
        rival_pokemon.perform_attack(player_pokemon, move)

        if player_pokemon.current_hp == 0:
            game_status = 'fainted'
        else:
            game_status = 'player turn'

        pygame.display
