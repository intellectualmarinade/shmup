class Enemy1group():

    def __init__(self):

        self.enemy_list = None
        self.enemy_bullet_list = None
        self.startenemy1()

    def startenemy1(self):

        # Load the textures for the enemies
        self.enemy_textures = []
        texture1 = arcade.load_texture("./Assets/sprites/container/enemy01.png")
        self.enemy_textures.append(texture1)

        # Create rows and columns of enemies
        x_count = random.randrange(2, 10)
        x_start = random.randrange(0, 600)
        x_spacing = 50
        y_count = random.randrange(1, 2)
        y_start = 800
        y_spacing = random.randrange(1, 50)
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):
                enemy1 = arcade.Sprite()
                enemy1.scale = 1
                enemy1.texture = self.enemy_textures[0]

                # Position the enemy
                enemy1.center_x = x
                enemy1.center_y = y

                # Add the enemy to the lists
                self.enemy_list.append(enemy1)

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()

    def update_enemies(self):

        # Move the enemy vertically
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        for enemy in self.enemy_list:
            enemy.center_y += self.enemy_change_y

        # Check every enemy to see if any hit the edge. If so, reverse the
        # direction and flag to move down.
        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        # Did we hit the edge above, and need to move the enemy down?
        if move_down:
            # Yes
            for enemy1 in self.enemy_list:
                # Move enemy down
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT

        if enemy.top < 0:
            enemy.remove_from_sprite_lists()

    def allow_enemies_to_fire(self):
        """
        See if any enemies will fire this frame.
        """
        # Track which x values have had a chance to fire a bullet.
        # Since enemy list is build from the bottom up, we can use
        # this to only allow the bottom row to fire.
        x_spawn = []
        for enemy1 in self.enemy_list:
            # Adjust the chance depending on the number of enemies. Fewer
            # enemies, more likely to fire.
            chance = 4 + len(self.enemy_list) * 4

            # Fire if we roll a zero, and no one else in this column has had
            # a chance to fire.
            if len(self.enemy_bullet_list) < MAX_ENEMY_BULLETS:
                if random.randrange(chance) == 0 and enemy1.center_x not in x_spawn:
                    # Create a bullet
                    bullet = arcade.Sprite("./Assets/sprites/container/purp_bullet.png", SPRITE_SCALING_ENEMYLASER)

                    # bullet attributes
                    bullet.angle = 180
                    bullet.change_y = -BULLET_SPEED
                    bullet.center_x = enemy1.center_x
                    bullet.top = enemy1.bottom

                    # Add the bullet to the appropriate list
                    self.enemy_bullet_list.append(bullet)

            # Ok, this column has had a chance to fire. Add to list so we don't
            # try it again this frame.
            x_spawn.append(enemy1.center_x)

    def process_enemy_bullets(self):

        # Move the bullets
        self.enemy_bullet_list.update()

        # Loop through each bullet
        for bullet in self.enemy_bullet_list:
            arcade.check_for_collision_with_list(bullet, self.player_list)

            # See if the player got hit with a bullet
            if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list):
                self.game_state = GAME_OVER

            # If the bullet falls off the screen get rid of it
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()

        if len(self.enemy_list) == 0:
            self.startenemy1()
