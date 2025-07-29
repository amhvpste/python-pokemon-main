import pygame

pygame.font.init()
font = pygame.font.SysFont("arial", 20)

def draw_text(surface, text, pos, color=(0,0,0)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def create_button(surface, width, height, left, top, text_cx, text_cy, label):
    mouse_pos = pygame.mouse.get_pos()
    button = pygame.Rect(left, top, width, height)

    if button.collidepoint(mouse_pos):
        pygame.draw.rect(surface, (218, 165, 32), button)  # gold highlight
    else:
        pygame.draw.rect(surface, (255,255,255), button)

    pygame.draw.rect(surface, (0,0,0), button, 2)

    text_surface = font.render(label, True, (0,0,0))
    text_rect = text_surface.get_rect(center=(text_cx, text_cy))
    surface.blit(text_surface, text_rect)

    return button
