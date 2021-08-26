import pygame #导入pygame模块
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game): # ai_game是AlienInvasion实例的引用。
        """初始化飞船并设置其初始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() #屏幕矩形

        # 加载飞船图像并获取其外接矩形。
        self.image = pygame.image.load('images\\ship.bmp') #加载图像
        #加载图像后使用get_rect()获取相应surface的属性rect
        self.rect = self.image.get_rect()

        #处理rect对象时，可以设置相应rect对象的属性center,centerx
        #或centery；还有top、bottom、left或right
        #甚至是一些组合属性midbottom、midtop、midleft和midright
        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中存储小数值
        self.x = float(self.rect.x) #float()将变量转换为浮点数类型


        #移动标志
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 根据self.x更新rect对象
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
        #blit方法将一个图像绘制到另一个图像上

    def center_ship(self):
        """让飞船在屏幕底端居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)