from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QComboBox, QTextEdit, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import (
    QPoint,
    Qt,
    QThread,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QEasingCurve,
    QMargins,
    pyqtProperty,
    QRegExp
)
from random import choice, randint
from time import sleep
from config import get_widget_style
from utils import convert_to_rgb

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(100)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)

        red, green, blue = get_widget_style('Button', 'default-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 77
            green = 77
            blue = 77
            
        self.anim2_color = QColor(red, green, blue)
        self.anim2_start_color = QColor(red, green, blue)
        
        red, green, blue = get_widget_style('Button', 'active-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 64
            green = 64
            blue = 64
        
        self.anim2_end_color = QColor(red, green, blue)
        self.anim2 = QPropertyAnimation(self, b'color')
        self.anim2.setDuration(100)

        self.anim_group = QParallelAnimationGroup(self)
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim2)
        
        self.update_style()
    
    def update_style(self):
        self.widget_style = f"QPushButton {{ /*start bg color*/ background-color: {get_widget_style('Button', 'default-background-color')}; /*end bg color*/ border-radius: 10px; color: {get_widget_style('Button', 'color')}}}"

        self.setStyleSheet(self.widget_style)
        
        red, green, blue = get_widget_style('Button', 'default-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 77
            green = 77
            blue = 77

        self.anim2_start_color = QColor(red, green, blue)
        
        red, green, blue = get_widget_style('Button', 'active-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 64
            green = 64
            blue = 64
        
        self.anim2_end_color = QColor(red, green, blue)

    @pyqtProperty(QColor)
    def color(self):
        return self.anim2_color

    @color.setter
    def color(self, color : QColor):
        self.anim2_color = color

        bg_color = self.widget_style[self.widget_style.index("/*start bg color*/")+len("/*start bg color*/"):self.widget_style.index("/*end bg color*/")]
        new_style = self.widget_style.replace(bg_color, f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")
        self.setStyleSheet(new_style)

    def enterEvent(self, a0: QtCore.QEvent | None) -> None:
        self.anim_group.setDirection(self.anim_group.Forward)

        if self.anim_group.state() == self.anim_group.State.Stopped:
            rect = self.geometry()
            self.anim.setStartValue(rect)
            rect += QMargins(3, 3, 3, 3)
            self.anim.setEndValue(rect)

            self.anim2.setStartValue(self.anim2_start_color)
            self.anim2.setEndValue(self.anim2_end_color)

            self.anim_group.start()

        return super().enterEvent(a0)
    
    def leaveEvent(self, a0: QtCore.QEvent | None) -> None:
        self.anim_group.setDirection(self.anim_group.Backward)

        if self.anim_group.state() == self.anim_group.State.Stopped:
            self.anim_group.start()

        return super().leaveEvent(a0)


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)    

        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(100)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        
        red, green, blue = get_widget_style('ComboBox', 'default-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 77
            green = 77
            blue = 77
            
        self.anim2_color = QColor(red, green, blue)
        self.anim2_start_color = QColor(red, green, blue)
        
        red, green, blue = get_widget_style('ComboBox', 'active-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 64
            green = 64
            blue = 64
        
        self.anim2_end_color = QColor(red, green, blue)
        self.anim2 = QPropertyAnimation(self, b'color')
        self.anim2.setDuration(100)


        self.anim_group = QParallelAnimationGroup(self)
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim2)
        
        self.update_style()

    def update_style(self):
        self.widget_style = f"QComboBox {{ /*start bg color*/ background-color: {get_widget_style('ComboBox', 'default-background-color')}; /*end bg color*/ border-radius: 10px; color: {get_widget_style('ComboBox', 'color')}}} QComboBox::drop-down {{ background-color: {get_widget_style('ComboBox', 'drop-down-background-color')}; }} QComboBox QAbstractItemView {{ background-color: {get_widget_style('ComboBox', 'abstract-item-view-background-color')}; selection-background-color: {get_widget_style('ComboBox', 'abstract-item-view-selection-background-color')}; }}"
        
        self.setStyleSheet(self.widget_style)
        
        red, green, blue = get_widget_style('ComboBox', 'default-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 77
            green = 77
            blue = 77

        self.anim2_start_color = QColor(red, green, blue)
        
        red, green, blue = get_widget_style('ComboBox', 'active-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 64
            green = 64
            blue = 64
        
        self.anim2_end_color = QColor(red, green, blue)
        
    @pyqtProperty(QColor)
    def color(self):
        return self.anim2_color

    @color.setter
    def color(self, color : QColor):
        self.anim2_color = color

        bg_color = self.widget_style[self.widget_style.index("/*start bg color*/")+len("/*start bg color*/"):self.widget_style.index("/*end bg color*/")]
        new_style = self.widget_style.replace(bg_color, f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")
        self.setStyleSheet(new_style)
    
    def enterEvent(self, a0: QtCore.QEvent | None) -> None:
        self.anim_group.setDirection(self.anim_group.Forward)

        if self.anim_group.state() == self.anim_group.State.Stopped:
            rect = self.geometry()
            self.anim.setStartValue(rect)
            rect += QMargins(2, 2, 2, 2)
            self.anim.setEndValue(rect)

            self.anim2.setStartValue(self.anim2_start_color)
            self.anim2.setEndValue(self.anim2_end_color)

            self.anim_group.start()

        return super().enterEvent(a0)
    
    def leaveEvent(self, a0: QtCore.QEvent | None) -> None:
        self.anim_group.setDirection(self.anim_group.Backward)

        if self.anim_group.state() == self.anim_group.State.Stopped:
            self.anim_group.start()

        return super().leaveEvent(a0)

class TextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        
        red, green, blue = get_widget_style('TextEdit', 'default-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 77
            green = 77
            blue = 77

        self.anim_color = QColor(red, green, blue)
        self.anim_start_color = QColor(red, green, blue)
        
        red, green, blue = get_widget_style('TextEdit', 'active-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 64
            green = 64
            blue = 64
        
        self.anim_end_color = QColor(red, green, blue)
        
        self.anim = QPropertyAnimation(self, b"color")
        self.anim.setDuration(100)

        self.anim_group = QParallelAnimationGroup(self)
        self.anim_group.addAnimation(self.anim)
        
        self.update_style()
    
    def update_style(self):
        self.widget_style = f"QTextEdit {{ /*start bg color*/ background-color: {get_widget_style('TextEdit', 'default-background-color')}; /*end bg color*/ color: {get_widget_style('TextEdit', 'color')}; selection-color: {get_widget_style('TextEdit', 'selection-color')}; selection-background-color: {get_widget_style('TextEdit', 'selection-background-color')}; }}"

        self.setStyleSheet(self.widget_style)
        
        red, green, blue = get_widget_style('TextEdit', 'default-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 77
            green = 77
            blue = 77

        self.anim_start_color = QColor(red, green, blue)
        
        red, green, blue = get_widget_style('TextEdit', 'active-background-color').replace("rgb(", "").replace(")", "").split(", ")
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
        except ValueError:
            red = 64
            green = 64
            blue = 64
        
        self.anim_end_color = QColor(red, green, blue)
        
    @pyqtProperty(QColor)
    def color(self):
        return self.anim_color

    @color.setter
    def color(self, color : QColor):
        self.anim_color = color
        
        bg_color = self.widget_style[self.widget_style.index("/*start bg color*/")+len("/*start bg color*/"):self.widget_style.index("/*end bg color*/")]
        new_style = self.widget_style.replace(bg_color, f"background-color: rgb({color.red()}, {color.green()}, {color.blue()});")
        self.setStyleSheet(new_style)
        
    def enterEvent(self, a0: QtCore.QEvent | None) -> None:
        self.anim_group.setDirection(self.anim_group.Forward)

        if self.anim_group.state() == self.anim_group.State.Stopped:
            self.anim.setStartValue(self.anim_start_color)
            self.anim.setEndValue(self.anim_end_color)

            self.anim_group.start()

        return super().enterEvent(a0)
    
    def leaveEvent(self, a0: QtCore.QEvent | None) -> None:
        self.anim_group.setDirection(self.anim_group.Backward)

        if self.anim_group.state() == self.anim_group.State.Stopped:
            self.anim_group.start()

        return super().leaveEvent(a0)

class Triangle(QWidget):
    def __init__(self, parent=None, position=(0, 0), width=100, height=85, color : QColor = QColor(255, 255, 255)):
        super().__init__(parent)
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.setGeometry(position[0], position[1], width, height)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.update()

    def set_color(self, color):
        self.color = color
        #self.update()

    def set_position(self, x, y):
        self.position = (x, y)
        self.setGeometry(x, y, self.width, self.height)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.color, 2, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(0, 0, 0, 0), Qt.SolidPattern))
        points = [
            QPoint(self.width // 2, 0),
            QPoint(self.width, self.height),
            QPoint(0, self.height)
        ]
        painter.drawPolygon(*points)

class Ellipse(QWidget):
    def __init__(self, parent=None, position=(0, 0), width=100, height=100, color : QColor = QColor(255, 255, 255)):
        super().__init__(parent)
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.setGeometry(position[0], position[1], width, height)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.update()

    def set_color(self, color):
        self.color = color
        #self.update()

    def set_position(self, x, y):
        self.position = (x, y)
        self.setGeometry(x, y, self.width, self.height)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(self.color, 2, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(0, 0, 0, 0), Qt.SolidPattern))
        painter.drawEllipse(0, 0, self.width, self.height)

class BackgroundCode():
    class BackgroundCodeSymbol():
        SYMBOL_WIDTH = 15
        SYMBOL_HEIGHT = 11
        def __init__(self, parent, relative_pos, symbol_type = None) -> None:
            self.parent = parent
            
            x_offset = relative_pos + BackgroundCode.BackgroundCodeSymbol.SYMBOL_WIDTH // 2
            y_offset = parent.height()//2 - BackgroundCode.BackgroundCodeSymbol.SYMBOL_HEIGHT // 2

            if x_offset+BackgroundCode.BackgroundCodeSymbol.SYMBOL_WIDTH <= parent.x()+parent.width()-BackgroundCode.BackgroundCodeSymbol.SYMBOL_WIDTH:
                if not symbol_type:
                    symbol_type = choice(("square", "triangle", "ellipse"))
                
                if symbol_type == "square":
                    self.symbol = QWidget(parent)
                    self.symbol.setGeometry(x_offset, y_offset, BackgroundCode.BackgroundCodeSymbol.SYMBOL_WIDTH, BackgroundCode.BackgroundCodeSymbol.SYMBOL_HEIGHT)
                    self.symbol.setStyleSheet("background-color: rgba(120, 120, 120, 40);")  
                elif symbol_type == "triangle":
                    self.symbol = Triangle(
                                            parent,
                                            (x_offset, y_offset),
                                            BackgroundCode.BackgroundCodeSymbol.SYMBOL_WIDTH,
                                            BackgroundCode.BackgroundCodeSymbol.SYMBOL_HEIGHT,
                                            QColor(120, 120, 120, 40)
                                        )
                elif symbol_type == "ellipse":
                    self.symbol = Ellipse(
                                            parent,
                                            (x_offset, y_offset),
                                            BackgroundCode.BackgroundCodeSymbol.SYMBOL_WIDTH,
                                            BackgroundCode.BackgroundCodeSymbol.SYMBOL_HEIGHT,
                                            QColor(120, 120, 120, 40)
                    )
            else:
                self.symbol = None
        def show(self):
            try:
                self.symbol.show()
                
                """
                if isinstance(self.symbol, QWidget):
                    self.symbol.setStyleSheet("background-color: rgba(120, 120, 120, 0);")
                    for i in range(1, 40):
                        self.symbol.setStyleSheet(f"background-color: rgba(120, 120, 120, {i});")
                        sleep(0.0015)
                if isinstance(self.symbol, Triangle):
                    pass
                    #self.symbol.set_color(QColor(120, 120, 120, 40))
                    #self.symbol.set_color(QColor(120, 120, 120, 0))
                    #for i in range(1, 40):
                    #    self.symbol.set_color(QColor(120, 120, 120, i))
                    #    sleep(0.0025)
                if isinstance(self.symbol, Ellipse):
                    pass
                    #self.symbol.set_color(QColor(120, 120, 120, 40))
                    #self.symbol.set_color(QColor(120, 120, 120, 0))
                    #for i in range(1, 40):
                    #    self.symbol.set_color(QColor(120, 120, 120, i))
                    #    sleep(0.0025)
                
                """
            except RuntimeError as e:
                print(e)
            
        def hide(self):
            self.symbol.hide()
    class FillThread(QThread):
        def run(self):
            for element in BackgroundCode.elements:
                element.display()

    current_coord_y = 20
    current_offset_x = 20
    elements = []
    fill_thread = None

    def __init__(self, parent):
        self.widget = QWidget(parent)
        
        y_offset = BackgroundCode.current_coord_y
        x_offset = BackgroundCode.current_offset_x

        lenght = randint(80, 180)
        BackgroundCode.current_offset_x += lenght + 10

        if len(BackgroundCode.elements) % 2 != 0:
            BackgroundCode.current_coord_y+=40
            BackgroundCode.current_offset_x = 20

        self.widget.setGeometry(x_offset, y_offset, lenght, 21)
        
        self.background_symbols = []
        
        BackgroundCode.elements.append(self)

        self.update_style()
        self.fill()
    
    def update_style(self):
        self.widget.setStyleSheet(f"background-color: {get_widget_style('BackgroundCodeLine', 'background-color')};")

    def fill(self):
        squares_count, triangles_count, ellipses_count = 0, 0, 0
        max_squares_count, max_triangles_count, max_ellipses_count = 10, 3, 2

        for i in range(randint(7, 16)):
            symbol_type = None

            while True:
                if max_squares_count + max_triangles_count + max_ellipses_count <= i:
                    break

                symbol_type = choice(("square", "triangle", "ellipse"))
                if symbol_type == "square" and squares_count < max_squares_count:
                    squares_count += 1
                    break
                if symbol_type == "triangle" and triangles_count < max_triangles_count:
                    triangles_count += 1
                    break
                if symbol_type == "ellipse" and ellipses_count < max_ellipses_count:
                    ellipses_count += 1
                    break
            
            symbol = self.BackgroundCodeSymbol(self.widget, i*17, symbol_type)
            if symbol.symbol:
                symbol.hide()
                self.background_symbols.append(symbol)
            if i*17 >= self.widget.width():
                break
            
    def display(self):
        for symbol in self.background_symbols:
            symbol.show()
            sleep(randint(2, 5)/100)
    
    @staticmethod
    def hide():
        for element in BackgroundCode.elements:
            element.widget.hide()

    @staticmethod
    def show():
        for element in BackgroundCode.elements:
            element.widget.show()
        
        BackgroundCode.fill_thread = BackgroundCode.FillThread()
        BackgroundCode.fill_thread.start()

class SyntaxHighlighter(QSyntaxHighlighter):
    class SyntaxType:
        class PythonSyntax:
            keywords = [ "\\bdef\\b", "\\bclass\\b", "\\bif\\b", "\\belse\\b", "\\bwhile\\b", 
                    "\\bfor\\b", "\\bin\\b", "\\breturn\\b", "\\bimport\\b", "\\bfrom\\b", 
                    "\\bas\\b", "\\btry\\b", "\\bexcept\\b", "\\blambda\\b", "\\bassert\\b",
                    "\\bfinally\\b", "\\bnonlocal\\b", "\\braise\\b", "\\bpass\\b", "\\byield\\b"
                    "\\bbreak\\b", "\\bcontinue\\b", "\\bTrue\\b", "\\bFalse\\b", "\\bNone\\b",
                    "\\bdel\\b", "\\bself\\b", "\\bglobal\\b"
            ]

            comment_rule = r"#[^\n]*"
            
            string_rules = [r"\".*\"", r"'.*'"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("PythonSyntaxHighlight", "keyword-color")),
                "number": convert_to_rgb(get_widget_style("PythonSyntaxHighlight", "number-color")),
                "brace": convert_to_rgb(get_widget_style("PythonSyntaxHighlight", "brace-color")),
                "string": convert_to_rgb(get_widget_style("PythonSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("PythonSyntaxHighlight", "comment-color"))
            }
        class CPPSyntax:
            keywords = [ "\\bauto\\b", "\\bchar\\b", "\\bconst\\b", 
                  "\\bdefault\\b", "\\bdouble\\b",
                  "\\benum\\b", "\\bextern\\b", "\\bfloat\\b",
                  "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bregister\\b",
                  "\\brestrict\\b", "\\bshort\\b", "\\bsigned\\b", "\\bsizeof\\b",
                  "\\bstatic\\b", "\\bstruct\\b", "\\btypedef\\b", "\\bunion\\b",
                  "\\bunsigned\\b", "\\bvoid\\b", "\\bvolatile\\b",
                  "\\basm\\b", "\\bbool\\b", "\\bclass\\b", "\\bconst_cast\\b",
                  "\\bdelete\\b", "\\bdynamic_cast\\b", "\\bexplicit\\b", "\\bexport\\b",
                  "\\bfalse\\b", "\\bfriend\\b", "\\binline\\b", "\\bmutable\\b", "\\bnamespace\\b",
                  "\\bnew\\b", "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b", "\\bpublic\\b",
                  "\\breinterpret_cast\\b", "\\bstatic_cast\\b", "\\btemplate\\b", "\\bthis\\b",
                "\\btrue\\b", "\\btypeid\\b", "\\btypename\\b",
                  "\\busing\\b", "\\bvirtual\\b", "\\bwchar_t\\b", "\\bconstexpr\\b", "\\bdecltype\\b",
                  "\\bnoexcept\\b", "\\bnullptr\\b", "\\bstatic_assert\\b", "\\bthread_local\\b"
            ]
            keywords2 = [ "\\bif\\b", "\\belse\\b", "\\bdo\\b", "\\bfor\\b", "\\bwhile\\b", "\\bgoto\\b", 
                          "\\bbreak\\b", "\\bcontinue\\b", "\\bthrow\\b", "\\breturn\\b", "\\bcatch\\b", "\\bcase\\b", "\\bswitch\\b", "\\btry\\b"
            ]

            keywords3 = [ "\\bBOOL\\b", "\\bINT64\\b", "\\bBYTE\\b", "\\bCHAR\\b", "\\bCSTR\\b", "\\bDWORD\\b", 
                          "\\bFLOAT\\b", "\\bHRESULT\\b", "\\bINT\\b", "\\bINT8\\b", "\\bINT16\\b", "\\bINT32\\b", 
                          "\\bLONGLONG\\b", "\\bLPARAM\\b", "\\bLPCSTR\\b", "\\bLPCWSTR\\b", "\\bLPSTR\\b", 
                          "\\bLPWSTR\\b", "\\bPBYTE\\b", "\\bPCHAR\\b", "\\bPCSTR\\b", "\\bPDWORD\\b", "\\bPFLOAT\\b", 
                          "\\bPHRESULT\\b", "\\bPINT\\b", "\\bPINT8\\b", "\\bPINT16\\b", "\\bPINT32\\b", 
                          "\\bPLONGLONG\\b", "\\bPNBYTE\\b", "\\bPNCHAR\\b", "\\bPNSTR\\b", "\\bPWCHAR\\b", 
                          "\\bPWORD\\b", "\\bQWORD\\b", "\\bUINT\\b", "\\bUINT8\\b", "\\bUINT16\\b", "\\bUINT32\\b", 
                          "\\bULONGLONG\\b", "\\bUSHORT\\b", "\\bVOID\\b", "\\bWPARAM\\b", "\\bWORD\\b", 
                          "\\bWCHAR\\b", "\\bHMODULE\\b", "\\bFILE\\b", "\\bLPVOID\\b", "\\bstring ?,?\\b"
            ]

            keywords4 = [ "\\binclude\\b", "\\bdefine\\b", "\\bifdef\\b", "\\bifndef\\b", "\\bpragma once\\b", "\\bpragma warning\\b" ]


            comment_rule = r"//[^\n]*"

            string_rules = [r"\".*\"", r"'.*'", r"<.*?>"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword-color")),
                "keyword2": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword2-color")),
                "keyword3": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword3-color")),
                "keyword4": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword4-color")),
                "number": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "number-color")),
                "brace": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "brace-color")),
                "string": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "comment-color"))
            }
        class CSyntax:
            keywords = [ "\\bauto\\b", "\\bbreak\\b", "\\bcase\\b", "\\bchar\\b", "\\bconst\\b", 
                    "\\bcontinue\\b", "\\bdefault\\b", "\\bdo\\b", "\\bdouble\\b", "\\belse\\b",
                    "\\benum\\b", "\\bextern\\b", "\\bfloat\\b", "\\bfor\\b", "\\bgoto\\b",
                    "\\bif\\b", "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bregister\\b",
                    "\\brestrict\\b", "\\breturn\\b", "\\bshort\\b", "\\bsigned\\b", "\\bsizeof\\b",
                    "\\bstatic\\b", "\\bstruct\\b", "\\bswitch\\b", "\\btypedef\\b", "\\bunion\\b",
                    "\\bunsigned\\b", "\\bvoid\\b", "\\bvolatile\\b", "\\bwhile\\b"
            ]

            keywords2 = [ "\\bif\\b", "\\belse\\b", "\\bdo\\b", "\\bfor\\b", "\\bwhile\\b", "\\bgoto\\b", 
                          "\\bbreak\\b", "\\bcontinue\\b", "\\bthrow\\b", "\\breturn\\b", "\\bcatch\\b", "\\bcase\\b", "\\bswitch\\b", "\\btry\\b" ]

            keywords3 = [ "\\bBOOL\\b", "\\bINT64\\b", "\\bBYTE\\b", "\\bCHAR\\b", "\\bCSTR\\b", "\\bDWORD\\b", 
                          "\\bFLOAT\\b", "\\bHRESULT\\b", "\\bINT\\b", "\\bINT8\\b", "\\bINT16\\b", "\\bINT32\\b", 
                          "\\bLONGLONG\\b", "\\bLPARAM\\b", "\\bLPCSTR\\b", "\\bLPCWSTR\\b", "\\bLPSTR\\b", 
                          "\\bLPWSTR\\b", "\\bPBYTE\\b", "\\bPCHAR\\b", "\\bPCSTR\\b", "\\bPDWORD\\b", "\\bPFLOAT\\b", 
                          "\\bPHRESULT\\b", "\\bPINT\\b", "\\bPINT8\\b", "\\bPINT16\\b", "\\bPINT32\\b", 
                          "\\bPLONGLONG\\b", "\\bPNBYTE\\b", "\\bPNCHAR\\b", "\\bPNSTR\\b", "\\bPWCHAR\\b", 
                          "\\bPWORD\\b", "\\bQWORD\\b", "\\bUINT\\b", "\\bUINT8\\b", "\\bUINT16\\b", "\\bUINT32\\b", 
                          "\\bULONGLONG\\b", "\\bUSHORT\\b", "\\bVOID\\b", "\\bWPARAM\\b", "\\bWORD\\b", 
                          "\\bWCHAR\\b", "\\bHMODULE\\b", "\\bFILE\\b", "\\bLPVOID\\b", "\\bstring\\b"
            ]

            keywords4 = [ "\\binclude\\b", "\\bdefine\\b", "\\bifdef\\b", "\\bifndef\\b", "\\bpragma once\\b", "\\bpragma warning\\b" ]

            comment_rule = r"//[^\n]*"

            string_rules = [r"\".*\"", r"'.*'", r"<.*>"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("CSyntaxHighlight", "keyword-color")),
                "keyword2": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword2-color")),
                "keyword3": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword3-color")),
                "keyword4": convert_to_rgb(get_widget_style("CPPSyntaxHighlight", "keyword4-color")),
                "number": convert_to_rgb(get_widget_style("CSyntaxHighlight", "number-color")),
                "brace": convert_to_rgb(get_widget_style("CSyntaxHighlight", "brace-color")),
                "string": convert_to_rgb(get_widget_style("CSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("CSyntaxHighlight", "comment-color"))
            }

        class JSSyntax:
            keywords = [ "\\bawait\\b", "\\bbreak\\b", "\\bcase\\b", "\\bcatch\\b", "\\bclass\\b", 
                    "\\bconst\\b", "\\bcontinue\\b", "\\bdebugger\\b", "\\bdefault\\b", 
                    "\\bdelete\\b", "\\bdo\\b", "\\belse\\b", "\\benum\\b", "\\bexport\\b", 
                    "\\bextends\\b", "\\bfalse\\b", "\\bfinally\\b", "\\bfor\\b", 
                    "\\bfunction\\b", "\\bif\\b", "\\bimport\\b", "\\bin\\b", 
                    "\\binstanceof\\b", "\\blet\\b", "\\bnew\\b", "\\bnull\\b", 
                    "\\breturn\\b", "\\bsuper\\b", "\\bswitch\\b", "\\bthis\\b", 
                    "\\bthrow\\b", "\\btrue\\b", "\\btry\\b", "\\btypeof\\b", "\\bvar\\b", 
                    "\\bvoid\\b", "\\bwhile\\b", "\\bwith\\b", "\\byield\\b"
            ]

            comment_rule = r"//[^\n]*"

            string_rules = [r"\".*\"", r"'.*'"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("JSSyntaxHighlight", "keyword-color")),
                "number": convert_to_rgb(get_widget_style("JSSyntaxHighlight", "number-color")),
                "brace": convert_to_rgb(get_widget_style("JSSyntaxHighlight", "brace-color")),
                "string": convert_to_rgb(get_widget_style("JSSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("JSSyntaxHighlight", "comment-color"))
            }

        class HTMLSyntax:
            keywords = [ "\\bdoctype\\b", "\\bhtml\\b", "\\bhead\\b", "\\bmain\\b", "\\btitle\\b", "\\bbody\\b", "\\bh1\\b", 
                  "\\bh2\\b", "\\bh3\\b", "\\bh4\\b", "\\bh5\\b", "\\bh6\\b", "\\bp\\b", 
                  "\\ba\\b", "\\bimg\\b", "\\bdiv\\b", "\\bspan\\b", "\\bstrong\\b", 
                  "\\bem\\b", "\\btable\\b", "\\btr\\b", "\\btd\\b", "\\bth\\b", "\\bthead\\b", 
                  "\\btbody\\b", "\\btfoot\\b", "\\bul\\b", "\\bol\\b", "\\bli\\b", "\\bform\\b", 
                  "\\binput\\b", "\\bbutton\\b", "\\btextarea\\b", "\\bselect\\b", "\\boption\\b",
                  "\\blink\\b", "\\bmeta\\b", "\\bscript\\b", "\\bstyle\\b"
            ]

            comment_rule = r"<!--.*?-->"

            string_rules = [r"\".*\"", r"'.*'"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("HTMLSyntaxHighlight", "keyword-color")),
                "string": convert_to_rgb(get_widget_style("HTMLSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("HTMLSyntaxHighlight", "comment-color"))
            }

        class CSSSyntax:
            keywords = [ "\\balignment-adjust\\b", "\\balignment-baseline\\b", "\\banimation\\b", 
                    "\\banimation-delay\\b", "\\banimation-direction\\b", "\\banimation-duration\\b", 
                    "\\banimation-fill-mode\\b", "\\banimation-iteration-count\\b", "\\banimation-name\\b", 
                    "\\banimation-play-state\\b", "\\banimation-timing-function\\b", "\\bbackface-visibility\\b", 
                    "\\bbackground\\b", "\\bbackground-attachment\\b", "\\bbackground-clip\\b", 
                    "\\bbackground-color\\b", "\\bbackground-image\\b", "\\bbackground-origin\\b", 
                    "\\bbackground-position\\b", "\\bbackground-repeat\\b", "\\bbackground-size\\b", 
                    "\\bborder\\b", "\\bborder-bottom\\b", "\\bborder-bottom-color\\b", "\\bborder-bottom-left-radius\\b", 
                    "\\bborder-bottom-right-radius\\b", "\\bborder-bottom-style\\b", "\\bborder-bottom-width\\b", 
                    "\\bborder-collapse\\b", "\\bborder-color\\b", "\\bborder-image\\b", "\\bborder-image-outset\\b", 
                    "\\bborder-image-repeat\\b", "\\bborder-image-slice\\b", "\\bborder-image-source\\b", 
                    "\\bborder-image-width\\b", "\\bborder-left\\b", "\\bborder-left-color\\b", "\\bborder-left-style\\b", 
                    "\\bborder-left-width\\b", "\\bborder-radius\\b", "\\bborder-right\\b", "\\bborder-right-color\\b", 
                    "\\bborder-right-style\\b", "\\bborder-right-width\\b", "\\bborder-spacing\\b", "\\bborder-style\\b", 
                    "\\bborder-top\\b", "\\bborder-top-color\\b", "\\bborder-top-left-radius\\b", "\\bborder-top-right-radius\\b", 
                    "\\bborder-top-style\\b", "\\bborder-top-width\\b", "\\bborder-width\\b", "\\bbottom\\b"
            ]

            comment_rule = r"/\*[^*]*\*+(?:[^/*][^*]*\*+)*/"

            string_rules = [r"\".*\"", r"'.*'"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("CSSSyntaxHighlight", "keyword-color")),
                "string": convert_to_rgb(get_widget_style("CSSSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("CSSSyntaxHighlight", "comment-color"))
            }

        class LuaSyntax:
            keywords = [ "\\band\\b", "\\bbreak\\b", "\\bdo\\b", "\\belse\\b", "\\belseif\\b", 
                    "\\bend\\b", "\\bfalse\\b", "\\bfor\\b", "\\bfunction\\b", "\\bif\\b", 
                    "\\bin\\b", "\\blocal\\b", "\\bnil\\b", "\\bnot\\b", "\\bor\\b", "\\brepeat\\b", 
                    "\\breturn\\b", "\\bthen\\b", "\\btrue\\b", "\\buntil\\b", "\\bwhile\\b"
            ]

            string_rules = [r"\".*\"", r"'.*'"]

            styles = {
                "keyword": convert_to_rgb(get_widget_style("LuaSyntaxHighlight", "keyword-color")),
                "number": convert_to_rgb(get_widget_style("LuaSyntaxHighlight", "number-color")),
                "brace": convert_to_rgb(get_widget_style("LuaSyntaxHighlight", "brace-color")),
                "string": convert_to_rgb(get_widget_style("LuaSyntaxHighlight", "string-color")),
                "comment": convert_to_rgb(get_widget_style("LuaSyntaxHighlight", "comment-color"))
            }

    def __init__(self, parent, syntax):
        super().__init__(parent)

        self.highlightRules = []

        # Defining hightlight rules
        
        if "keyword" in syntax.styles:
            keywordFormat = QTextCharFormat()
            
            keywordFormat.setForeground(QColor(*syntax.styles["keyword"]))
            keywordFormat.setFontWeight(QtGui.QFont.Bold)

            for word in syntax.keywords:
                self.highlightRules.append((QRegExp(word), keywordFormat))
        if "keyword2" in syntax.styles:
            keywordFormat = QTextCharFormat()

            keywordFormat.setForeground(QColor(*syntax.styles["keyword2"]))
            keywordFormat.setFontWeight(QtGui.QFont.Bold)

            for word in syntax.keywords2:
                self.highlightRules.append((QRegExp(word), keywordFormat))
        if "keyword3" in syntax.styles:
            keywordFormat = QTextCharFormat()

            keywordFormat.setForeground(QColor(*syntax.styles["keyword3"]))
            keywordFormat.setFontWeight(QtGui.QFont.Bold)

            for word in syntax.keywords3:
                self.highlightRules.append((QRegExp(word), keywordFormat))

        if "keyword4" in syntax.styles:
            keywordFormat = QTextCharFormat()

            keywordFormat.setForeground(QColor(*syntax.styles["keyword4"]))
            keywordFormat.setFontWeight(QtGui.QFont.Bold)

            for word in syntax.keywords4:
                self.highlightRules.append((QRegExp(word), keywordFormat))

        if "number" in syntax.styles:
            digitFormat = QTextCharFormat()
            digitFormat.setForeground(QColor(*syntax.styles["number"]))
            self.highlightRules.append((QRegExp(r"\b\d+\b"), digitFormat))
            self.highlightRules.append((QRegExp(r"\d+\.\d+"), digitFormat))

        if "brace" in syntax.styles:
            braceFormat = QTextCharFormat()
            braceFormat.setForeground(QColor(*syntax.styles["brace"]))
            self.highlightRules.append((QRegExp(r"\("), braceFormat))
            self.highlightRules.append((QRegExp(r"\)"), braceFormat))
            self.highlightRules.append((QRegExp(r"\["), braceFormat))
            self.highlightRules.append((QRegExp(r"\]"), braceFormat))
            self.highlightRules.append((QRegExp(r"\{"), braceFormat))
            self.highlightRules.append((QRegExp(r"\}"), braceFormat))

        if "string" in syntax.styles:
            stringFormat = QTextCharFormat()
            stringFormat.setForeground(QColor(*syntax.styles["string"]))
            self.highlightRules.append((QRegExp(syntax.string_rules[0]), stringFormat))
            self.highlightRules.append((QRegExp(QRegExp(syntax.string_rules[1])), stringFormat))
        
        if "comment" in syntax.styles:
            commentFormat = QTextCharFormat()
            commentFormat.setForeground(QColor(*syntax.styles["comment"]))
            self.highlightRules.append((QRegExp(syntax.comment_rule), commentFormat))

    def highlightBlock(self, text: str | None) -> None:
        for pattern, text_format in self.highlightRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)

            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, text_format)
                index = expression.indexIn(text, index+length)
    