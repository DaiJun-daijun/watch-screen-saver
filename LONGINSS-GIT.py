from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
import sys
import datetime
from zhdate import ZhDate


class Longinss_Phase(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Longinss")
        self.showFullScreen()

        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(10, 25, 45))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # 设置字体
        self.font_main = QFont("New", 6, QFont.Bold)  # 主表盘数字
        self.font_main.setStretch(150)
        self.font_brand = QFont("New", 7, QFont.Bold)
        self.font_brand.setStretch(130)
        self.font_city = QFont("Arial", 3.8)
        self.font_swiss_made = QFont("Arial", 3)
        self.font_date = QFont("Arial", 3)
        self.font_instruction = QFont("Arial", 16)

        # 计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

        # 指针路径（保持不变）
        self.hour_hand_path = QPainterPath()
        self.hour_hand_path.moveTo(0, -95)
        self.hour_hand_path.cubicTo(1, -45, 7, -35, 0, 0)
        self.hour_hand_path.lineTo(-0, 0)
        self.hour_hand_path.cubicTo(-7, -35, -1, -45, 0, -95)

        self.minute_hand_path = QPainterPath()
        self.minute_hand_path.moveTo(0, -135)
        self.minute_hand_path.cubicTo(1, -95, 5.5, -50, 0, 0)
        self.minute_hand_path.lineTo(-0, 0)
        self.minute_hand_path.cubicTo(-5.5, -50, -1, -95, 0, -135)

        self.second_hand_path = QPainterPath()
        self.second_hand_path.moveTo(0, -138)
        self.second_hand_path.lineTo(1.1, 20)
        self.second_hand_path.lineTo(0, 24.5)
        self.second_hand_path.lineTo(-1.1, 20)
        self.second_hand_path.closeSubpath()

        self.date_hand_path = QPainterPath()
        self.date_hand_path.moveTo(0, -45)
        self.date_hand_path.cubicTo(0.6, -25, 3, -15, 0, 0)
        self.date_hand_path.lineTo(-0, 0)
        self.date_hand_path.cubicTo(-3, -15, -0.6, -25, 0, -45)

        # 颜色定义
        self.hand_color = QColor(255, 255, 255)
        self.hand_outline_color = QColor(235, 235, 235)
        self.logo_color = QColor(235, 235, 235)
        self.mark_color = QColor(255, 255, 255)
        self.black_color = QColor(0, 0, 0)
        self.text_color = QColor(255, 255, 255)
        self.date_color = QColor(255, 255, 255)
        self.dot_color = QColor(200, 200, 200)
        self.moon_color = QColor(180, 160, 25)
        self.bc_color = QColor(10, 25, 45)
        self.instruction_color = QColor(250, 250, 250, 200)
        self.subdial_blue = QColor(20, 35, 60)

        # 秒针中心圆点
        self.second_hand1_dot_radius = 3
        self.second_hand1_dot_color = QColor(255, 255, 255)
        self.second_hand2_dot_radius = 2.5
        self.second_hand2_dot_color = QColor(10, 25, 45)
        self.second_hand3_dot_radius = 2
        self.second_hand3_dot_color = QColor(255, 255, 255)

        # 针轴美化
        self.but1_dot_radius = 3.5
        self.but1_dot_color = QColor(10, 25, 45)
        self.but2_dot_radius = 3.3
        self.but2_dot_color = QColor(255, 255, 255)
        self.but3_dot_radius = 1.5
        self.but3_dot_color = QColor(10, 25, 45)
        self.but4_dot_radius = 1
        self.but4_dot_color = QColor(255, 255, 255)

        # 月相参数
        lunar_date = ZhDate.today()
        lunar_day = lunar_date.lunar_day
        self.moon_phase_angle = 6.1 * lunar_day
        self.large_dot_radius = 15.5
        self.small_star_size = 1.0
        self.medium_star_size = 1.5
        self.dot1_distance = 22
        self.dot2_distance = 13
        self.dot3_distance = 30
        self.dot4_distance = 8

        # 半圆参数
        self.small_semi_circle_radius = 17
        self.large_semi_circle_radius = 39
        self.semi_circle_y_offset = 60

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.moon_phase_angle += 6.2
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.HighQualityAntialiasing
        )

        min_size = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(min_size / 300, min_size / 300)

        time = QTime.currentTime()
        date = datetime.datetime.now().day

        self.draw_main_dial(painter)
        self.draw_brand_text(painter)
        self.draw_date_dial(painter, date)
        self.draw_moon_phase_dots(painter)
        self.draw_semi_circles(painter)

        # ⭐ 这里调用新的标志（五角星），不再是飞翼沙漏
        self.draw_custom_logo(painter)   # 替换了原来的 draw_winged_sandglass

        # 重新绘制 "AUTOMATIC" 等文字
        painter.setPen(self.text_color)
        painter.setFont(self.font_city)
        painter.drawText(QRectF(-50, 71, 100, 20), Qt.AlignCenter, "AUTOMATIC")
        painter.setFont(self.font_swiss_made)
        angle = 12
        painter.rotate(angle)
        painter.drawText(QRectF(-35, 120, 80, 20), Qt.AlignCenter, "SWISS")
        angle = -24
        painter.rotate(angle)
        painter.drawText(QRectF(-46, 120, 80, 20), Qt.AlignCenter, "MADE")
        angle = 12
        painter.rotate(angle)

        self.draw_date_hand_top_layer(painter, date)
        self.draw_hour_hand(painter, time)
        self.draw_minute_hand(painter, time)
        self.draw_center(painter)
        self.draw_second_hand(painter, time)
        self.draw_instruction(painter)

    def draw_custom_logo(self, painter):
        """绘制自定义标志（五角星），位置在12点，取代飞翼沙漏"""
        painter.save()
        # 使用银色
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.logo_color)

        # 利用已有的 draw_star 方法，在12点位置画一个稍大的五角星
        # 位置大约在 (0, -55)，大小 8
        self.draw_star(painter, 0, -55, 8)

        # 可以再加一个小圆点点缀
        painter.setBrush(QColor(255, 215, 0))  # 金色小点
        painter.drawEllipse(QPointF(0, -55), 1.5, 1.5)

        painter.restore()

    def draw_instruction(self, painter):
        painter.save()
        painter.resetTransform()
        painter.setPen(self.instruction_color)
        painter.setFont(self.font_instruction)
        text = "SPACE | ADJUST MOON PHASE"
        text_rect = QRectF(self.width() - 620, self.height() - 45, 600, 30)
        painter.drawText(text_rect, Qt.AlignRight | Qt.AlignVCenter, text)
        painter.restore()

    def draw_semi_circles(self, painter):
        painter.save()
        painter.translate(0, self.semi_circle_y_offset)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.bc_color)
        painter.translate(0, +2)
        for i in [-1, 1]:
            x_offset = i * (self.small_semi_circle_radius + 5.5)
            path = QPainterPath()
            path.moveTo(x_offset, 0)
            path.arcTo(x_offset - self.small_semi_circle_radius, -self.small_semi_circle_radius,
                       self.small_semi_circle_radius * 2, self.small_semi_circle_radius * 2,
                       0, 180)
            painter.drawPath(path)
        painter.translate(0, -2)
        path = QPainterPath()
        path.moveTo(0, 1)
        path.arcTo(-self.large_semi_circle_radius, -37,
                   self.large_semi_circle_radius * 2, self.large_semi_circle_radius * 2,
                   180, 180)
        painter.drawPath(path)
        painter.restore()

    def draw_date_hand_top_layer(self, painter, date):
        painter.save()
        painter.translate(0, 61)
        date_angle = 360 * (date - 1) / 31
        painter.rotate(date_angle)
        outline_pen = QPen(self.hand_outline_color, 0.8)
        painter.setPen(outline_pen)
        painter.setBrush(self.hand_color)
        painter.drawPath(self.date_hand_path)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.but1_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but1_dot_radius, self.but1_dot_radius)
        painter.setBrush(self.but2_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but2_dot_radius, self.but2_dot_radius)
        painter.setBrush(self.but3_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but3_dot_radius, self.but3_dot_radius)
        painter.setBrush(self.but4_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but4_dot_radius, self.but4_dot_radius)
        painter.restore()

    def draw_star(self, painter, x, y, size):
        """绘制实心五角星（顶点朝上）"""
        star = QPainterPath()
        for i in range(5):
            angle_rad = radians(18 + i * 72)
            outer_radius = size
            inner_radius = size * 0.4
            outer_x = x + outer_radius * sin(angle_rad)
            outer_y = y - outer_radius * cos(angle_rad)
            inner_x = x + inner_radius * sin(radians(18 + i * 72 + 36))
            inner_y = y - inner_radius * cos(radians(18 + i * 72 + 36))
            if i == 0:
                star.moveTo(outer_x, outer_y)
            else:
                star.lineTo(outer_x, outer_y)
            star.lineTo(inner_x, inner_y)
        star.closeSubpath()
        painter.drawPath(star)

    def draw_moon_phase_dots(self, painter):
        painter.save()
        painter.translate(0, 60)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.moon_color)
        painter.rotate(self.moon_phase_angle)
        # 大圆点
        painter.drawEllipse(QPointF(self.dot1_distance, 0),
                            self.large_dot_radius, self.large_dot_radius)
        painter.drawEllipse(QPointF(-self.dot1_distance, 0),
                            self.large_dot_radius, self.large_dot_radius)
        # 小五角星
        small_dot_angles = [65, 110]
        for angle in small_dot_angles:
            x = self.dot2_distance * cos(radians(angle)) + 2
            y = -self.dot2_distance * sin(radians(angle)) + 1
            self.draw_star(painter, x, y, self.small_star_size)
            self.draw_star(painter, -x, -y, self.small_star_size)
        # 中五角星
        medium_dot_angles = [50, 75, 90, 125]
        medium_distances = [self.dot3_distance - 0, self.dot3_distance - 10,
                            self.dot3_distance + 0, self.dot3_distance - 5]
        for i, angle in enumerate(medium_dot_angles):
            distance = medium_distances[i % len(medium_distances)]
            x = distance * cos(radians(angle))
            y = -distance * sin(radians(angle))
            self.draw_star(painter, x, y, self.medium_star_size)
            self.draw_star(painter, -x, -y, self.medium_star_size)
        painter.restore()

    def draw_main_dial(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.subdial_blue)
        painter.drawEllipse(QPointF(0, 61), 39, 39)
        for i in range(12):
            if i == 0:
                thick_pen1 = QPen(self.mark_color, 3.8)
                painter.setPen(thick_pen1)
                painter.drawLine(0, -104, 0, -133)
                normal_pen = QPen(self.mark_color, 2)
                painter.setPen(normal_pen)
            elif i == 6:
                painter.drawLine(0, -118, 0, -133)
            else:
                painter.drawLine(0, -104, 0, -133)
            painter.rotate(30)
        for i in range(60):
            if i % 5 != 0:
                thick_pen2 = QPen(self.mark_color, 0.9)
                painter.setPen(thick_pen2)
                painter.drawLine(0, -140, 0, -146.5)
            painter.rotate(6)
        painter.setFont(self.font_main)
        painter.setPen(self.text_color)
        radius = 143
        for i in range(12):
            angle = -30 * i - 30
            x = -radius * sin(radians(angle))
            y = -radius * cos(radians(angle))
            painter.save()
            painter.translate(x, y)
            painter.rotate(-angle)
            painter.drawText(QRectF(-15, -15, 30, 31), Qt.AlignCenter, str(5 * i + 5))
            painter.restore()
        painter.restore()

    def draw_brand_text(self, painter):
        painter.save()
        painter.setPen(self.text_color)
        painter.setFont(self.font_brand)
        text = "LONGINSS"
        total_width = 0
        letter_spacing = -1.5
        for letter in text:
            total_width += painter.fontMetrics().width(letter) + letter_spacing
        total_width -= letter_spacing
        x_start = -total_width / 2
        x = x_start
        for letter in text:
            painter.drawText(QPointF(x, -62), letter)
            x += painter.fontMetrics().width(letter) + letter_spacing
        painter.restore()

    def draw_date_dial(self, painter, date):
        painter.save()
        painter.translate(0, 61)
        outer_radius = 50
        inner_radius = 40
        painter.setPen(QPen(self.black_color, 0.5))
        painter.drawEllipse(QPointF(0, 0), outer_radius, outer_radius)
        painter.setPen(QPen(self.hand_outline_color, 0.5))
        painter.drawEllipse(QPointF(0, 0), inner_radius, inner_radius)
        painter.setFont(self.font_date)
        painter.setPen(self.date_color)
        for day in range(1, 32):
            angle = -(360 * (day - 1) / 31)
            radius = (outer_radius + inner_radius) / 2
            x = -radius * sin(radians(angle))
            y = -radius * cos(radians(angle))
            painter.save()
            painter.translate(x, y)
            if day % 2 == 0:
                painter.setPen(Qt.NoPen)
                painter.setBrush(self.dot_color)
                painter.drawEllipse(QPointF(0, 0), 1, 1)
            else:
                if day > 8 and day < 24:
                    painter.rotate(180)
                painter.rotate(-angle)
                painter.drawText(QRectF(-5, -5, 10, 10), Qt.AlignCenter, str(day))
            painter.restore()
        painter.restore()

    def draw_second_hand(self, painter, time):
        painter.save()
        outline_pen = QPen(self.hand_outline_color, 0.8)
        painter.setPen(outline_pen)
        painter.setBrush(self.hand_color)
        painter.rotate(6 * time.second() + 0.006 * time.msec())
        painter.drawPath(self.second_hand_path)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.second_hand1_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.second_hand1_dot_radius, self.second_hand1_dot_radius)
        painter.setBrush(self.second_hand2_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.second_hand2_dot_radius, self.second_hand2_dot_radius)
        painter.setBrush(self.second_hand3_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.second_hand3_dot_radius, self.second_hand3_dot_radius)
        painter.restore()

    def draw_hour_hand(self, painter, time):
        painter.save()
        precise_hour = time.hour() % 12 + (time.minute() + time.second() / 60.0 + time.msec() / 60000.0) / 60.0
        outline_pen = QPen(self.hand_outline_color, 0.8)
        painter.setPen(outline_pen)
        painter.setBrush(self.hand_color)
        hour_angle = 30 * precise_hour
        painter.rotate(hour_angle)
        painter.drawPath(self.hour_hand_path)
        painter.restore()

    def draw_minute_hand(self, painter, time):
        painter.save()
        precise_minute = time.minute() + time.second() / 60.0 + time.msec() / 60000.0
        outline_pen = QPen(self.hand_outline_color, 0.8)
        painter.setPen(outline_pen)
        painter.setBrush(self.hand_color)
        minute_angle = 6 * precise_minute
        painter.rotate(minute_angle)
        painter.drawPath(self.minute_hand_path)
        painter.restore()

    def draw_center(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(QPointF(0, 0), 6, 6)
        painter.setBrush(self.but1_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but1_dot_radius, self.but1_dot_radius)
        painter.setBrush(self.but2_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but2_dot_radius, self.but2_dot_radius)
        painter.setBrush(self.but3_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but3_dot_radius, self.but3_dot_radius)
        painter.setBrush(self.but4_dot_color)
        painter.drawEllipse(QPointF(0, 0), self.but4_dot_radius, self.but4_dot_radius)
        highlight = QRadialGradient(0, 0, self.but4_dot_radius)
        highlight.setColorAt(0, QColor(255, 255, 255, 150))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawEllipse(QPointF(0, 0), self.but4_dot_radius, self.but4_dot_radius)
        painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Longinss_Phase()
    window.show()
    app.exec_()