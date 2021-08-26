import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """初始化按钮的属性。"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        #pygame.font.SysFont从文件创建新字体对象
        #第一个参数是文字来自的文件，第二个参数是象素
        self.font = pygame.font.SysFont(None, 48)

        #创建按钮的rect对象，并使其居中。
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #按钮的标签只需创建一次。
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中。"""
        #在新的surface上绘制文本,函数还接受一个布尔参数，表示是否开启反锯齿功能
        self.msg_imag = self.font.render(msg, True, self.text_color,
                                         self.button_color)
        self.msg_imag_rect = self.msg_imag.get_rect()
        self.msg_imag_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本。
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_imag, self.msg_imag_rect)
        #screen.fill()用来绘制表示按钮的矩形
        #screen.blit()传递一幅图像以及与该图像相关联的rect，从而在屏幕上绘制文本图像

