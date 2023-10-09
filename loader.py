import pygame 
import random 
class Img:
    def __init__(self, w, h, layout):
        self.w = w; 
        self.h = h; 
        self.layout = layout; 
    
    def __str__(self):
        return "w: " + str(self.w) + " h: " + str(self.h) + " layout: " + str(self.layout) 
    
    def unpack(self):
        return [self.w, self.h, self.layout] 

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

def draw_layout_img(surface, img, rect_size=10, foreground=pygame.Color(255,150, 0), background=pygame.Color(0,0,0)):
    w, h, layout = img.unpack() 
    if surface == None:
        surface = pygame.Surface((w*rect_size, h*rect_size)); 
    pos_x = [[x, x+rect_size] for x in range(0, w*rect_size, rect_size)] 
    pos_y = [[y, y+rect_size] for y in range(0, h*rect_size, rect_size)] 

    with pygame.PixelArray(surface) as pix:
        pix[:] = background 
        for i, row in enumerate(layout):
            re,rs = pos_y[i] 
            for j, col in enumerate(row):
                cs, ce = pos_x[j] 
                fill = col == 1 
                if fill:
                    pix[cs:ce,rs:re] = foreground

    return surface 

def dump_layout(fname, w,h, layout):
    with open(fname, "w") as layout_file:
        layout_file.write(str(w) + "," + str(h) + "\n") 
        for row in layout:
            for i, cell in enumerate(row):
                end_tok = ","
                if (i == len(row)-1):
                    end_tok = ""
                buffer = str(cell) + end_tok 
                layout_file.write(buffer)
            layout_file.write("\n")



def init_img(fname, w, h, token="#", sep=","):
    with open(fname, "w") as img_file:
        img_file.write(str(w) + "," + str(h) + "\n") 
        
        tok = token + sep; 
        row = tok * w;
        row = row[:-1] + "\n"
        
        for i in range(h):
            img_file.write(row) 

def read_img(fname, token="1", sep=","):
    with open(fname, "r") as img_file:
        header = img_file.readline() 
        w, h = header.split(",") 
        w = int(w) 
        h = int(h)
        layout = [] 
        for line in img_file:
            tokens = line.split(",")
            row = [] 
            for i, t in enumerate(tokens):
                sym = 0 
                if (t == token):
                    sym = 1 
                row.append(sym) 
            layout.append(row) 
        
        return Img(w, h, layout) 

def get_rand():
    return random.randrange(0,255) 

def get_random_color():
    return pygame.Color(get_rand(), get_rand(), get_rand()) 

def load_layout_surf(fname):
    img = read_img(fname) 
    return img, draw_layout_img(None, img, rect_size=30, foreground=pygame.Color(255,150, 0), background=pygame.Color(0,0,0))
    
def main_loop(fname):
    width, height = 1280, 720 
    pygame.init() 
    screen = pygame.display.set_mode((width, height)) 
    clock = pygame.time.Clock() 
    img, pix = load_layout_surf(fname) 
    screen.blit(pix, (50,50))
    running = True
    px, py,sz = 50, 50, 30
    s = 3
    cr = pygame.Color(255,255,255)
    pygame.key.set_repeat(10)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.DROPFILE: 
                print("file dropped: ", event.file) 
                img,pix = load_layout_surf(event.file) 
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed();
                dx,dy = 0,0 
                increase_size = False
                if (keys[pygame.K_w]):
                    dy -= s
                if (keys[pygame.K_s]):
                    dy += s 
                if (keys[pygame.K_a]):
                    dx -= s 
                if (keys[pygame.K_d]):
                    dx += s
                if (keys[pygame.K_z] and sz < 30):
                    sz += 1
                if (keys[pygame.K_x] and sz > 10):
                    sz -= 1
                if (keys[pygame.K_c]):
                    cr = get_random_color() 
                increase_size = keys[pygame.K_z] or keys[pygame.K_x] or keys[pygame.K_c]  
                if (increase_size):
                    pix = draw_layout_img(pix, img, rect_size=sz, foreground=cr) 
                px += dx 
                py += dy 
        screen.fill("black")
        screen.blit(pix, (px,py))
        pygame.display.flip() 
        clock.tick(60) 

def init_cells(scrn, width, height, size, color=(255,0,0)):
    w,h = int(width/size), int(height/size)
    layout = [] 
    rect_arr = []
    for i in range(h):
        rect_row = []
        layout_row = [] 
        for j in range(w):
            rect = pygame.Rect(j*size,i*size,size,size); 
            pygame.draw.rect(scrn, color, rect, width=2) 
            rect_row.append(rect)
            layout_row.append(0) 
        rect_arr.append(rect_row)
        layout.append(layout_row)

    return rect_arr,layout 

def is_collide(x,y, rect_arr):
    for i,row in enumerate(rect_arr):
        for j,r in enumerate(row): 
            if (r.collidepoint(x,y)):
                return i,j 
    return -1,-1 

def draw_cells(scrn, width, height, size,layout,rect_arr, fill=(255,0,0)):
    w,h = int(width/size), int(height/size)
    for i in range(h):
        for j in range(w):
            stroke = 2 
            if (layout[i][j] == 1):
                stroke = 0 
            pygame.draw.rect(scrn, fill, rect_arr[i][j], width=stroke) 

            

def draw_tool(width, height, rect_size):
    width, height = width * rect_size, height * rect_size 
    pygame.init() 
    screen = pygame.display.set_mode((width, height)) 
    clock = pygame.time.Clock() 
    rect_arr,layout = init_cells(screen, width, height, rect_size) 
    running = True 
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos() 
                i,j = is_collide(x,y,rect_arr); 
                if (i != -1 and j != -1):
                    t = 0 
                    if (layout[i][j] == 0):
                        t = 1
                    layout[i][j] = t
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed() 
                if (keys[pygame.K_s]):
                    running = False 

        screen.fill("black") 
        draw_cells(screen, width, height, rect_size, layout, rect_arr)
        pygame.display.flip() 
        clock.tick(60) 
    
    return layout

w,h = 15,10 
layout = draw_tool(w,h,50)
dump_layout("sprite3.txt", w, h, layout) 
main_loop("sprite3.txt")
