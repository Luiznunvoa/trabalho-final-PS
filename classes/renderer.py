import pygame
import math
from .constantes import *
from .carta import Carta
from .jogador import Jogador
from .tabuleiro import Tabuleiro
from .era import Era
from .button import Button

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.f_tiny = pygame.font.SysFont("segoeui", 12)
        self.f_sm = pygame.font.SysFont("segoeui", 15)
        self.f_md = pygame.font.SysFont("segoeui", 18, bold=True)
        self.f_lg = pygame.font.SysFont("segoeui", 26, bold=True)
        self.f_xl = pygame.font.SysFont("segoeui", 40, bold=True)
        self.f_icon = pygame.font.SysFont("segoeui", 30, bold=True)
        self.f_title = pygame.font.SysFont("segoeui", 52, bold=True)

    @staticmethod
    def panel(surf, rect, bg=PANEL_BG, bd=PANEL_BD, bw=2, r=12):
        pygame.draw.rect(surf, (12, 12, 22), rect.move(4, 4), border_radius=r)
        pygame.draw.rect(surf, bg, rect, border_radius=r)
        pygame.draw.rect(surf, bd, rect, bw, border_radius=r)

    def draw_card(self, surf, carta, x, y, w=70, h=100, selected=False, is_leader=False):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surf, (12, 12, 22), rect.move(3, 3), border_radius=7)
        if is_leader:
            glow = rect.inflate(14, 14)
            pygame.draw.rect(surf, (180, 150, 30), glow, border_radius=10)
            pygame.draw.rect(surf, GOLD, glow, 3, border_radius=10)
        pygame.draw.rect(surf, CARD_BG, rect, border_radius=7)
        if is_leader:
            pygame.draw.rect(surf, GOLD, rect, 4, border_radius=7)
        elif selected:
            pygame.draw.rect(surf, (255, 255, 80), rect, 3, border_radius=7)
        else:
            bc = carta.region_color if not carta.is_dragon else (150, 40, 40)
            pygame.draw.rect(surf, bc, rect, 2, border_radius=7)

        if carta.is_dragon:
            inner = rect.inflate(-8, -8)
            pygame.draw.rect(surf, (70, 18, 18), inner, border_radius=5)
            dt = self.f_icon.render("D", True, (230, 60, 60))
            surf.blit(dt, dt.get_rect(center=(x + w // 2, y + h // 2 - 4)))
            lt = self.f_tiny.render("DRAGAO", True, (210, 90, 90))
            surf.blit(lt, lt.get_rect(center=(x + w // 2, y + h - 13)))
        else:
            bar = pygame.Rect(x + 3, y + 3, w - 6, 20)
            pygame.draw.rect(surf, carta.region_color, bar, border_radius=4)
            rn = self.f_tiny.render(REGION_SHORT[carta.region_idx], True, WHITE)
            surf.blit(rn, rn.get_rect(center=bar.center))
            cx_c, cy_c = x + w // 2, y + h // 2 + 3
            r = min(w, h) // 5 + 2
            pygame.draw.circle(surf, carta.race_color, (cx_c, cy_c), r)
            pygame.draw.circle(surf, BLACK, (cx_c, cy_c), r, 2)
            sym = TRIBE_SYMBOLS.get(carta.race, "?")
            st = self.f_lg.render(sym, True, WHITE)
            surf.blit(st, st.get_rect(center=(cx_c, cy_c)))
            rl = self.f_tiny.render(carta.race, True, DGRAY)
            surf.blit(rl, rl.get_rect(center=(x + w // 2, y + h - 11)))

        if is_leader:
            cx_cr = x + w - 13
            cy_cr = y + 7
            pts = [(cx_cr-8,cy_cr+10), (cx_cr-6,cy_cr), (cx_cr-2,cy_cr+7),
                   (cx_cr,cy_cr-2), (cx_cr+2,cy_cr+7), (cx_cr+6,cy_cr), (cx_cr+8,cy_cr+10)]
            pygame.draw.polygon(surf, GOLD, pts)
            pygame.draw.polygon(surf, (150, 120, 0), pts, 1)
            lt = self.f_tiny.render("LIDER", True, GOLD)
            surf.blit(lt, lt.get_rect(center=(x + w // 2, y + h + 6)))
        return rect

    def draw_top_bar(self, jogadores, current_idx):
        s = self.screen
        pygame.draw.rect(s, (18, 18, 32), (0, 0, SCREEN_W, TOP_H))
        pygame.draw.line(s, PANEL_BD, (0, TOP_H), (SCREEN_W, TOP_H), 2)
        pw = SCREEN_W // 4
        for i, p in enumerate(jogadores):
            x = i * pw + 4
            pnl = pygame.Rect(x, 3, pw - 8, TOP_H - 6)
            is_cur = i == current_idx
            bg = (42, 42, 68) if is_cur else (28, 28, 45)
            pygame.draw.rect(s, bg, pnl, border_radius=10)
            if is_cur:
                pygame.draw.rect(s, p.cor, pnl, 3, border_radius=10)
                tag = self.f_tiny.render("SUA VEZ", True, BLACK)
                tr = tag.get_rect(topright=(x + pw - 16, 6))
                pygame.draw.rect(s, GOLD, tr.inflate(10, 4), border_radius=5)
                s.blit(tag, tr)
            else:
                pygame.draw.rect(s, (48, 48, 68), pnl, 1, border_radius=10)
            pygame.draw.circle(s, p.cor, (x + 16, 18), 7)
            nt = self.f_sm.render(p.nome, True, WHITE)
            s.blit(nt, (x + 28, 8))
            if p.tribo:
                bx = x + 28 + nt.get_width() + 6
                pygame.draw.circle(s, p.race_color, (bx + 8, 16), 9)
                pygame.draw.circle(s, WHITE, (bx + 8, 16), 9, 1)
                st = self.f_tiny.render(p.race_symbol, True, WHITE)
                s.blit(st, st.get_rect(center=(bx + 8, 16)))
            pt = self.f_md.render(str(p.glorias), True, GOLD)
            s.blit(pt, (x + 28, 28))
            s.blit(self.f_tiny.render("pts", True, GRAY), (x + 28 + pt.get_width() + 3, 33))
            info = self.f_tiny.render(f"Mao:{len(p.mao)}    Bando:{len(p.bandos)}", True, GRAY)
            s.blit(info, (x + 130, 10))
            for r in range(6):
                rx = x + 130 + r * 26
                ry = 30
                mini = pygame.Rect(rx, ry, 22, 14)
                c = REGION_COLORS[r] if p.controle[r] > 0 else (38, 38, 52)
                pygame.draw.rect(s, c, mini, border_radius=3)
                if p.controle[r] > 0:
                    ct = self.f_tiny.render(str(p.controle[r]), True, WHITE)
                    s.blit(ct, ct.get_rect(center=mini.center))
                else:
                    pygame.draw.rect(s, (52, 52, 68), mini, 1, border_radius=3)
            for bi in range(min(len(p.bandos), 8)):
                bx_ = x + 130 + bi * 14
                pygame.draw.rect(s, p.cor, (bx_, 50, 10, 8), border_radius=2)
                pygame.draw.rect(s, WHITE, (bx_, 50, 10, 8), 1, border_radius=2)

    def draw_board(self, jogadores, era):
        s = self.screen
        mp = pygame.Rect(10, MAP_Y, 700, MAP_H)
        self.panel(s, mp, (26, 26, 42), (48, 48, 72))
        title = self.f_sm.render(f"Mapa  |  Era {era.numero}/3 ({era})", True, LGRAY)
        s.blit(title, (20, MAP_Y + 5))
        cx, cy = 360, MAP_Y + MAP_H // 2 + 10
        rad = 52
        for i in range(6):
            ang = math.radians(60 * i - 30)
            px = cx + int(115 * math.cos(ang))
            py = cy + int(90 * math.sin(ang))
            pts = []
            for j in range(6):
                a = math.radians(60 * j)
                pts.append((px + int(rad * math.cos(a)), py + int(rad * math.sin(a))))
            shd = [(hx + 3, hy + 3) for hx, hy in pts]
            pygame.draw.polygon(s, (12, 12, 22), shd)
            pygame.draw.polygon(s, REGION_COLORS[i], pts)
            pygame.draw.polygon(s, WHITE, pts, 2)
            nt = self.f_sm.render(REGION_SHORT[i], True, WHITE)
            s.blit(nt, nt.get_rect(center=(px, py - 20)))
            sc = REGION_SCORES[i]
            st = self.f_tiny.render(f"{sc[0]}/{sc[1]}/{sc[2]}", True, (240, 240, 240))
            s.blit(st, st.get_rect(center=(px, py - 6)))
            active = [(pi, p1.controle[i]) for pi, p1 in enumerate(jogadores) if p1.controle[i] > 0]
            for ti, (pi, cnt) in enumerate(active):
                tx = px - len(active) * 12 + ti * 26
                ty = py + 10
                pygame.draw.circle(s, jogadores[pi].cor, (tx + 8, ty + 8), 10)
                pygame.draw.circle(s, WHITE, (tx + 8, ty + 8), 10, 1)
                ct = self.f_tiny.render(str(cnt), True, WHITE)
                s.blit(ct, ct.get_rect(center=(tx + 8, ty + 8)))

    def draw_sidebar(self, tabuleiro, jogadores):
        s = self.screen
        pnl = pygame.Rect(720, MAP_Y, SCREEN_W - 730, MAP_H)
        self.panel(s, pnl, (26, 26, 42), (48, 48, 72))
        x, y = 735, MAP_Y + 10
        s.blit(self.f_md.render("Baralho", True, LGRAY), (x, y)); y += 24
        dt = self.f_lg.render(str(len(tabuleiro.baralho)), True, WHITE)
        s.blit(dt, (x, y))
        s.blit(self.f_sm.render("cartas", True, GRAY), (x + dt.get_width() + 8, y + 6)); y += 35
        s.blit(self.f_md.render("Dragoes", True, (220, 80, 80)), (x, y)); y += 24
        for d in range(NUM_DRAGONS):
            c = (200, 50, 50) if d < len(tabuleiro.dragoes) else (55, 55, 55)
            pygame.draw.circle(s, c, (x + 15 + d * 35, y + 10), 13)
            pygame.draw.circle(s, WHITE, (x + 15 + d * 35, y + 10), 13, 1)
            if d < len(tabuleiro.dragoes):
                dt2 = self.f_sm.render("D", True, WHITE)
                s.blit(dt2, dt2.get_rect(center=(x + 15 + d * 35, y + 10)))
        y += 35
        pygame.draw.line(s, PANEL_BD, (x, y), (x + pnl.w - 30, y), 1); y += 8
        s.blit(self.f_md.render("Tribos dos Jogadores", True, LGRAY), (x, y)); y += 24
        for p in jogadores:
            if p.tribo:
                rc = p.tribo.cor
                pygame.draw.circle(s, rc, (x + 10, y + 8), 9)
                pygame.draw.circle(s, BLACK, (x + 10, y + 8), 9, 1)
                st = self.f_sm.render(p.tribo.simbolo, True, WHITE)
                s.blit(st, st.get_rect(center=(x + 10, y + 8)))
                s.blit(self.f_sm.render(p.nome, True, p.cor), (x + 26, y))
                s.blit(self.f_tiny.render(p.tribo.nome, True, LGRAY), (x + 110, y + 2))
            y += 22
        y += 6
        pygame.draw.line(s, PANEL_BD, (x, y), (x + pnl.w - 30, y), 1); y += 8
        s.blit(self.f_md.render("Bonus por Bando", True, LGRAY), (x, y)); y += 22
        for sz, pts in BAND_BONUS.items():
            lbl = "carta" if sz == 1 else "cartas"
            s.blit(self.f_tiny.render(f"{sz} {lbl} = {pts} pts", True, GRAY), (x, y)); y += 15

    def draw_market(self, cartas):
        s = self.screen
        pnl = pygame.Rect(10, MKT_Y, SCREEN_W - 20, MKT_H)
        self.panel(s, pnl, (26, 26, 42), (48, 48, 72))
        rects = []
        x0, y0 = 20, MKT_Y + 22
        label = self.f_sm.render(f"Mercado Aberto ({len(cartas)})", True, LGRAY)
        s.blit(label, (x0, MKT_Y + 3))
        if not cartas:
            s.blit(self.f_sm.render("Nenhuma carta no mercado.", True, GRAY), (x0, y0 + 12))
            return rects
        cw, ch = 54, 76
        spacing = cw + 4
        mx = min(len(cartas), (SCREEN_W - 60) // spacing)
        for i in range(mx):
            r = self.draw_card(s, cartas[i], x0 + i * spacing, y0, w=cw, h=ch)
            rects.append((r, i))
        if len(cartas) > mx:
            s.blit(self.f_sm.render(f"+{len(cartas) - mx}", True, GRAY), (x0 + mx * spacing, y0 + 28))
        return rects

    def draw_action_bar(self, state, buttons):
        s = self.screen
        pygame.draw.rect(s, (20, 20, 35), (0, ACT_Y - 4, SCREEN_W, 40))
        if state == "TURN":
            buttons["draw"].draw(s, self.f_md)
            buttons["band"].draw(s, self.f_md)
            buttons["skip"].draw(s, self.f_md)
            s.blit(self.f_sm.render("Compre 1 carta, jogue bando ou passe a vez.", True, GRAY),
                   (740, ACT_Y + 6))
        elif state == "SELECT_BAND":
            s.blit(self.f_md.render("Selecione cartas (mesma tribo OU mesmo reino). Confirme.",
                                    True, (255, 255, 100)), (20, ACT_Y + 4))
            buttons["confirm"].draw(s, self.f_md)
            buttons["cancel"].draw(s, self.f_md)
        elif state == "SELECT_LEADER":
            s.blit(self.f_md.render("Clique no LIDER do bando (determina o reino).", True,
                                    (255, 200, 80)), (20, ACT_Y + 4))
            buttons["cancel"].draw(s, self.f_md)

    def draw_hand(self, jogador, state, selected_indices, is_leader):
        s = self.screen
        pnl = pygame.Rect(10, HAND_Y, SCREEN_W - 20, HAND_H)
        bc = jogador.cor if state in ("SELECT_BAND", "SELECT_LEADER") else (48, 48, 72)
        self.panel(s, pnl, (28, 28, 48), bc)
        tribo_info = f" ({jogador.tribo.nome})" if jogador.tribo else ""
        label = self.f_sm.render(f"Mao de {jogador.nome}{tribo_info}  ({len(jogador.mao)} cartas)", True, jogador.cor)
        s.blit(label, (20, HAND_Y + 3))
        rects = []
        if not jogador.mao:
            s.blit(self.f_sm.render("Mao vazia.", True, GRAY), (20, HAND_Y + 35))
            return rects
        cw, ch = 66, 96
        spacing = cw + 7
        if len(jogador.mao) * spacing > SCREEN_W - 60:
            spacing = (SCREEN_W - 60) // len(jogador.mao)
        sx = max(20, (SCREEN_W - len(jogador.mao) * spacing) // 2)
        y = HAND_Y + 22
        for i, carta in enumerate(jogador.mao):
            sel = i in selected_indices
            ldr = is_leader and sel
            r = self.draw_card(s, carta, sx + i * spacing, y, w=cw, h=ch, selected=sel, is_leader=ldr)
            rects.append((r, i))
        return rects

    def draw_message(self, msg, timer):
        if msg and timer > 0:
            s = self.screen
            pygame.draw.rect(s, (14, 14, 28), (0, MSG_Y, SCREEN_W, 40))
            pygame.draw.line(s, GOLD, (0, MSG_Y), (SCREEN_W, MSG_Y), 1)
            s.blit(self.f_md.render(msg, True, (255, 255, 130)), (15, MSG_Y + 8))

    def draw_menu(self, btn_start):
        s = self.screen
        ts = self.f_title.render("ETHNOS", True, (100, 80, 0))
        s.blit(ts, ts.get_rect(center=(SCREEN_W // 2 + 3, 63)))
        t = self.f_title.render("ETHNOS", True, GOLD)
        s.blit(t, t.get_rect(center=(SCREEN_W // 2, 60)))
        sub = self.f_md.render("Jogo de Tabuleiro Digital - 4 Jogadores Local", True, LGRAY)
        s.blit(sub, sub.get_rect(center=(SCREEN_W // 2, 105)))
        rp = pygame.Rect(SCREEN_W // 2 - 440, 135, 880, 460)
        self.panel(s, rp, (28, 28, 48), (55, 55, 85))
        x, y = rp.x + 30, rp.y + 18
        s.blit(self.f_lg.render("Como Jogar", True, GOLD), (x, y)); y += 36
        rules = [
            ("OBJETIVO:", " Acumule glorias ao longo de 3 Eras jogando Bandos e controlando Reinos."),
            ("", ""),
            ("NO SEU TURNO voce faz UMA acao:", ""),
            (" 1) COMPRAR CARTA:", " do baralho (fechada) ou do mercado (aberta). Max 10 na mao."),
            (" 2) JOGAR BANDO:", " selecione cartas com mesma TRIBO ou mesmo REINO."),
            (" 3) PASSAR VEZ:", " pula o turno sem fazer nada."),
            ("", ""),
            ("BANDO - Detalhes:", ""),
            ("  Lider:", " Escolha 1 carta como LIDER. O reino do lider recebe seu marcador."),
            ("  Descarte:", " Cartas NAO selecionadas vao para o mercado aberto."),
            ("  Pontos:", " Bandos maiores = mais glorias (2=1, 3=3, 4=6, 5=10, 6=15)."),
            ("", ""),
            ("DRAGOES:", " Ha 3 no baralho. O 3o encerra a Era imediatamente."),
            ("  Fim de Era:", " Quem domina cada reino (mais marcadores) ganha glorias bonus."),
            ("", ""),
            ("TRIBOS:", " Cada jogador escolhe 1 tribo - habilidade ativa ao jogar bando:"),
            ("  Centauro (C):", " Compra 1 carta extra.        Halfling (H): +1 pt por carta."),
            ("  Esqueleto (S):", " Guarda cartas p/ proxima Era.  Elfo (E): Mantem 1 carta."),
            ("  Gigante (G):", " +3 pts bonus.                Mago (M): Compra topo do baralho."),
            ("  Troll (T):", " +1 controle.                 Orc (O): Pega 1 do mercado."),
        ]
        for lbl, desc in rules:
            if lbl:
                lt = self.f_sm.render(lbl, True, (200, 200, 255))
                s.blit(lt, (x, y))
                if desc:
                    s.blit(self.f_sm.render(desc, True, LGRAY), (x + lt.get_width(), y))
            y += 19
        btn_start.draw(s, self.f_lg)

    def draw_setup(self, current_pi, selected, race_rects_out):
        s = self.screen
        pcolor = PLAYER_COLORS[current_pi]
        pname = PLAYER_NAMES[current_pi]
        ts = self.f_xl.render("ESCOLHA DE TRIBOS", True, (100, 80, 0))
        s.blit(ts, ts.get_rect(center=(SCREEN_W // 2 + 2, 42)))
        t = self.f_xl.render("ESCOLHA DE TRIBOS", True, GOLD)
        s.blit(t, t.get_rect(center=(SCREEN_W // 2, 40)))
        pygame.draw.circle(s, pcolor, (SCREEN_W // 2 - 145, 78), 12)
        s.blit(self.f_lg.render(f"{pname} - escolha sua tribo!", True, pcolor), (SCREEN_W // 2 - 125, 66))

        sx = 30
        for pi in range(4):
            ch = selected.get(pi)
            pc = PLAYER_COLORS[pi]
            bg = (42, 48, 68) if pi == current_pi else (28, 28, 45)
            pr = pygame.Rect(sx, 100, 175, 38)
            pygame.draw.rect(s, bg, pr, border_radius=7)
            pygame.draw.rect(s, pc if pi == current_pi else (48, 48, 65), pr, 2, border_radius=7)
            pygame.draw.circle(s, pc, (sx + 14, 119), 6)
            s.blit(self.f_sm.render(PLAYER_NAMES[pi], True, WHITE), (sx + 26, 105))
            if ch:
                s.blit(self.f_sm.render(ch, True, TRIBE_COLORS[ch]), (sx + 26, 121))
            elif pi == current_pi:
                s.blit(self.f_tiny.render("escolhendo...", True, GOLD), (sx + 26, 123))
            sx += 185

        taken = set(selected.values())
        race_rects_out.clear()
        cols, cw, ch_c = 4, 305, 190
        gx, gy = 22, 18
        tw = cols * cw + (cols - 1) * gx
        x0 = (SCREEN_W - tw) // 2
        y0 = 150
        for i, nome in enumerate(ALL_TRIBES):
            col, row = i % cols, i // cols
            rx = x0 + col * (cw + gx)
            ry = y0 + row * (ch_c + gy)
            rect = pygame.Rect(rx, ry, cw, ch_c)
            race_rects_out.append((rect, nome))
            is_taken = nome in taken
            is_mine = selected.get(current_pi) == nome
            if is_mine:
                bg, bd, bw = (45, 65, 45), GOLD, 3
            elif is_taken:
                bg, bd, bw = (22, 22, 32), (45, 45, 45), 1
            else:
                bg, bd, bw = (32, 32, 52), (75, 75, 105), 2
            pygame.draw.rect(s, (10, 10, 18), rect.move(3, 3), border_radius=12)
            pygame.draw.rect(s, bg, rect, border_radius=12)
            pygame.draw.rect(s, bd, rect, bw, border_radius=12)
            dim = is_taken and not is_mine
            ac = GRAY if dim else WHITE
            ccx, ccy = rx + 42, ry + 48
            rc = TRIBE_COLORS.get(nome, GRAY)
            if dim:
                rc = tuple(c // 3 for c in rc)
            pygame.draw.circle(s, rc, (ccx, ccy), 26)
            pygame.draw.circle(s, ac, (ccx, ccy), 26, 2)
            sym_t = self.f_icon.render(TRIBE_SYMBOLS[nome], True, ac)
            s.blit(sym_t, sym_t.get_rect(center=(ccx, ccy)))
            s.blit(self.f_sm.render(TRIBE_DESC[nome], True, LGRAY if not dim else DGRAY), (rx + 80, ry + 50))
            if dim:
                owner = [pi for pi, r in selected.items() if r == nome][0]
                s.blit(self.f_sm.render(f"Escolhida por {PLAYER_NAMES[owner]}", True, PLAYER_COLORS[owner]), (rx + 80, ry + 73))
            elif is_mine:
                s.blit(self.f_lg.render("SELECIONADA", True, GOLD), (rx + 80, ry + 73))
            ey = ry + 105
            for ri in range(6):
                ec = REGION_COLORS[ri] if not dim else tuple(c // 3 for c in REGION_COLORS[ri])
                ex = rx + 14 + ri * 46
                er = pygame.Rect(ex, ey, 40, 52)
                pygame.draw.rect(s, ec, er, border_radius=4)
                pygame.draw.rect(s, (140, 140, 140) if not dim else (45, 45, 45), er, 1, border_radius=4)
                rt1 = self.f_tiny.render(REGION_SHORT[ri], True, ac)
                s.blit(rt1, rt1.get_rect(center=(ex + 20, ey + 18)))
                rt2 = self.f_tiny.render(TRIBE_SYMBOLS[nome], True, ac)
                s.blit(rt2, rt2.get_rect(center=(ex + 20, ey + 38)))

        btn_y = y0 + 2 * (ch_c + gy) + 12
        rects_out = {}
        if current_pi > 0:
            br = pygame.Rect(SCREEN_W // 2 - 330, btn_y, 185, 46)
            pygame.draw.rect(s, (10, 10, 18), br.move(3, 3), border_radius=10)
            pygame.draw.rect(s, (75, 55, 55), br, border_radius=10)
            pygame.draw.rect(s, WHITE, br, 2, border_radius=10)
            bt = self.f_md.render("< Jogador Anterior", True, WHITE)
            s.blit(bt, bt.get_rect(center=br.center))
            rects_out["back"] = br
        if current_pi < 3 and current_pi in selected:
            nr = pygame.Rect(SCREEN_W // 2 + 145, btn_y, 185, 46)
            pygame.draw.rect(s, (10, 10, 18), nr.move(3, 3), border_radius=10)
            pygame.draw.rect(s, (45, 75, 125), nr, border_radius=10)
            pygame.draw.rect(s, WHITE, nr, 2, border_radius=10)
            bt = self.f_md.render("Proximo Jogador >", True, WHITE)
            s.blit(bt, bt.get_rect(center=nr.center))
            rects_out["next"] = nr
        if len(selected) == 4:
            sr = pygame.Rect(SCREEN_W // 2 - 135, btn_y, 270, 46)
            pygame.draw.rect(s, (10, 10, 18), sr.move(3, 3), border_radius=10)
            pygame.draw.rect(s, (35, 115, 35), sr, border_radius=10)
            pygame.draw.rect(s, WHITE, sr, 2, border_radius=10)
            bt = self.f_lg.render("COMECAR PARTIDA", True, WHITE)
            s.blit(bt, bt.get_rect(center=sr.center))
            rects_out["start"] = sr
        esc = self.f_sm.render("ESC = voltar ao menu", True, GRAY)
        s.blit(esc, esc.get_rect(center=(SCREEN_W // 2, btn_y + 62)))
        return rects_out

    def draw_age_end(self, era, jogadores, btn_next, btn_end):
        s = self.screen
        t = self.f_xl.render(f"Fim da Era {era.numero} - {era}!", True, GOLD)
        s.blit(t, t.get_rect(center=(SCREEN_W // 2, 75)))
        pnl = pygame.Rect(SCREEN_W // 2 - 400, 115, 800, 360)
        self.panel(s, pnl, (28, 28, 48), (55, 55, 85))
        x, y = pnl.x + 25, pnl.y + 18
        s.blit(self.f_lg.render("Pontuacao", True, GOLD), (x, y)); y += 42
        heads = ["Jogador", "Pts"] + REGION_SHORT
        cw_ = [170, 75] + [80] * 6
        for ci, h in enumerate(heads):
            c = REGION_COLORS[ci - 2] if ci >= 2 else LGRAY
            s.blit(self.f_md.render(h, True, c), (x + sum(cw_[:ci]), y))
        y += 32
        for p in jogadores:
            s.blit(self.f_md.render(p.nome, True, p.cor), (x, y))
            s.blit(self.f_lg.render(str(p.glorias), True, GOLD), (x + cw_[0], y))
            for r in range(6):
                rx_ = x + cw_[0] + cw_[1] + r * cw_[2]
                if p.controle[r] > 0:
                    pygame.draw.circle(s, p.cor, (rx_ + 15, y + 12), 12)
                    ct = self.f_sm.render(str(p.controle[r]), True, WHITE)
                    s.blit(ct, ct.get_rect(center=(rx_ + 15, y + 12)))
                else:
                    s.blit(self.f_tiny.render("-", True, DGRAY), (rx_ + 12, y + 5))
            y += 50
        y += 8
        for p in jogadores:
            tribo_name = p.tribo.nome if p.tribo else "?"
            s.blit(self.f_sm.render(f"{p.nome}: {len(p.bandos)} bando(s) | Tribo: {tribo_name}", True, p.cor), (pnl.x + 25, y))
            y += 22
        btn_y = y + 12
        if era != Era.EPILOGO:
            btn_next.rect.y = btn_y
            btn_next.draw(s, self.f_lg)
        else:
            btn_end.rect.y = btn_y
            btn_end.draw(s, self.f_lg)

    def draw_game_over(self, jogadores):
        s = self.screen
        ts = self.f_title.render("FIM DE JOGO!", True, (100, 80, 0))
        s.blit(ts, ts.get_rect(center=(SCREEN_W // 2 + 3, 83)))
        t = self.f_title.render("FIM DE JOGO!", True, GOLD)
        s.blit(t, t.get_rect(center=(SCREEN_W // 2, 80)))
        pnl = pygame.Rect(SCREEN_W // 2 - 320, 130, 640, 420)
        self.panel(s, pnl, (28, 28, 48), (55, 55, 85))
        ranking = sorted(jogadores, key=lambda p: p.glorias, reverse=True)
        medals = ["1o", "2o", "3o", "4o"]
        medal_c = [GOLD, (192, 192, 192), (205, 127, 50), GRAY]
        for i, p in enumerate(ranking):
            y = 175 + i * 80
            pygame.draw.circle(s, medal_c[i], (pnl.x + 48, y + 22), 24)
            pygame.draw.circle(s, WHITE, (pnl.x + 48, y + 22), 24, 2)
            mt = self.f_md.render(medals[i], True, BLACK)
            s.blit(mt, mt.get_rect(center=(pnl.x + 48, y + 22)))
            s.blit(self.f_lg.render(p.nome, True, p.cor), (pnl.x + 85, y + 3))
            if p.tribo:
                s.blit(self.f_sm.render(f"Tribo: {p.tribo.nome}", True, p.tribo.cor), (pnl.x + 85, y + 32))
            pt = self.f_xl.render(str(p.glorias), True, GOLD)
            s.blit(pt, (pnl.x + 420, y + 2))
            s.blit(self.f_sm.render("pts", True, GRAY), (pnl.x + 420 + pt.get_width() + 5, y + 18))
        winner = ranking[0]
        wt = self.f_xl.render(f"{winner.nome} VENCEU!", True, winner.cor)
        s.blit(wt, wt.get_rect(center=(SCREEN_W // 2, 580)))
        ft = self.f_md.render("R = jogar novamente | ESC = sair", True, GRAY)
        s.blit(ft, ft.get_rect(center=(SCREEN_W // 2, 625)))