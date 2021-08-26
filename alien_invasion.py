# 导入模块sys和pygame
import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 初始化背景设置
        self.settings = Settings()
        # 创建一个显示窗口，实参是一个元组(1200, 800),指定了游戏窗口的尺寸：宽1200,高800
        # 赋给属性screen的对象是一个surface。
        # self.screen = pygame.display.set_mode(
        #    (self.settings.screen_width,
        #      self.settings.screen_height))

        # 全屏模式
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # 设置当前窗口的标题栏
        pygame.display.set_caption("Alien Invasion")

        #创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)

        # 创建记分牌。
        self.sb = ScoreBoard(self)

        # 设置背景色 以RGB值指定的
        self.bg_color = (self.settings.bg_color)

        self.ship = Ship(self)

        #创建存储子弹的编组
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建play按钮
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件。
            self._check_evnets()
            if self.stats.game_active:

                self.ship.update()

                self._update_bullets()

                self._update_aliens()

            # 每次循环时都重绘屏幕。
            self._update_screen()

    def _check_evnets(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            # pygame.event.get()这个函数返回一个列表，其中包含它
            # 在上次被调用后发生的所有事件
            if event.type == pygame.QUIT:
                sys.exit()  # 退出游戏
            elif event.type == pygame.KEYDOWN:  # 按下键
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 松开键
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #获取鼠标光标的位置，返回一个元组，包含x、y坐标
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:  # 右键
            # 向右移动飞船。
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:  # 右键
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """玩家单机Play按钮时开始新游戏。"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #检查鼠标单机位置是否在Play按钮的rect内
        if button_clicked and not self.stats.game_active:
            #重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            #隐藏鼠标光标。
            pygame.mouse.set_visible(False)

            #重置游戏设置
            self.settings.initialize_dynamic_settings()

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _fire_bullet(self):
        """创建一个子弹，并将其加入编组bullets中。"""
        if len(self.bullets) <= self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""

        # 方法fill()用这种背景色填充屏幕。
        # 方法fill()用于处理surface，只接受一个实参：一种颜色。
        self.screen.fill(self.settings.bg_color)
        # 填充背景后，调用ship.blitme()将飞船绘制到屏幕上。
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # aliens绘制在哪个surface上
        self.aliens.draw(self.screen)

        #显示得分
        self.sb.show_score()

        #如果游戏处于非活动状态，就绘制Play按钮。
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _update_bullets(self):
        # 对编组调用update()时
        # 编组自动对其中的每个精灵调用update()
        # 因此代码行bullets.update()将为编组bullets中的每个子弹调用bullet.update()
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():  # copy()返回一个浅复制
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞。"""
        #删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并新创建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """创建外星人群。"""
        #创建一个外星人并计算一行可容纳多少个外星人
        #外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        #放置外星人的水平空间
        available_space_x = self.settings.screen_width - (2 * alien_width)
        #外星人个数
        number_aliens_x = available_space_x // (2 * alien_width)

        #计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并将其加入到当前行。
        alien = Alien(self)
        alien_width, alien.height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘，
        更新外星人群中所有外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船之间的碰撞
        #函数pygame.sprite.spritecollideany()接受两个实参：
        #一个精灵和一个编组。它检查编组是否有成员与精灵发生了碰撞，并在
        #找到与精灵发生碰撞的成员后停止遍历编组。如果没有发生碰撞，返回None
        if pygame.sprite.spritecollideany(self.ship,  self.aliens):
            self._ship_hit()

        #检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施。"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船被外星人撞到。"""
        if self.stats.ships_left > 0:
            #将ships_left减1
            self.stats.ships_left -= 1

            #更新记分牌
            self.sb.prep_ships()

            # 清空余下的外星人和子弹。
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端。"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #像飞船被撞一样处理。
                self._ship_hit()
                break

if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()
