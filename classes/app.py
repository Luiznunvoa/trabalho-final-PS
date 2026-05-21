import pygame
import sys
from .constantes import *
from .jogo import Jogo
from .jogador import Jogador
from .bando import Bando
from .aliado import Aliado
from .reino import REINOS
from .tribo import TRIBOS
from .renderer import Renderer
from .button import Button

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Ethnos - Jogo de Tabuleiro")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        
        self.jogo = Jogo.getInstancia()
        for _ in range(4):
            self.jogo.criar_jogador()
            
        self.state = "MENU"
        self.msg = ""
        self.msg_timer = 0
        self.selected_indices: list[int] = []
        self.setup_pi = 0
        self.setup_tribes: dict[int, str] = {}
        self.setup_race_rects: list = []
        self.setup_btn_rects: dict = {}
        self.market_rects: list = []
        self.hand_rects: list = []
        
        bx = 20
        self.buttons = {
            "draw": Button(bx, ACT_Y, 180, 34, "Comprar do Baralho", (45, 75, 125)),
            "band": Button(bx + 200, ACT_Y, 160, 34, "Jogar Bando", (95, 55, 115)),
            "skip": Button(bx + 380, ACT_Y, 140, 34, "Passar Vez", (120, 100, 40)),
            "confirm": Button(bx + 560, ACT_Y, 130, 34, "Confirmar", (35, 115, 35)),
            "cancel": Button(bx + 710, ACT_Y, 130, 34, "Cancelar", (135, 35, 35)),
            "start": Button(SCREEN_W // 2 - 145, 610, 290, 55, "ESCOLHER TRIBOS", (35, 95, 35)),
            "next_age": Button(SCREEN_W // 2 - 120, 650, 240, 48, "Proxima Era", (35, 95, 35)),
            "end": Button(SCREEN_W // 2 - 120, 700, 240, 48, "Ver Resultado", (35, 95, 35)),
        }
        
    def msg_set(self, txt):
        self.msg = txt
        self.msg_timer = 240
        
    @property
    def cur(self):
        return self.jogo.jogador_atual
        
    def iniciar(self):
        self.jogo.iniciar_jogo()
        self.state = "TURN"
        self.msg_set(f"Era {self.jogo.eraAtual.numero} ({self.jogo.eraAtual}) comecou! Vez de {self.cur.nome}.")
        
    def comprar_baralho(self):
        j = self.cur
        if len(j.mao) >= 10:
            self.msg_set("Mao cheia! (max 10)"); return
        carta = self.jogo.tabuleiro.compra_carta()
        ok = self.jogo.dar_carta(carta, j)
        if ok:
            self.jogo.proximo_turno()
            self.msg_set(f"Vez de {self.cur.nome}.")
        elif len(self.jogo.tabuleiro.dragoes) >= NUM_DRAGONS:
            self._end_age()
            
    def comprar_mercado(self, idx):
        j = self.cur
        if len(j.mao) >= 10:
            self.msg_set("Mao cheia! (max 10)"); return
        cartas = self.jogo.tabuleiro.cartasAbertas
        if 0 <= idx < len(cartas):
            carta = cartas.pop(idx)
            j.pegar_carta(carta)
            self.jogo.proximo_turno()
            self.msg_set(f"Vez de {self.cur.nome}.")
            
    def jogar_bando(self, indices, leader_idx):
        j = self.cur
        aliados = [j.mao[i] for i in sorted(indices) if isinstance(j.mao[i], Aliado)]
        if not aliados:
            return
        bando = Bando(aliados, j)
        lider = j.mao[leader_idx]
        if not isinstance(lider, Aliado):
            return
        bando.define_lider(lider)
        
        band_set = set(indices)
        descartadas = [c for i, c in enumerate(j.mao) if i not in band_set]
        for c in descartadas:
            self.jogo.tabuleiro.receber_carta(c)
        j.mao.clear()
        
        reino = REINOS[lider.reino.idx]
        self.jogo.fazer_ataque(bando, reino)
        
        bonus = BAND_BONUS.get(len(aliados), 15)
        self.msg_set(f"{j.nome} jogou bando de {len(aliados)} em {reino.nome_curto} (+{bonus})")
        
        if len(self.jogo.tabuleiro.dragoes) >= NUM_DRAGONS:
            self._end_age()
        elif self.state not in ("AGE_END", "GAME_OVER"):
            self.jogo.proximo_turno()
            self.state = "TURN"
            self.msg_set(f"Vez de {self.cur.nome}.")
            
    def _end_age(self):
        self.jogo._pontuar_reinos()
        self.msg_set(f"Era {self.jogo.eraAtual.numero} ({self.jogo.eraAtual}) terminou!")
        if self.jogo.eraAtual.value == 3:
            self.state = "GAME_OVER"
        else:
            self.state = "AGE_END"
            
    def validate_band(self, indices):
        if not indices:
            return False
        aliados = [self.cur.mao[i] for i in indices if isinstance(self.cur.mao[i], Aliado)]
        if len(aliados) != len(indices):
            return False
        if len(set(c.tribo.nome for c in aliados)) == 1:
            return True
        if len(set(c.reino.idx for c in aliados)) == 1:
            return True
        return False
        
    def on_click_turn(self, pos):
        if self.buttons["draw"].clicked(pos):
            self.comprar_baralho(); return
        for rect, idx in self.market_rects:
            if rect.collidepoint(pos):
                self.comprar_mercado(idx); return
        if self.buttons["band"].clicked(pos):
            if any(isinstance(c, Aliado) for c in self.cur.mao):
                self.state = "SELECT_BAND"
                self.selected_indices.clear()
            else:
                self.msg_set("Sem cartas para bando!")
            return
        if self.buttons["skip"].clicked(pos):
            self.jogo.proximo_turno()
            self.msg_set(f"Vez de {self.cur.nome}.")
            
    def on_click_band(self, pos):
        for rect, i in self.hand_rects:
            if rect.collidepoint(pos) and isinstance(self.cur.mao[i], Aliado):
                if i in self.selected_indices:
                    self.selected_indices.remove(i)
                else:
                    self.selected_indices.append(i)
                return
        if self.buttons["confirm"].clicked(pos):
            if self.validate_band(self.selected_indices):
                if len(self.selected_indices) == 1:
                    self.jogar_bando(self.selected_indices, self.selected_indices[0])
                    self.selected_indices.clear()
                else:
                    self.state = "SELECT_LEADER"
            else:
                self.msg_set("Bando invalido! Mesma tribo OU mesmo reino.")
            return
        if self.buttons["cancel"].clicked(pos):
            self.state = "TURN"
            self.selected_indices.clear()
            
    def on_click_leader(self, pos):
        for rect, i in self.hand_rects:
            if rect.collidepoint(pos) and i in self.selected_indices:
                self.jogar_bando(self.selected_indices, i)
                self.selected_indices.clear()
                return
        if self.buttons["cancel"].clicked(pos):
            self.state = "SELECT_BAND"
            
    def on_click_age_end(self, pos):
        from .era import Era
        if self.jogo.eraAtual != Era.EPILOGO and self.buttons["next_age"].clicked(pos):
            self.jogo.passar_era()
            self.state = "TURN"
            self.msg_set(f"Era {self.jogo.eraAtual.numero} ({self.jogo.eraAtual}) comecou!")
        elif self.jogo.eraAtual == Era.EPILOGO and self.buttons["end"].clicked(pos):
            self.state = "GAME_OVER"
            
    def on_click_setup(self, pos):
        taken = set(self.setup_tribes.values())
        for rect, nome in self.setup_race_rects:
            if rect.collidepoint(pos):
                if self.setup_tribes.get(self.setup_pi) == nome:
                    del self.setup_tribes[self.setup_pi]
                elif nome not in taken:
                    self.setup_tribes[self.setup_pi] = nome
                return
        if "back" in self.setup_btn_rects and self.setup_btn_rects["back"].collidepoint(pos):
            self.setup_pi = max(0, self.setup_pi - 1); return
        if "next" in self.setup_btn_rects and self.setup_btn_rects["next"].collidepoint(pos):
            self.setup_pi = min(3, self.setup_pi + 1); return
        if "start" in self.setup_btn_rects and self.setup_btn_rects["start"].collidepoint(pos):
            for pi, nome in self.setup_tribes.items():
                self.jogo.jogadores[pi].tribo = TRIBOS[nome]
            self.iniciar()
            
    def run(self):
        running = True
        R = self.renderer
        while running:
            self.clock.tick(FPS)
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        if self.state == "SETUP":
                            self.state = "MENU"
                        else:
                            running = False
                    elif ev.key == pygame.K_r and self.state == "GAME_OVER":
                        self.state = "MENU"
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    pos = ev.pos
                    if self.state == "MENU":
                        if self.buttons["start"].clicked(pos):
                            self.setup_tribes.clear()
                            self.setup_pi = 0
                            self.state = "SETUP"
                    elif self.state == "SETUP":
                        self.on_click_setup(pos)
                    elif self.state == "TURN":
                        self.on_click_turn(pos)
                    elif self.state == "SELECT_BAND":
                        self.on_click_band(pos)
                    elif self.state == "SELECT_LEADER":
                        self.on_click_leader(pos)
                    elif self.state == "AGE_END":
                        self.on_click_age_end(pos)
                        
            self.screen.fill(BG)
            jogo = self.jogo
            if self.state == "MENU":
                R.draw_menu(self.buttons["start"])
            elif self.state == "SETUP":
                self.setup_btn_rects = R.draw_setup(self.setup_pi, self.setup_tribes, self.setup_race_rects)
            elif self.state == "GAME_OVER":
                R.draw_game_over(jogo.jogadores)
            elif self.state == "AGE_END":
                R.draw_age_end(jogo.eraAtual, jogo.jogadores, self.buttons["next_age"], self.buttons["end"])
            else:
                R.draw_top_bar(jogo.jogadores, jogo.id_jogador_atual)
                R.draw_board(jogo.jogadores, jogo.eraAtual)
                R.draw_sidebar(jogo.tabuleiro, jogo.jogadores)
                self.market_rects = R.draw_market(jogo.tabuleiro.cartasAbertas)
                R.draw_action_bar(self.state, self.buttons)
                is_ldr = self.state == "SELECT_LEADER"
                self.hand_rects = R.draw_hand(self.cur, self.state, self.selected_indices, is_ldr)
                if self.msg_timer > 0:
                    self.msg_timer -= 1
                R.draw_message(self.msg, self.msg_timer)
                
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()