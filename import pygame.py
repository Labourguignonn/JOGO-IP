import pygame
import button

pygame.init()
############### FABY #############################
#GAME WINDOW
largura = 800
altura = 640
#lower
margem = 100
#side
margem_lado = 300

tela = pygame.display.set_mode((largura + margem_lado, altura + margem))
pygame.display.set_caption('Após a enchente')


#variaveis scrool
esquerda = False
direita = False
scroll = 0 
scroll_speed = 1
#variaveis matriz
rows = 16
colunas_max = 150
tamanho = altura // rows
#variaveis grafico
#QUANTAS IMAGENS TEM ---  tem que mudar sempre que add alguma imagem
tipo = 4
current_tile = 0


#ADD AS IMAGES
background = pygame.image.load('sewer.png').convert_alpha()
background = pygame.transform.scale(background, (largura,altura))

img_lista = []
for x in range(tipo):
    #ADIÇÃO DAS IMAGENS NO INVENTARIO
    img = pygame.image.load(f'img/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (tamanho, tamanho))
    img_lista.append(img)

#DEFINIR CORES 
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (144, 201, 120)

#CRIAR LISTA COM OS ESPAÇOS VAZIOS
#World data
lista = []
for row in range(rows):
    r = [-1]*colunas_max
    lista.append(r)

#CRIAR CHÃO
for tile in range(0, colunas_max):
    lista[rows - 2][tile] = 2 ##número da foto

for tile in range(0, colunas_max):
    lista[rows - 1][tile] = 3 ##número da foto

#FUNÇÃO PARA AS IMAGENS 

def imagens():
    tela.fill(BLACK)
    width = tela.get_width()
    #quantas vezes a imagem repete 
    for x in range(4):
        tela.blit(background,((x*width) - scroll * 0.7,0)) ##0.7 == velocidade que move a tela

#FUNÇÃO MATRIZES
def matrizes():
    #linha vertical 
    for j in range(colunas_max + 1):
        pygame.draw.line(tela, WHITE, (j *tamanho - scroll,0), (j *tamanho - scroll, altura))
    #linha horizontal 
    for j in range(rows + 1):
        pygame.draw.line(tela, WHITE, (0, j *tamanho), (altura, j *tamanho))

#FUNÇÃO PRA DESENHAR AS PLATAFORMAS
def desenhar_mundo():
    #interar entre os valores da matriz
    for y, row in enumerate(lista):
        for x, tile in enumerate(row):
            if tile >= 0:
                tela.blit(img_lista[tile], (x *tamanho - scroll, y *tamanho ))

#CRIAR OS BOTÕES DAS IMAGENS
botao_lista = []
#col
botao1 = 0 
#row
botao2 = 0

for i in range(len(img_lista)):
    ideia_botao = button.Button(altura + (75 *botao1) + 50, 75 * botao2 + 50, img_lista[i], 1)
    botao_lista.append(ideia_botao)
    botao1 += 1
    if botao1 == 3:
        botao2 += 1
        botao1 = 0

rodando = True
while rodando == True:

    imagens()
    matrizes()
    desenhar_mundo()

    #painel/invetário 
    pygame.draw.rect(tela, WHITE, (altura, 0, margem_lado, largura))
    contador_botao = 0
    for contador_botao, i in enumerate(botao_lista): 
       if i.draw(tela):
            current_tile = contador_botao

    #marca que fica sobre as imagens dentro do inventário 
    pygame.draw.rect(tela, GREEN, botao_lista[current_tile].rect, 3)

    if esquerda == True and scroll > 0:
        scroll -= 5
    if direita == True:
        scroll += 5
    
    #FAZER O MOUSE PUXAR A IMAGEM PARA POR NA GRADE
    posicao = pygame.mouse.get_pos()
    x = (posicao[0] + scroll) // tamanho
    y = posicao[1] // tamanho

    #VER SE O CLIQUE ESTÁ SENDO NA ALTURA E LARGURA DO JOGO 
    if posicao[0] < largura and posicao[1] < altura:
        if pygame.mouse.get_pressed()[0] == 1:
            if lista[y][x] != current_tile:
                lista[y][x] = current_tile
        #CLICAR COM O BOTÃO DIREITO E APAGA O QUE FOI FEITO
        if pygame.mouse.get_pressed()[2] == 1:
             lista[y][x] = -1
    
    #MOVER A TELA 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False 
        #pressionar teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                esquerda = True
            if event.key == pygame.K_RIGHT:
                direita = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                esquerda = False
            if event.key == pygame.K_RIGHT:
                direita = False

    pygame.display.update()

pygame.quit()