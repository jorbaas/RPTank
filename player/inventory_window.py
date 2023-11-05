from camera import Window
import pygame
from tanks.bullets.bullet_types import all_ammo
from camera.buttons import Button
from camera.textBox import TextBox



class Inventory_window():
    def __init__(self, player, pos, size, name):


        self.player = player
        self.pos = pos
        self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.border_rect = pygame.rect.Rect(pos[0], pos[1], size[0], 15)
        self.name = name
        self.font_size = 13
        self.font = pygame.font.Font(None, 14)

        self.tab = 'parts'

        self.last_click_time = 0
        self.double_click_delay = 300

        self.active = False
        self.moving = False
        self.moving_item = False
        self.selected_item = None
        self.item_text_box = None
        self.highlighted_item = None

        self.first_mouse_pos = ()

        self.buttons = []
        self.ammo_images = []
        self.parts_images = []
        self.parts_rects = []
        self.slot_rects = []
        self.equip_rects = []


        self.slot_image = pygame.image.load('assets/item_slot.png').convert_alpha()
        self.create_tab_buttons()


        self.create_item_slot_rects()
        self.create_equip_slot_rects()

        self.create_parts_tab()
        self.create_ammo_tab()


    def create_tab_buttons(self):
        tab_names = ('parts', 'ammo', 'misc')
        x_offset = 0
        for name in tab_names:
            self.create_button((self.pos[0] + x_offset, self.pos[1] + 15), (50,30), name)
            x_offset += 50


    def create_ammo_tab(self):
        pos = (self.rect.x + 4, self.rect.y + 48)
        w = 4
        h = 7
        c = 0
        sc = 0  # slot rect counters
        c2 = 5  # for ammo slots
        spacing = 35

        for item in self.player.inventory.ammo:
            item = self.player.inventory.ammo[item][0]

            if item.type == 'ammo':
                if c < 7:
                    item.rect = self.slot_rects[sc].copy()
                    item.rect.center = self.slot_rects[sc].center
                    c += 1
                    sc += 1

        for item in self.player.tank.ammo_inventory.ammo:
            item = self.player.tank.ammo_inventory.ammo[item][0]



            item.rect = self.equip_rects[c2].copy()
            item.rect.center = self.equip_rects[c2].center
            c2 += 1


    def create_parts_tab(self):
        pos = (self.rect.x + 4, self.rect.y + 48)
        w = 4
        h = 7
        c = 0
        sc = 0 # slot rect counters
        c2 = 0 # for equip slots
        spacing = 35

        for item in self.player.inventory.items:
            item = self.player.inventory.items[item][0]

            if item.type in ['hull', 'turret', 'barrel', 'cannon', 'engine']:

                item.rect = self.slot_rects[sc].copy()
                item.rect.center = self.slot_rects[sc].center
                c += 1
                sc += 1

        for item in self.player.tank.equipped_parts:
            item.rect = self.equip_rects[c2].copy()
            item.rect.center = self.equip_rects[c2].center
            c2 += 1


    def create_item_slot_rects(self):

        pos = (self.rect.x + 20 , self.rect.y + 65)
        w = 4
        h = 7
        c = 0
        spacing = 35

        for i in range(w*h+7):
            if c < w:
                rect = self.slot_image.get_rect(center=pos)
                self.slot_rects.append(rect)
                pos = (pos[0] + spacing, pos[1])
                c += 1
            else:
                pos = (pos[0] - (spacing*w), pos[1] + spacing)
                c = 0


    def create_equip_slot_rects(self):
        pos = (self.rect.x + 188, self.rect.y + 97)
        w = 3
        h = 4
        c = 0
        c2 = 0
        spacing = 35

        for i in range(w * h):
            if c < h-c2:
                rect = self.slot_image.get_rect(center=pos)
                self.equip_rects.append(rect)
                pos = (pos[0], pos[1] + spacing)
                c += 1
            else:
                pos = (pos[0] + spacing, self.rect.y + 97 + (spacing * (c2+1)))
                c = 0
                c2 += 1


    def move_window(self, mouse_pos, mouse_click):
        if self.active:

            if self.border_rect.collidepoint(mouse_pos) and mouse_click[0] and not self.moving:
                self.first_mouse_pos = mouse_pos
                self.moving = True

            if self.border_rect.collidepoint(mouse_pos) and mouse_click[0] and self.moving:
                dx = self.first_mouse_pos[0] - mouse_pos[0]
                dy = self.first_mouse_pos[1] - mouse_pos[1]
                self.rect.x -= dx
                self.rect.y -= dy
                self.border_rect.x -= dx
                self.border_rect.y -= dy

                if self.buttons:
                    for button in self.buttons:
                        button.rect.x -= dx
                        button.rect.y -= dy

                for item in self.player.inventory.items:
                    item = self.player.inventory.items[item][0]
                    item.rect.x -= dx
                    item.rect.y -= dy

                for item in self.player.inventory.ammo:
                    item = self.player.inventory.ammo[item][0]
                    item.rect.x -= dx
                    item.rect.y -= dy

                for item in self.player.tank.ammo_inventory.ammo:
                    item = self.player.tank.ammo_inventory.ammo[item][0]
                    item.rect.x -= dx
                    item.rect.y -= dy

                for item in self.player.tank.equipped_parts:
                    item.rect.x -= dx
                    item.rect.y -= dy

                for slot in self.slot_rects:
                    slot.x -= dx
                    slot.y -= dy

                for slot in self.equip_rects:
                    slot.x -= dx
                    slot.y -= dy

            else:
                self.moving = False

    def create_button(self, pos, size, text):
        button = Button(pos, size, text)
        self.buttons.append(button)


    def press_button(self, mouse_pos, mouse_click):

        current_time = pygame.time.get_ticks()  # for dubble click
        if mouse_click[0] and self.active:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    self.tab = button.text
                    if button.text == 'ammo':
                        self.create_ammo_tab()


            # if current_time - self.last_click_time <= self.double_click_delay:
            #     # Perform the action for a double-click here
            #     # print("Double-click detected")
            # self.last_click_time = current_time

        self.move_item(mouse_pos, mouse_click)
        self.highlight_item(mouse_pos)


    def highlight_item(self, mouse_pos):

        if self.tab == 'parts':
            for item in self.player.inventory.items:
                item = self.player.inventory.items[item][0]

                if item.rect.collidepoint(mouse_pos):
                    self.item_text_box = TextBox(item.rect.topright, item.values)
                    self.item_text_box.active = True
                    self.highlighted_item = item
                    break

        if self.tab == 'ammo':
            for item in self.player.inventory.ammo:
                item = self.player.inventory.ammo[item][0]
                if item.rect.collidepoint(mouse_pos):
                    self.item_text_box = TextBox(item.rect.topright, item.values)
                    self.item_text_box.active = True
                    self.highlighted_item = item
                    break

        if self.highlighted_item != None and not self.highlighted_item.rect.collidepoint(mouse_pos):
                self.item_text_box.active = False
                self.highlighted_item = None

        for item in self.player.tank.equipped_parts:
            if item.rect.collidepoint(mouse_pos):
                self.item_text_box = TextBox(item.rect.topright, item.values)
                self.item_text_box.active = True
                self.highlighted_item = item
                break

        for item in self.player.tank.ammo_inventory.ammo:
            item = self.player.tank.ammo_inventory.ammo[item][0]
            if item.rect.collidepoint(mouse_pos):
                self.item_text_box = TextBox(item.rect.topright, item.values)
                self.item_text_box.active = True
                self.highlighted_item = item
                break

        if self.highlighted_item != None and not self.highlighted_item.rect.collidepoint(mouse_pos):
                self.item_text_box.active = False
                self.highlighted_item = None


    def move_item(self, mouse_pos, mouse_click):
        if self.tab == 'parts':
            if mouse_click[0]:
                for item in self.player.inventory.items:
                    item = self.player.inventory.items[item][0]
                    if item.rect.collidepoint(mouse_pos) and self.selected_item == None:
                        self.first_mouse_pos = mouse_pos
                        self.selected_item = item
                if self.selected_item != None:
                    if self.selected_item.rect.collidepoint(mouse_pos):
                            item = self.selected_item
                            dx = self.first_mouse_pos[0] - mouse_pos[0]
                            dy = self.first_mouse_pos[1] - mouse_pos[1]
                            item.rect.x -= dx
                            item.rect.y -= dy
                            self.first_mouse_pos = mouse_pos
            elif self.selected_item:
                self.equip_item(self.selected_item, mouse_pos)
                self.selected_item = None
                self.create_parts_tab()

        if self.tab == 'ammo':
            if mouse_click[0]:
                for item in self.player.inventory.ammo:
                    self.item_amount = self.player.inventory.ammo[item][1]
                    item = self.player.inventory.ammo[item][0]
                    if item.rect.collidepoint(mouse_pos) and self.selected_item == None:
                        self.first_mouse_pos = mouse_pos
                        self.selected_item = item
                if self.selected_item != None:
                    if self.selected_item.rect.collidepoint(mouse_pos):
                            item = self.selected_item
                            dx = self.first_mouse_pos[0] - mouse_pos[0]
                            dy = self.first_mouse_pos[1] - mouse_pos[1]
                            item.rect.x -= dx
                            item.rect.y -= dy
                            self.first_mouse_pos = mouse_pos
            elif self.selected_item:
                self.switch_ammo(self.selected_item, self.item_amount, mouse_pos)
                self.selected_item = None
                self.create_ammo_tab()

        for item in self.player.tank.ammo_inventory.ammo:
            amount = self.player.tank.ammo_inventory.ammo[item][1]
            item = self.player.tank.ammo_inventory.ammo[item][0]

            if item.rect.collidepoint(mouse_pos) and mouse_click[2]:
                self.player.tank.ammo_inventory.remove_item(item, amount=amount)
                self.player.inventory.add_item(item, amount=amount)
                self.create_ammo_tab()
                break


    def equip_item(self, item, mouse_pos):
        name = item.name
        type = item.type
        tank = self.player.tank

        if item.type == 'barrel' and self.equip_rects[0].collidepoint(mouse_pos):
            self.player.inventory.add_item_by_name(tank.barrel.name)
            self.player.inventory.remove_item(item)
            self.player.tank.switch_part(name, type)


        elif item.type == 'turret' and self.equip_rects[1].collidepoint(mouse_pos):
            self.player.inventory.add_item_by_name(tank.turret.name)
            self.player.inventory.remove_item(item)
            self.player.tank.switch_part(name, type)
            self.player.tank.turret.calculate_turret_offset(tank.rect, tank.hull.turret_offset, tank.angle)
            self.create_parts_tab()



        elif item.type == 'hull' and self.equip_rects[2].collidepoint(mouse_pos):
            self.player.inventory.add_item_by_name(tank.hull.name)
            self.player.inventory.remove_item(item)
            self.player.tank.switch_part(name, type)

        elif item.type == 'engine' and self.equip_rects[3].collidepoint(mouse_pos):
            self.player.inventory.add_item_by_name(tank.engine.name)
            self.player.inventory.remove_item(item)
            self.player.tank.switch_part(name, type)

        elif item.type == 'cannon' and self.equip_rects[4].collidepoint(mouse_pos):
            self.player.inventory.add_item_by_name(tank.cannon.name)
            self.player.inventory.remove_item(item)
            self.player.tank.switch_part(name, type)


    def switch_ammo(self, item, amount, mouse_pos):
        name = item.name
        tank_ammo = self.player.tank.ammo_inventory.ammo
        player_ammo = self.player.inventory.ammo
        c = 5 # counter for rect index
        n = 0


        for ammo in tank_ammo:
            ammo = tank_ammo[ammo]

            if self.equip_rects[c].collidepoint(mouse_pos) and name == ammo[0].name:
                # self.player.inventory.add_item(ammo[0], amount=ammo[1])
                self.player.inventory.remove_item(item, amount=amount)
                # self.player.tank.ammo_inventory.remove_item(ammo[0], amount=ammo[1])
                self.player.tank.ammo_inventory.add_item(item, amount=amount)
                self.player.tank.set_ammo_order()
                self.player.tank.reset_active_ammo()
                break
            elif self.equip_rects[c].collidepoint(mouse_pos) and name != ammo[0].name:
                self.player.inventory.remove_item(item, amount=amount)
                self.player.inventory.add_item(ammo[0], amount=ammo[1])

                self.player.tank.ammo_inventory.remove_item(ammo[0], amount=ammo[1])
                self.player.tank.ammo_inventory.add_item(item, amount=amount)
                self.player.tank.set_ammo_order()
                self.player.tank.reset_active_ammo()
                break
            c += 1

        for i in range(3):
            self.equip_rects[i+5].collidepoint(mouse_pos)
            self.player.inventory.remove_item(item, amount=amount)
            self.player.tank.ammo_inventory.add_item(item, amount=amount)
            self.player.tank.set_ammo_order()
            self.player.tank.reset_active_ammo()
            break



    def print_text(self,screen, text, pos):
        x = pos[0]
        y = pos[1]
        y_spacing = self.font_size
        text = text.split('\n')
        for line in text:
            line = self.font.render(line, True, 'black')
            screen.blit(line, (x,y))
            y += y_spacing

    def create_stat_box(self, screen):
        tank = self.player.tank
        text = (f'mass: {tank.mass}\n'
                f'accel.: {tank.acceleration}\n'
                f'max speed: {tank.engine.max_speed}'
                )
        self.print_text(screen, text, (self.rect.centerx + 100, self.rect.centery -50))


    def draw(self, screen):
        # window
        if self.active:
            # draw the inv window
            pygame.draw.rect(screen, 'grey', self.rect)
            pygame.draw.rect(screen, 'darkgrey', self.border_rect)

            for rect in self.slot_rects: # draw item slots
                screen.blit(self.slot_image, rect)

            for rect in self.equip_rects: # draw equip slots
                screen.blit(self.slot_image, rect)

            for button in self.buttons: # draw buttons
                button.draw(screen)

            for item in self.player.tank.equipped_parts: # draw equiped tank pats
                try:
                    screen.blit(item.image, item.rect)
                except:
                    pass

            for item in self.player.tank.ammo_inventory.ammo: # draw ammo
                amount = self.player.tank.ammo_inventory.ammo[item][1]
                item = self.player.tank.ammo_inventory.ammo[item][0]
                amount_render = self.font.render(str(amount), True, 'black')

                try:
                    screen.blit(item.image, item.rect)
                    screen.blit(amount_render, item.rect)
                except:
                    pass


            if self.tab == 'parts':
                for item in self.player.inventory.items:
                    item = self.player.inventory.items[item][0]

                    if item.type in ['hull', 'turret', 'barrel', 'cannon', 'engine']:

                        screen.blit(item.image, item.rect)


            if self.tab == 'ammo':
                for item in self.player.inventory.ammo:
                    amount = self.player.inventory.ammo[item][1]
                    item = self.player.inventory.ammo[item][0]


                    amount_render = self.font.render(str(amount), True, 'black')
                    if item.type == 'ammo':
                        screen.blit(item.image, item.rect)
                        screen.blit(amount_render, item.rect)


            if self.item_text_box != None:
                self.item_text_box.draw(screen)

            self.create_stat_box(screen)





