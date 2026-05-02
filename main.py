import pygame
import sys
import os
from models import Jogo, Tribo, Era

# Configurações Básicas
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ethnos - Python Simplificado")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 36)
small_font = pygame.font.SysFont("Verdana", 20)

# Estados do Jogo
MENU = 0
SETUP = 1
GAME = 2
state = MENU

# Dados das Tribos Fixas
TRIBOS_DISPONIVEIS = [
    Tribo("Centauros", "Rápidos na conquista.", "Avanço rápido."),
    Tribo("Halflings", "Muitos números facilmente.", "Aumenta limite do bando."),
    Tribo("Elfos", "Magia antiga de mãos.", "Retém cartas na mão."),
    Tribo("Esqueletos", "A horda morta-viva não para.", "Retorna peças do descarte.")
]

jogo = Jogo()
for i in range(4):
    jogo.criar_jogador(i + 1, f"Jogador {i + 1}")

tribos_selecionadas = {}  # jogador_id -> Tribo

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def menu_loop():
    global state
    screen.fill((20, 20, 30))
    
    title_font = pygame.font.SysFont("Verdana", 72, bold=True)
    draw_text("E T H N O S", title_font, (255, 215, 0), screen, WIDTH // 2 - 200, HEIGHT // 3)
    draw_text("Python Edition", small_font, (200, 200, 200), screen, WIDTH // 2 - 80, HEIGHT // 3 + 80)
    
    # Botão Iniciar
    btn_iniciar = pygame.Rect(WIDTH // 2 - 125, HEIGHT // 2 + 50, 250, 60)
    pygame.draw.rect(screen, (50, 180, 50), btn_iniciar, border_radius=10)
    pygame.draw.rect(screen, WHITE, btn_iniciar, 2, border_radius=10)
    draw_text("Iniciar", font, WHITE, screen, btn_iniciar.x + 65, btn_iniciar.y + 10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_iniciar.collidepoint(event.pos):
                state = SETUP

def setup_loop():
    global state
    screen.fill((30, 30, 45))
    draw_text("Seleção de Raças (4 Jogadores)", font, WHITE, screen, 50, 40)
    
    jogador_atual_idx = len(tribos_selecionadas)
    
    if jogador_atual_idx < 4:
        draw_text(f"Vez do {jogo.jogadores[jogador_atual_idx].nome} escolher:", small_font, (150, 200, 255), screen, 50, 90)
    else:
        draw_text("Todas as raças selecionadas! Clique em INICIAR para jogar.", small_font, GREEN, screen, 50, 90)
        
    mouse_pos = pygame.mouse.get_pos()
    hovered_tribo = None
    
    tribes_rects = []
    start_y = 140
    for i, t in enumerate(TRIBOS_DISPONIVEIS):
        is_selected = t in tribos_selecionadas.values()
        
        rect = pygame.Rect(50, start_y + i * 85, 400, 70)
        
        if rect.collidepoint(mouse_pos) and not is_selected:
            hovered_tribo = t
            color = (80, 150, 255)
        else:
            color = (80, 80, 100) if is_selected else (50, 80, 150)
            
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
        
        status = " (Já Escolhida)" if is_selected else ""
        draw_text(f"{t.nome}{status}", font, WHITE, screen, rect.x + 20, rect.y + 15)
        tribes_rects.append((rect, t, is_selected))

    # Painel de Descrição Lateral
    info_rect = pygame.Rect(500, 140, 700, 325)
    pygame.draw.rect(screen, (20, 20, 30), info_rect, border_radius=15)
    pygame.draw.rect(screen, (100, 100, 150), info_rect, 3, border_radius=15)
    
    if hovered_tribo:
        draw_text(f"{hovered_tribo.nome}", font, GREEN, screen, 530, 160)
        draw_text("Descrição:", small_font, (200, 200, 200), screen, 530, 220)
        draw_text(f"{hovered_tribo.descricao}", small_font, WHITE, screen, 550, 250)
        
        draw_text("Poder Racial:", small_font, (200, 200, 200), screen, 530, 310)
        
        # Word wrap simples para o poder
        words = hovered_tribo._poder.split(" ")
        lines = []
        current_line = ""
        for w in words:
            if len(current_line + w) < 45:
                current_line += w + " "
            else:
                lines.append(current_line)
                current_line = w + " "
        lines.append(current_line)
        
        py = 340
        for l in lines:
            draw_text(l, small_font, (255, 215, 0), screen, 550, py)
            py += 30
    else:
        draw_text("Passe o mouse sobre uma", font, (150, 150, 150), screen, 650, 250)
        draw_text("tribo para ver seus detalhes.", font, (150, 150, 150), screen, 630, 300)

    # Botoes na parte inferior
    btn_voltar = pygame.Rect(50, HEIGHT - 100, 150, 50)
    pygame.draw.rect(screen, (180, 50, 50), btn_voltar, border_radius=8)
    draw_text("Voltar", font, WHITE, screen, btn_voltar.x + 20, btn_voltar.y + 5)
    
    btn_comecar = pygame.Rect(WIDTH - 250, HEIGHT - 100, 200, 50)
    if jogador_atual_idx == 4:
        pygame.draw.rect(screen, (50, 180, 50), btn_comecar, border_radius=8)
        draw_text("Iniciar Jogo", font, WHITE, screen, btn_comecar.x + 10, btn_comecar.y + 5)
    else:
        pygame.draw.rect(screen, (100, 100, 100), btn_comecar, border_radius=8)
        draw_text("Aguardando...", small_font, WHITE, screen, btn_comecar.x + 20, btn_comecar.y + 15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_voltar.collidepoint(event.pos):
                tribos_selecionadas.clear()
                state = MENU
            
            if btn_comecar.collidepoint(event.pos) and jogador_atual_idx == 4:
                # Assinala as tribos aos jogadores e entra no jogo
                for idx, t in tribos_selecionadas.items():
                    jogo.jogadores[idx].tribo_selecionada = t
                jogo.iniciar_jogo(list(tribos_selecionadas.values()))
                state = GAME
                
            if jogador_atual_idx < 4:
                for rect, tribo, is_sel in tribes_rects:
                    if rect.collidepoint(event.pos) and not is_sel:
                        tribos_selecionadas[jogador_atual_idx] = tribo

# Carregamento da imagem - usar try/except pois o arquivo pode falhar se rodado de outro diretório
try:
    # Apenas como placeholder futuro, se for pra ter fundo, removemos.
    # O mapa agora será dinâmicos em pontos (os reinos).
    pass
except Exception as e:
    pass

# Definição visual dos pontos do Mapa (Reinos)
reinos_posicoes = [
    {"nome": "Floresta", "pos": (150, 150)},
    {"nome": "Montanha", "pos": (450, 100)},
    {"nome": "Deserto", "pos": (750, 150)},
    {"nome": "Pântano", "pos": (200, 400)},
    {"nome": "Planícies", "pos": (450, 450)},
    {"nome": "Mar", "pos": (700, 400)},
]

# Variáveis de UI state
cartas_selecionadas = []  # Índices na mão do jogador atual
scroll_x_mao = 0          # Scroll horizontal das cartas da mão
scroll_x_mercado = 0      # Scroll horizontal do mercado aberto

def draw_mapa_pontos(screen, jogo):
    # Conexões/Linhas do mapa (Layout básico Ethnos)
    conexoes = [
        (0,1), (1,2),     # Top connection
        (0,3), (1,4), (2,5), # Vertical connection
        (3,4), (4,5)      # Bottom connection
    ]
    for orig, dest in conexoes:
        p1 = reinos_posicoes[orig]["pos"]
        p2 = reinos_posicoes[dest]["pos"]
        pygame.draw.line(screen, (100, 100, 120), p1, p2, 4)
        
    for r_pos in reinos_posicoes:
        x, y = r_pos["pos"]
        # Encontra a instância real do Reino:
        reino_obj = next((r for r in jogo.reinos if r.nome == r_pos["nome"]), None)
        if not reino_obj: continue
        
        # Desenha Círculo
        pygame.draw.circle(screen, reino_obj.cor, (x, y), 50)
        pygame.draw.circle(screen, WHITE, (x, y), 50, 3)
        
        # Nome centrado acima do círculo
        t_nome = small_font.render(r_pos["nome"], True, WHITE)
        screen.blit(t_nome, t_nome.get_rect(center=(x, y - 75)))
        
        # Tokens de Era (Valores na parte de cima) centrados
        tokens_text = []
        for t in reino_obj.glorias:
            txt = str(t.valor)
            if t.era == jogo.eraAtual:
                txt = f"[{txt}]" # Highlight na era atual
            tokens_text.append(txt)
        t_toks = small_font.render("Tokens: " + "-".join(tokens_text), True, (255, 215, 0))
        screen.blit(t_toks, t_toks.get_rect(center=(x, y - 55)))
        
        # Marcadores de controle dos jogadores movidos para BAIXO do círculo
        my_y = y + 65
        if reino_obj.marcadores:
            for jid, qtd in reino_obj.marcadores.items():
                j_obj = jogo.get_jogador_by_id(jid)
                nome_reduzido = j_obj.nome[:12] if j_obj else "?"
                txt_obj = small_font.render(f"{nome_reduzido}: {qtd}", True, (200, 200, 255))
                txt_rect = txt_obj.get_rect(center=(x, my_y))
                
                # Retângulo de fundo para facilitar a leitura
                c_rect = txt_rect.inflate(12, 6)
                pygame.draw.rect(screen, (30, 30, 35), c_rect, border_radius=4)
                screen.blit(txt_obj, txt_rect)
                my_y += 25
        else:
            t_vazio = small_font.render("Vazio", True, (150, 150, 150))
            screen.blit(t_vazio, t_vazio.get_rect(center=(x, my_y)))

def game_loop():
    global state, cartas_selecionadas, scroll_x_mao, scroll_x_mercado
    screen.fill((40, 40, 60))
    
    draw_mapa_pontos(screen, jogo)

    ui_panel = pygame.Rect(900, 0, 380, HEIGHT)
    pygame.draw.rect(screen, (30, 30, 45), ui_panel)
    pygame.draw.rect(screen, (60, 60, 80), ui_panel, 4)

    # UI Direita (HUD)
    ui_x = 940
    pygame.draw.circle(screen, GREEN, (ui_x - 10, 30), 8)
    draw_text(f"Era Atual: {jogo.eraAtual.name}", small_font, WHITE, screen, ui_x, 20)
    
    # Hand UI
    atual = jogo.jogador_atual()
    draw_text("Vez do Jogador:", small_font, (200, 200, 200), screen, ui_x, 60)
    # Highlight
    vez_rect = pygame.Rect(ui_x, 85, 300, 40)
    pygame.draw.rect(screen, (50, 100, 50), vez_rect, border_radius=5)
    draw_text(f"{atual.nome} ({atual.tribo_selecionada.nome if atual.tribo_selecionada else ''})", small_font, WHITE, screen, ui_x + 10, 95)

    
    import pygame.draw as pydraw
    
    # --- MERCADO ABERTO (MESA) ---
    pydraw.rect(screen, (40, 50, 40), (0, 500, 900, 100))
    pydraw.rect(screen, (80, 100, 80), (0, 500, 900, 100), 4)
    draw_text("Mesa:", small_font, (150, 200, 150), screen, 20, 535)
    
    mercado_rects = []
    max_w_mercado = len(jogo.tabuleiro.cartasAbertas) * 115
    max_scroll_m = max(0, max_w_mercado - 700)
    if scroll_x_mercado < -max_scroll_m: scroll_x_mercado = -max_scroll_m
    if scroll_x_mercado > 0: scroll_x_mercado = 0
    
    mx = 110 + scroll_x_mercado
    for i, c in enumerate(jogo.tabuleiro.cartasAbertas):
        r = pygame.Rect(mx, 515, 105, 70)
        pydraw.rect(screen, (60, 80, 60), r, border_radius=4)
        pydraw.rect(screen, (150, 200, 150), r, 2, border_radius=4)
        
        n = c.nome
        if len(n) > 12: n = n[:10] + "..."
        nome_carta_text = f"{c.tribo.nome}" if hasattr(c, "tribo") and c.tribo else n
        
        # Renderização miniatura (Mercado)
        text_mini = pygame.font.SysFont("Verdana", 14).render(nome_carta_text, True, WHITE)
        screen.blit(text_mini, (r.x + 5, r.y + 5))
        
        if hasattr(c, "reino"):
            r_str = c.reino
            text_r = pygame.font.SysFont("Verdana", 12).render(r_str[:12], True, GREEN)
            screen.blit(text_r, (r.x + 5, r.y + 30))
            
        mercado_rects.append((r, c))
        mx += 115
    
    # --- MÃO DO JOGADOR ---
    pydraw.rect(screen, (30, 30, 45), (0, 600, WIDTH, 120))
    pydraw.rect(screen, (60, 60, 80), (0, 600, WIDTH, 120), 4)

    draw_text("Sua Mão:", small_font, WHITE, screen, 20, 640)
    
    # Limitar o scroll maximo baseado no tamanho da mão
    max_w = len(atual.mao) * 155
    max_scroll = max(0, max_w - 700) # Espaço disponível (~700 px)
    if scroll_x_mao < -max_scroll: scroll_x_mao = -max_scroll
    if scroll_x_mao > 0: scroll_x_mao = 0

    hand_rects = []
    hx = 150 + scroll_x_mao
    for idx, c in enumerate(atual.mao):
        r = pygame.Rect(hx, 620, 140, 80)
        pydraw.rect(screen, (70, 70, 100), r, border_radius=5)
        
        # Se for líder ou selecionada, mudar a cor da borda
        border_color = (200, 200, 220)
        thickness = 2
        if idx in cartas_selecionadas:
            if cartas_selecionadas.index(idx) == 0:
                border_color = (255, 215, 0) # LÍDER: Borda Dourada
                thickness = 4
                draw_text("LÍDER", small_font, (255, 215, 0), screen, r.x + 35, r.y - 25)
            else:
                border_color = (0, 255, 0) # SELECIONADA: Borda Verde
                thickness = 3
                
        pydraw.rect(screen, border_color, r, thickness, border_radius=5)
        
        # se for dragão
        n = c.nome
        if len(n) > 15: n = n[:13] + "..."
        
        # Corrigindo exibição da tribo na carta
        nome_carta_text = f"{c.tribo.nome}" if hasattr(c, "tribo") and c.tribo else n
        draw_text(nome_carta_text, small_font, WHITE, screen, r.x + 5, r.y + 10)
        
        if hasattr(c, "reino"):
            r_str = c.reino
            # Se for muito longo o reino, diminui um pouco para caber
            draw_text(r_str[:16], small_font, GREEN, screen, r.x + 5, r.y + 45)
        elif hasattr(c, "efeito"):
            draw_text("DRAGÃO!", small_font, RED, screen, r.x + 5, r.y + 45)
            
        hand_rects.append((r, c, idx))
        hx += 155

    # --- UI Era / Dragões indicativos ---
    draw_text(f"Dragões: {len(jogo.tabuleiro.dragoes)}/3", small_font, RED, screen, ui_x, 125)
    
    draw_text(f"Mesa (abertas): {len(jogo.tabuleiro.cartasAbertas)}", small_font, (220, 220, 220), screen, ui_x, 150)
    draw_text(f"Baralho: {len(jogo.tabuleiro.baralho)}", small_font, (220, 220, 220), screen, ui_x, 180)
    
    btn_comprar = pygame.Rect(ui_x, 230, 200, 45)
    pygame.draw.rect(screen, (50, 100, 200), btn_comprar, border_radius=8)
    draw_text("Comprar Carta", small_font, WHITE, screen, btn_comprar.x + 20, btn_comprar.y + 8)

    btn_band = pygame.Rect(ui_x, 290, 200, 45)
    pygame.draw.rect(screen, (200, 140, 0), btn_band, border_radius=8)
    draw_text("Jogar Bando", small_font, WHITE, screen, btn_band.x + 40, btn_band.y + 8)
    
    btn_passar = pygame.Rect(ui_x, 350, 200, 45)
    pygame.draw.rect(screen, (200, 50, 50), btn_passar, border_radius=8)
    draw_text("Passar Vez", small_font, WHITE, screen, btn_passar.x + 40, btn_passar.y + 8)
    
    y_offset = 430
    draw_text("Bandos e Glórias:", font, WHITE, screen, ui_x, y_offset)
    y_offset += 50
    for j in jogo.jogadores:
        marca = ">>" if j == atual else "  "
        total_b = sum(b.tamanho_atual() for b in j.bandos)
        # O nome do jogador vinha cortado até a letra 5 (Ex: Jogad), aumentei para 12.
        draw_text(f"{marca} {j.nome[:12]} | B:{total_b} | Gpts:{j.glorias}", small_font, (255,215,0), screen, ui_x, y_offset)
        y_offset += 30
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEWHEEL:
            # Pegar a posição do mouse para saber se scrolla a mão (embaixo) ou o mercado (meio)
            mx, my = pygame.mouse.get_pos()
            if my > 600:
                scroll_x_mao += event.y * 30  # scroll na HUD Mão
            elif 500 < my < 600:
                scroll_x_mercado += event.y * 30 # scroll no Mercado
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_comprar.collidepoint(event.pos):
                carta = jogo.tabuleiro.compra_carta()
                if carta:
                    # Regra do dragão
                    if carta.nome == "Dragão":
                        print("DRAGÃO COMPRADO!")
                        jogo.tabuleiro.dragoes.append(carta)
                        if len(jogo.tabuleiro.dragoes) >= 3:
                            print("FIM DA ERA!")
                            jogo.passar_era()
                            # Restart dragons and map layout se tivermos mudado de era.
                            jogo.tabuleiro.dragoes.clear()
                            
                            # Embaralha resto do deck e devolucoes apos pontuacao de era
                            jogo.tabuleiro.baralho.extend(jogo.tabuleiro.cartasAbertas)
                            jogo.tabuleiro.cartasAbertas.clear()
                            jogo.tabuleiro._embaralhar()
                            
                            # Todos esvaziam suas maos/bandos se isso for uma regra estrita
                            # Mas pro Ethnos bandos ficam travados e a mao fica (depende da rulebook)
                            for g_j in jogo.jogadores:
                                g_j.mao.clear() # Normalmente perde a mão no fim da era
                                g_j.bandos.clear() # Bandos esvaziam
                    else:
                        jogo.dar_carta(carta, atual)
                    cartas_selecionadas.clear()
                    jogo.proximo_turno()
            elif btn_band.collidepoint(event.pos):
                if cartas_selecionadas:
                    # Validar seleção: Mesma Tribo ou Mesmo Reino do Líder
                    lider_idx = cartas_selecionadas[0]
                    lider = atual.mao[lider_idx]
                    
                    if not hasattr(lider, "reino"):
                        print("Um dragão não pode ser líder de bando!")
                        continue
                        
                    valido = True
                    is_same_tribe = True
                    is_same_region = True
                    
                    # Checamos todos contra o líder
                    for i in cartas_selecionadas:
                        c = atual.mao[i]
                        if not hasattr(c, "reino") or not hasattr(c, "tribo"):
                            valido = False
                            break
                        if c.tribo.nome != lider.tribo.nome:
                            is_same_tribe = False
                        if c.reino != lider.reino:
                            is_same_region = False
                            
                    valido = valido and (is_same_tribe or is_same_region)
                    
                    if valido:
                        from models import Bando
                        novo_bando = Bando(lider.tribo)
                        
                        cartas_ordenadas = sorted([atual.mao[i] for i in cartas_selecionadas], key=lambda x: x.nome)
                        reino_alvo = lider.reino
                            
                        for c in cartas_ordenadas:
                            novo_bando.tropas.append(c)
                            atual.mao.remove(c)
                                
                        atual.bandos.append(novo_bando)
                        
                        # Logica de Colocar Marcador no Reino Alvo se maior q atual marcador no reino obj
                        if reino_alvo:
                            r_obj = next((r for r in jogo.reinos if r.nome == reino_alvo), None)
                            if r_obj:
                                current_marcadores = r_obj.marcadores.get(atual.id, 0)
                                if novo_bando.tamanho_atual() > current_marcadores:
                                    r_obj.marcadores[atual.id] = current_marcadores + 1
                                    print(f"Marcador adicionado no reino {reino_alvo} pro Jogador {atual.nome}")
                                    
                        if hasattr(novo_bando, "ativar_poder"):
                            novo_bando.ativar_poder()
                        
                        # Esvaziar o Resto da mão ao termino.
                        # Ethnos Rule: jogar bando FAZ OBRIGATORIAMENTE você descartar as outras cartas da mao para as abertas!
                        jogo.tabuleiro.cartasAbertas.extend(atual.mao)
                        atual.mao.clear()
                        cartas_selecionadas.clear()
                        jogo.proximo_turno()
                    else:
                        print("Seleção inválida! Elas devem pertencer à MESMA tribo OU MESMO reino do LÍDER (1ª carta).")
            elif btn_passar.collidepoint(event.pos):
                cartas_selecionadas.clear()
                jogo.proximo_turno()
            else:
                # Checar clique nas cartas da mão para selecionar
                clicked_hand = False
                for r, c, idx in hand_rects:
                    if r.collidepoint(event.pos):
                        clicked_hand = True
                        if idx in cartas_selecionadas:
                            cartas_selecionadas.remove(idx)
                        else:
                            cartas_selecionadas.append(idx)
                        break
                
                # Checar clique no mercado aberto para comprar
                if not clicked_hand:
                    for r, c in mercado_rects:
                        if r.collidepoint(event.pos):
                            # Compra a carta visível na mesa
                            jogo.tabuleiro.cartasAbertas.remove(c)
                            jogo.dar_carta(c, atual)
                            cartas_selecionadas.clear()
                            jogo.proximo_turno()
                            break

while True:
    if state == MENU:
        menu_loop()
    elif state == SETUP:
        setup_loop()
    elif state == GAME:
        game_loop()
        
    pygame.display.flip()
    clock.tick(FPS)