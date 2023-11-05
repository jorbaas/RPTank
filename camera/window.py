import pygame
from .buttons import Button
from .textBox import TextBox

class Window():




    def create_button(self, pos, size, text):
        button = Button(pos, size, text)
        self.buttons.append(button)


    def press_button(self, mouse_pos, mouse_click):
        current_time = pygame.time.get_ticks()  # for dubble click
        if mouse_click[0]:
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
                break
            elif self.equip_rects[c].collidepoint(mouse_pos) and name != ammo[0].name:
                self.player.inventory.remove_item(item, amount=amount)
                self.player.inventory.add_item(ammo[0], amount=ammo[1])

                self.player.tank.ammo_inventory.remove_item(ammo[0], amount=ammo[1])
                self.player.tank.ammo_inventory.add_item(item, amount=amount)
                self.player.tank.set_ammo_order()
                break
            c += 1

        for i in range(3):
            self.equip_rects[i+5].collidepoint(mouse_pos)
            self.player.inventory.remove_item(item, amount=amount)
            self.player.tank.ammo_inventory.add_item(item, amount=amount)
            self.player.tank.set_ammo_order()
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


    def draw(self, screen):
        # window
        if self.active:
            pygame.draw.rect(screen, 'grey', self.rect)
            pygame.draw.rect(screen, 'darkgrey', self.border_rect)

        # status window
            if self.name == 'status':
                hull_image = pygame.transform.scale(self.tank.hull.original_image, (128, 128))
                turret_image = pygame.transform.scale(self.tank.turret.original_image, (128, 128))
                barrel_image = pygame.transform.scale(self.tank.barrel.original_image, (128, 128))
                screen.blit(hull_image, (self.rect.x + 100, self.rect.y + 100))
                screen.blit(turret_image, (self.rect.x + 100, self.rect.y + 100))
                screen.blit(barrel_image, (self.rect.x + 100, self.rect.y + 100))

                self.draw_text(screen)

                for button in self.buttons:
                    button.draw(screen)


        # inventory window
            elif self.name == 'inv':

                for rect in self.slot_rects:
                    screen.blit(self.slot_image, rect)

                for rect in self.equip_rects:
                    screen.blit(self.slot_image, rect)

                for button in self.buttons:
                    button.draw(screen)

                for item in self.player.tank.equipped_parts:
                    try:
                        screen.blit(item.image, item.rect)
                    except:
                        pass

                for item in self.player.tank.ammo_inventory.ammo:
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






