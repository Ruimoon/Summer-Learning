import pygame  # 导入 pygame
from game_items import *  # 导入游戏袁术模块


class Game(object):
    def __init__(self):
        self.main_window = pygame.display.set_mode((640, 480))  # 窗口创建 (宽, 高)
        pygame.display.set_caption('贪吃蛇')  # 标题创建

        self.score_label = Lable()  # 得分的标签创建

        self.snake = Snake()  # 绘制贪吃蛇

        self.food = Food(self.snake.body_list)  # 食物的创建

        self.tip_lable = Lable(24, False)  # 暂停|游戏结束 的标签

        self.is_game_over = False  # 游戏是否结束的标记，如果为True则游戏结束
        self.is_pause = False  # 游戏是否暂停的标记，如果为True则说明游戏已经被暂停
        # print(self.snake.body_list)

    def start(self):
        """
        启动并控制游戏
        """
        clock = pygame.time.Clock()  # 游戏时钟

        while True:
            # 事件监听
            for event in pygame.event.get():  # 遍历同一时刻发生的事件列表
                if event.type == pygame.QUIT:  # 判断退出事件
                    print('点击了关闭按键')
                    return

                elif event.type == pygame.KEYDOWN:  # 判断按键事件
                    if event.key == pygame.K_ESCAPE:
                        print('按下了ESC键')
                        return

                    elif event.key == pygame.K_SPACE:
                        if self.is_game_over:
                            self.reset_game()
                            print('游戏重新开始')
                        else:
                            self.is_pause = not self.is_pause
                            print('切换暂停状态')

                if not self.is_pause and not self.is_game_over:
                    # 只有当游戏没有暂停也没结束才需要处理
                    if event.type == FOOD_UPDATE_EVENT:
                        self.food.random_rect(self.snake.body_list)
                        print('新事件发生，需要更新食物')
                    elif event.type == SNAKE_UPDATE_EVENT:
                        # 移动蛇的位置
                        self.is_game_over = not self.snake.update()
                        print("蛇移动一次,当前程序运行时间" + str(pygame.time.get_ticks()))
                    elif event.type == pygame.KEYDOWN:
                        # 有键盘按键按下
                        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                            self.snake.change_dir(event.key)

            # 依次绘制游戏元素
            self.main_window.fill(BACKGROUND_COLOR)  # 设置窗口背景颜色
            self.score_label.draw(self.main_window, "得分：%d" % self.snake.score)  # 绘制得分
            self.food.draw(self.main_window)  # 绘制食物
            self.snake.draw(self.main_window)  # 绘制贪吃蛇
            self.coordinate()  # 绘制坐标系

            # 判断游戏状态，绘制 暂停|游戏结束 标签
            if self.is_game_over:
                self.tip_lable.draw(self.main_window, "游戏结束，按空格键继续新游戏...")
            elif self.is_pause:
                self.tip_lable.draw(self.main_window, "游戏暂停，按空格键继续...")
            else:
                if self.snake.has_eat(self.food):
                    self.food.random_rect(self.snake.body_list)

            # 更新显示,刷新背景颜色
            pygame.display.update()

            clock.tick(60)  # 刷新帧率

    def reset_game(self):
        """
        重置游戏参数
        """
        self.is_game_over = False
        self.is_pause = False

        self.snake.reset_snake()  # 重置蛇的数据
        self.food.random_rect(self.snake.body_list)  # 重置食物位置

    def coordinate(self):
        # 计算可用的行数和列数
        col = int(SCREEN_RECT.w / CELL_SIZE)
        row = int(SCREEN_RECT.h / CELL_SIZE)

        for i in range(col):
            pygame.draw.line(self.main_window, (200, 100, 20), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_RECT.h), 2)
        for j in range(row):
            pygame.draw.line(self.main_window, (200, 100, 20), (0, j * CELL_SIZE), (SCREEN_RECT.w, j * CELL_SIZE), 2)


if __name__ == '__main__':
    pygame.init()  # 初始化所有模块
    # 游戏代码
    Game().start()

    pygame.quit()  # 取消初始化所有模块
