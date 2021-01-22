import pygame
from Button import Button
from Constants import *


class Information():
    def __init__(self, item_name, money_score, info, free_slots=None):
        self.free_slots = free_slots
        self.got_space = True
        
        self.count = 1
        self.buy = False
        self.got_money = True
        
        self.item_name = item_name
        self.money_score = money_score
        self.info = info
        
        self.item_icon = pygame.image.load(self.info['image'])
        self.item_icon = pygame.transform.scale(self.item_icon, HIGH_QUALITY)
        
        # Для покупки
        x = PAD11 + PAD8 + HIGH_QUALITY[0] + PAD10 * 2 + PAD9
        y = PAD11 + PAD8 + HIGH_QUALITY[1] + PAD10 * 2 + PAD9
        w = SIZE[0] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[0] - PAD9
        h = SIZE[1] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[1] - PAD9
        
        self.buttons = [Button('X', TEXT_COLOR, CLOSE_BUTTON, FONT,
                               SIZE[0] - PAD11 - CLOSE_BUTTON,
                               PAD11 - CLOSE_BUTTON,
                               CLOSE_BUTTON, CLOSE_BUTTON,
                               (CLOSE_COLOR1, CLOSE_COLOR2, CLOSE_COLOR3), True),
                        Button('Купить', TEXT_COLOR, TEXT_SIZE, FONT,
                               x + w / 2 + PAD10, y + h / 3 + PAD10,
                               w / 2 - PAD10 * 2, h * 2 / 3 - PAD10 * 2,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4), True),
                        Button('<', TEXT_COLOR, TEXT_SIZE, FONT,
                               x + PAD10, y + h / 3 + PAD10,
                               w / 2 / 5 - PAD10, h / 3 - PAD10,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4)),
                        Button('>', TEXT_COLOR, TEXT_SIZE, FONT,
                               x + w / 2 / 5 * 4 + PAD10, y + h / 3 + PAD10,
                               w / 2 / 5 - PAD10, h / 3 - PAD10,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4))]
    
    def drawing(self, screen):
        for button in self.buttons:
            button.block(False)
            
        if self.count == 1:
            self.buttons[2].block(True)
        if self.count == self.money_score // self.info['cost']:
            self.buttons[3].block(True)
            
        if self.money_score < self.info['cost']:
            self.got_money = False
            self.buttons[1].block(True)
            self.buttons[2].block(True)
            self.buttons[3].block(True)
        elif (self.free_slots or self.free_slots == 0) and self.count > self.free_slots:
            self.got_space = False
            self.buttons[1].block(True)
            self.buttons[3].block(True)
        elif self.money_score // self.info['cost'] > self.count > 1:
            self.got_space = True
        else:
            self.got_space = True
        
        # Верхняя панель
        pygame.draw.rect(screen, CLOSE_PANEL_COLOR, (PAD11, PAD11 - CLOSE_BUTTON,
                                                     SIZE[0] - PAD11 * 2,
                                                     CLOSE_BUTTON))
        window = pygame.font.SysFont(FONT, int(CLOSE_BUTTON - PAD10)).render('Оборудование и снаряжение', True, TEXT_COLOR)
        screen.blit(window, (PAD11 + PAD10,
                             PAD11 - CLOSE_BUTTON + window.get_height() / 2))
        # Окно
        pygame.draw.rect(screen, INFO_COLOR, (PAD11, PAD11,
                                              SIZE[0] - PAD11 * 2,
                                              SIZE[1] - PAD11 * 2))
        # Картинка
        pygame.draw.rect(screen, PANEL_COLOR, (PAD11 + PAD8, PAD11 + PAD8,
                                              HIGH_QUALITY[0] + PAD10 * 2,
                                              HIGH_QUALITY[1] + PAD10 * 2))
        screen.blit(self.item_icon, (PAD11 + PAD8 + PAD10, PAD11 + PAD8 + PAD10))
        # Значения
        pygame.draw.rect(screen, PANEL_COLOR, (PAD11 + PAD8,
                                               PAD11 + PAD8 + HIGH_QUALITY[1] + PAD10 * 2 + PAD9,
                                               HIGH_QUALITY[0] + PAD10 * 2,
                                               SIZE[1] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[1] - PAD9))
        line = 0
        for value in list(self.info['specifications'].keys()):
            line += 1
            values = pygame.font.SysFont(FONT, int((HIGH_QUALITY[0]) / 15)).render(value + ': ' + self.info['specifications'][value], True, TEXT_COLOR)
            screen.blit(values, (PAD11 + PAD8 + PAD10 * 2,
                                 PAD11 + PAD8 + HIGH_QUALITY[1] + PAD9 + PAD10 + line * (values.get_height() + BETWEEN)))
        # Описание
        x = PAD11 + PAD8 + HIGH_QUALITY[0] + PAD10 * 2 + PAD9
        y = PAD11 + PAD8
        w = SIZE[0] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[0] - PAD9
        h = HIGH_QUALITY[1] + PAD10 * 2
        pygame.draw.rect(screen, DESCR_COLOR, (x, y, w, h))
        
        line1 = 0
        text = ' ' * INDENT
        test = ''
        for i in self.info['name'].split():
            test = text
            test += (i + ' ')
            name = pygame.font.SysFont(FONT, int(TEXT_SIZE)).render(test, True, TEXT_COLOR)
            if name.get_width() > w - PAD10 * 3:
                name = pygame.font.SysFont(FONT, int(TEXT_SIZE)).render(text, True, TEXT_COLOR)
                screen.blit(name, (x + PAD10 * 2, y + PAD10 * 2 + TEXT_SIZE * line1))
                text = i + ' '
                line1 += 1
            else:
                text = test
        name = pygame.font.SysFont(FONT, int(TEXT_SIZE)).render(test, True, TEXT_COLOR)
        screen.blit(name, (x + PAD10 * 2, y + PAD10 * 2 + TEXT_SIZE * line1))
        
        line2 = 0
        text = ''
        test = ''
        par_num_orig = 0
        for paragraph in self.info['description']:
            par_num = 0
            text = ' ' * INDENT
            for i in paragraph.split():
                test = text
                test += (i + ' ')
                name = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render(test, True, TEXT_COLOR)
                if name.get_width() > w - PAD10 * 3:
                    name = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render(text, True, TEXT_COLOR)
                    screen.blit(name, (x + PAD10 * 2,
                                       y + PAD10 * 7 + TEXT_SIZE * (line1 + line2) + par_num_orig))
                    par_num += name.get_height()
                    text = i + ' '
                    line2 += 1
                else:
                    text = test
            name = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render(test, True, TEXT_COLOR)
            screen.blit(name, (x + PAD10 * 2, 
                               y + PAD10 * 7 + TEXT_SIZE * (line1 + line2) + par_num_orig))
            line2 += 1
            par_num_orig = par_num
        # Покупка
        x = PAD11 + PAD8 + HIGH_QUALITY[0] + PAD10 * 2 + PAD9
        y = PAD11 + PAD8 + HIGH_QUALITY[1] + PAD10 * 2 + PAD9
        w = SIZE[0] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[0] - PAD9
        h = SIZE[1] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[1] - PAD9
        pygame.draw.rect(screen, PANEL_COLOR, (x, y, w, h))
        pygame.draw.rect(screen, BUY_COLOR1, (x + PAD10, y + PAD10,
                                             w - PAD10 * 2,
                                             h / 3 - PAD10))
        cost1 = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render('Цена', True, TEXT_COLOR)
        screen.blit(cost1, (x + PAD10 * 2,
                            (y + h / 5) - cost1.get_height() / 2))
        cost2 = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render(str(self.info['cost']) + '$', True, TEXT_COLOR)
        screen.blit(cost2, (x + w - cost2.get_width() - PAD10 * 2,
                            (y + h / 5) - cost2.get_height() / 2))
        if self.got_money:
            pygame.draw.rect(screen, BUY_COLOR1, (x + w / 10 + PAD10,
                                                 y + h / 3 + PAD10,
                                                 w / 10 * 3 - PAD10,
                                                 h / 3 - PAD10))
            buy = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render(str(self.count), True, TEXT_COLOR)
            screen.blit(buy, ((x + w / 4 + PAD10 / 2) - buy.get_width() / 2,
                              (y + h / 2 + PAD10 / 2) - buy.get_height() / 2))        
            
            pygame.draw.rect(screen, BUY_COLOR1, (x + PAD10, y + h * 2 / 3 + PAD10,
                                                 w / 2 - PAD10,
                                                 h / 3 - PAD10 * 2))        
            money = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render(str(self.info['cost'] * self.count) + '$', True, TEXT_COLOR) # + ' (-' + str(self.info['cost'] * self.count) + '$)'
            screen.blit(money, ((x + w / 4) - money.get_width() / 2,
                                (y + h / 6 * 5) - money.get_height() / 2))
            
            if self.got_space or not (self.free_slots or self.free_slots == 0):               
                for button in self.buttons:
                    button.drawing(screen)
            else:
                pygame.draw.rect(screen, BUY_COLOR4, (x + w / 2 + PAD10,
                                                      y + h / 3 + PAD10,
                                                      w / 2 - PAD10 * 2,
                                                      h * 2 / 3 - PAD10 * 2))
                no_space = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render('Недостаточно места', True, TEXT_COLOR)
                screen.blit(no_space, ((x + w / 4 * 3) - no_space.get_width() / 2,
                                       (y + h / 3 * 2) - no_space.get_height() / 2))
                self.buttons[0].drawing(screen)
                self.buttons[2].drawing(screen)
                self.buttons[3].drawing(screen)
        else:
            no_money = pygame.font.SysFont(FONT, int(h / 3 - PAD10)).render('Недостаточно средств', True, TEXT_COLOR)
            screen.blit(no_money, ((x + w / 2) - no_money.get_width() / 2,
                                   (y + h / 3 * 2) - no_money.get_height() / 2))
            self.buttons[0].drawing(screen)
    
    def controller(self, event, screen):
        if self.buttons[0].down:
            return False
        elif self.buttons[1].down:
            self.buy = True
            return False
        elif self.buttons[2].down and self.count > 1:
            self.buttons[2].down = False
            self.count -= 1
        elif self.buttons[3].down and self.count < self.money_score // self.info['cost']:
            self.buttons[3].down = False
            self.count += 1
        
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                if button.on_button(event.pos):
                    button.selected(True)
                else:
                    button.selected(False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.on_button(event.pos):
                    button.pressed(True)
                else:
                    button.pressed(False)
        return True
