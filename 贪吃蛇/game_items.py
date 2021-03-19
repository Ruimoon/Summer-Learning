import random

import pygame  # 导入 pygame

# 全局变量定义
BACKGROUND_COLOR = (232, 232, 232)  # 窗口背景色
SCORE_TEXT_COLOR = (192, 192, 192)  # 分数文字颜色
TIP_TEXT_COLOR = (64, 64, 64)  # 提示文字颜色
SCREEN_RECT = pygame.Rect(0, 0, 640, 480)  # 窗口的大小
CELL_SIZE = 20  # 每个格子的宽高
FOOD_UPDATE_EVENT = pygame.USEREVENT  # 食物更新事件标志
SNAKE_UPDATE_EVENT = pygame.USEREVENT + 1  # 蛇更新事件标准


class Lable(object):
    """
    标签文本类
    """

    def __init__(self, size=48, is_score=True):
        """
        初始化标签信息
        :param size :字体大小
        :param is_score : 是否是显示得分的对象
        """
        self.font = pygame.font.SysFont("simhei", size)  # 黑体字
        self.is_score = is_score

    def draw(self, window, text):
        """
        绘制当前对象的内容
        """
        # 渲染字体
        color = SCORE_TEXT_COLOR if self.is_score else TIP_TEXT_COLOR
        text_surface = self.font.render(text, True, color)

        # 获取文本的矩形
        text_rect = text_surface.get_rect()
        # print('文字的矩形', text_rect)  # 宽高可能每个人不一样，按照自己的宽写

        # 获取窗口的矩形
        window_rect = window.get_rect()

        # 修改显示的坐标
        if self.is_score:
            # 游戏得分，显示在窗口左下角
            # text_rect.y = window_rect.height - text_rect.height
            text_rect.bottomleft = window_rect.bottomleft
        else:
            # 提示信息，暂停|游戏结束，显示在窗口中间
            text_rect.center = window_rect.center

        # 绘制文本内容到窗口
        window.blit(text_surface, text_rect)


class Food(object):
    """
    食物类
    """

    def __init__(self, body_list):
        """
        初始化食物
        """
        self.color = (100, 50, 100)  # 食物颜色
        self.score = 1  # 默认一颗食物的得分
        self.rect = (0, 0, CELL_SIZE, CELL_SIZE)  # 初始的显示位置
        self.random_rect(body_list)  # 随机分配位置

    def draw(self, window):
        """
        使用当前食物的矩形，绘制实心图形
        """
        if self.rect.w < CELL_SIZE:  # 只要显示的矩形小于单元格大小，就继续放大
            self.rect.inflate_ip(2, 2)  # 向周围放大一个像素

        pygame.draw.ellipse(window, self.color, self.rect)

    def random_rect(self, body_list):
        """
        随机确定绘制食物的位置
        """
        # 计算可用的行数和列数
        col = SCREEN_RECT.w / CELL_SIZE - 1  # 列
        row = SCREEN_RECT.h / CELL_SIZE - 1  # 行

        # 随机分配一个行和列，并计算行和列的x, y值
        x = random.randint(1, col-1) * CELL_SIZE
        y = random.randint(1, row-1) * CELL_SIZE

        # 重新生成绘制食物的矩形
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        while self.rect in body_list:
            x = random.randint(1, col-1) * CELL_SIZE
            y = random.randint(1, row-1) * CELL_SIZE
            self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        self.rect.inflate_ip(-CELL_SIZE, -CELL_SIZE)  # 把创建好的矩形大小修改为0,食物初始不可见

        # 设置定时，时间到了之后要重新设置食物位置
        pygame.time.set_timer(FOOD_UPDATE_EVENT, 30000)  # 3秒


class Snake(object):
    """
    蛇类
    """

    def __init__(self):
        """
        初始化蛇的数据
        """
        self.dir = pygame.K_RIGHT  # 运动方向
        self.time_interval = 500  # 运动事件间隔
        self.score = 0  # 游戏得分
        self.color = (64, 64, 64)  # 身体颜色-深灰色
        self.body_list = []  # 身体列表

        self.reset_snake()
        self.update()

    def reset_snake(self):
        """
        重置蛇的数据
        """
        self.dir = pygame.K_RIGHT
        self.time_interval = 500
        self.score = 0
        self.body_list.clear()  # self.body_list = [] 清空身体列表

        for i in range(3):  # 添加三节身体
            self.add_node()

    def add_node(self):
        """
        在蛇的运动方向上，添加一节身体
        """
        # 1、判断是否有身体
        if self.body_list:  # 已经有身体了
            head = self.body_list[0].copy()  # 生成新的矩形对象
        else:  # 还没有身体
            head = pygame.Rect(-CELL_SIZE * 2, 0, CELL_SIZE, CELL_SIZE)

        # 2.根据运动方向，调整head的位置
        # 根据移动方向，把新生成的头部放到恰当的位置
        if self.dir == pygame.K_RIGHT:
            head.x += CELL_SIZE
        elif self.dir == pygame.K_LEFT:
            head.x -= CELL_SIZE
        elif self.dir == pygame.K_UP:
            head.y -= CELL_SIZE
        elif self.dir == pygame.K_DOWN:
            head.y += CELL_SIZE

        # 3、将蛇头插入到身体列表第0项
        # 把新生成的头部放到列表的最前面
        self.body_list.insert(0, head)

    def draw(self, window):
        """
        遍历绘制每一节身体
        """
        for idx, rect in enumerate(self.body_list):
            pygame.draw.rect(window, self.color, rect.inflate(-2, -2), idx == 0)
            # 不改变原rect缩小矩形区域，==判断语句，成立取True蛇头绘制边框不填充

    def update(self):
        """
        移动蛇的身体
        """
        # 备份移动之前的身体列表
        body_list_copy = self.body_list.copy()

        self.add_node()
        self.body_list.pop()

        # 定时更新身体
        pygame.time.set_timer(SNAKE_UPDATE_EVENT, self.time_interval)

        # 判断是否死亡
        if self.is_dead():
            self.body_list = body_list_copy
            return False

        return True

    def change_dir(self, to_dir):
        """
        改变贪吃蛇的运动方向

        :param to_dir: 要变化的方向
        """
        hor_dirs = (pygame.K_RIGHT, pygame.K_LEFT)  # 水平方向
        ver_dirs = (pygame.K_UP, pygame.K_DOWN)  # 垂直方向

        # 判断当前运动方向及要修改的方向
        if ((self.dir in hor_dirs and to_dir not in hor_dirs) or
                (self.dir in ver_dirs and to_dir not in ver_dirs)):
            self.dir = to_dir

    def has_eat(self, food):
        """
        判断蛇头是否与食物相遇==吃到食物
        :param food: 食物对象
        :return: 是否吃到食物
        """
        if self.body_list[0].contains(food.rect):  # 蛇头和食物已经重叠
            self.score += food.score  # 增加分数

            # 修改运动时间间隔
            if self.time_interval > 100:
                self.time_interval -= 50

            self.add_node()  # 增加一节身体

            return True

        return False

    def is_dead(self):
        """
        判断是否已经死亡，如果死亡则返回True
        """
        # 获取蛇头的矩形
        head = self.body_list[0]

        # 判断蛇头是否不在窗口里
        if not SCREEN_RECT.contains(head):
            return True

        # 判断蛇头是否与身体重叠
        for body in self.body_list[1:]:
            if head.contains(body):
                return True

        return False