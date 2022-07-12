import pygame
vec1 = pygame.math.Vector2(10, 5)
vec2 = pygame.math.Vector2(5,10)
vec3 = pygame.math.Vector2(0,0)
vec3.x = vec1.x / vec2.x
print(vec3)