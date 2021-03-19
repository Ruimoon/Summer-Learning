import pygame


def test():
    """
    简单测试
    """
    window = pygame.display.set_mode((640, 480))

    color = (255, 0, 0)  # 绘制使用的颜色
    rect = pygame.Rect(10, 10, 20, 20)  # 圆形和矩形显示范围
    point1 = (10, 100)  # 线条的一个点
    point2 = (200, 20)  # 线条的一个点
    point3 = (100, 200)  # 线条的一个点

    points = (point1, point2, point3)  # 绘制折线使用的点列表

    while True:

        pygame.draw.rect(window, color, rect)  # 绘制实心矩形
        # pygame.draw.rect(window, color, rect, 2)  # 绘制空心矩形
        # pygame.draw.ellipse(window, color, rect)  # 绘制实心圆形
        # pygame.draw.ellipse(window, color, rect, 2)  # 绘制圆圈
        # pygame.draw.line(window, color, point1, point2, 2)  # 直线
        # pygame.draw.lines(window, color, False, points, 2)  # 折线
        # pygame.draw.lines(window, color, True, points, 2)  # 闭合折线

        pygame.display.update()


if __name__ == "__main__":
    test()
