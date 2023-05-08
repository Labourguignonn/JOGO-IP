from game_variables import *

def imagens(screen):
    screen.fill(WHITE)
    width = screen.get_width()
    #quantas vezes a imagem repete 
    for x in range(4):
        screen.blit(background,((x*width) - bg_scroll*0.7, 0)) ##0.7 == velocidade que move a tela

def reset_level():
    water_group.empty()
    enemy_group.empty()
    cure_potion_group.empty()
    data = []
    for row in range(rows):
        r = [-1]*colunas_max
        data.append(r)

    return data

def menu_inicial(showing_game_history):
    content_table_menu_bg = pygame.image.load('menu_img/fundo_menu.png')
    content_table_menu_bg = pygame.transform.scale(content_table_menu_bg, (largura + 300, altura + 100))
    tela.blit(content_table_menu_bg, (-200,0))
    
    ###Carrega nome do jogo
    font_title = pygame.font.Font('menu_img/Minecraftia-Regular.ttf', 46)
    text = font_title.render('APÓS A ENCHENTE', True, (172,176,85))
    text_rect_title = text.get_rect()
    text_rect_title.center = (largura // 2  + 300, altura // 2 - 160)
    tela.blit(text,text_rect_title)

    #Se tiver mostrando a história
    if showing_game_history == True:
        mensagens = [
            'Durante um período de chuva muito forte em Recife',
            'a UFPE sofreu um perigoso alagamento!',
            'Era tudo o que a legião de ratos escondidos nos',
            'esgotos do CIn precisava para invadir e sequestrar',
            'a tia Edilene a fim de conseguir acesso a todo o CIn',
            'Ajude Lucas a matar o máximo de ratos no subsolo do',
            'Centro de Informática'
        ]
        spacing = -135
        for mensagem in mensagens:
            spacing += 45
            text = font.render(mensagem, True, WHITE)
            text_rect_description = text.get_rect()
            text_rect_description.center = (largura // 2 + 300, altura // 2 + spacing)
            tela.blit(text,text_rect_description)
    else:
        
        mensagens = {
            '0':('Água de Leptospirose é morte instantânea!', 'aguaVenenosa', (1300, 225), (750, 225)),
            '1':('Movimentação e ataque em            + espaço', 'setasTeclado', (1120,275)),
            '2':('Ache a poção e recupere vida!', 'potion', (1210,333), (835, 333)),
            '4':('FIQUE ATENTO À SUA HEALTH BAR E BOA SORTE NO ESGOTO, GUERREIRO!', 'idlePerson')
        }
        
        spacing = -125
        for mensagem in mensagens.values():
            color = WHITE
            if mensagem[1] == 'idlePerson':
                color = (172,176,85)

            spacing += 55
            text = font.render(mensagem[0], True, color)
            text_rect_description = text.get_rect()
            text_rect_description.center = (largura // 2 + 300, altura // 2 + spacing)
            tela.blit(text,text_rect_description)

            try:
                #carrega imagem
                img_menu = pygame.image.load(f'menu_img/{mensagem[1]}.png').convert_alpha()
                img_menu = pygame.transform.scale(img_menu, (50, 50))
                tela.blit(img_menu, mensagem[2])

            
                rotated_img = pygame.transform.flip(img_menu, True, False)
                tela.blit(rotated_img, mensagem[3])
            except:
                pass
                
