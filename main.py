import pygame 
import time 

def make_pixel_img(surface,
                    w, 
                    layout, 
                    pix_size=10,
                    foreground=pygame.Color(255,150,0),
                    background=pygame.Color(0,0,0)):
    if (surface == None):
        surface = pygame.Surface((w*pix_size, w*pix_size))
    pos = [[x, x+pix_size] for x in range(0, w*pix_size, pix_size)]
    with pygame.PixelArray(surface) as pix:
        pix[:] = background
        for i, row in enumerate(layout): 
            rs,re = pos[i] 
            for j, col in enumerate(row):
                cs,ce = pos[j] 
                fill = col == 1 
                if fill:
                    pix[cs:ce,rs:re] = foreground 
    return surface

width, height = 1280, 720 

pygame.init() 
screen = pygame.display.set_mode((width, height)) 
clock = pygame.time.Clock() 

layout1 = [[0,1,0,1,0],[0,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0],[0,0,0,0,0]]
layout2 = [[0,1,0,1,0],[0,1,0,1,0],[0,0,0,0,0],[0,1,1,1,0],[0,0,0,0,0]]
toggle = True 
pix = make_pixel_img(None,5,layout2,pix_size=50,foreground=pygame.Color(255,200,200))

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    screen.fill("black")
    screen.blit(pix, (150,150))
    if (toggle):
        layout = layout1 
    else:
        layout = layout2 
    pix = make_pixel_img(pix,5,layout,pix_size=50,foreground=pygame.Color(255,200,200)) 
    toggle = not toggle 
    time.sleep(0.6)
    pygame.display.flip() 
    clock.tick(60) 


