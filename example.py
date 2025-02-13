import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super(SyntaxHighlighter, self).__init__(parent)
        self.highlightingRules = []

        # Определение правил подсветки
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("blue"))
        keywordFormat.setFontWeight(QFont.Bold)
        
        keywords = [
            "\\bdef\\b", "\\bclass\\b", "\\bif\\b", "\\belse\\b", "\\bwhile\\b", 
            "\\bfor\\b", "\\bin\\b", "\\breturn\\b", "\\bimport\\b", "\\bfrom\\b", 
            "\\bas\\b", "\\btry\\b", "\\bexcept\\b", "\\braise\\b", "\\bpass\\b",
            "\\bbreak\\b", "\\bcontinue\\b"
        ]
        
        for word in keywords:
            self.highlightingRules.append((QRegExp(word), keywordFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("green"))
        self.highlightingRules.append((QRegExp("#[^\n]*"), commentFormat))

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("magenta"))
        self.highlightingRules.append((QRegExp("\".*\""), stringFormat))
        self.highlightingRules.append((QRegExp("'.*'"), stringFormat))
        
        # Подсветка для C++ (аналогично для других языков)
        cpp_keywords = [
            "\\bint\\b", "\\bfloat\\b", "\\bdouble\\b", "\\bchar\\b", "\\bvoid\\b",
            "\\breturn\\b", "\\bif\\b", "\\belse\\b", "\\bwhile\\b", "\\bfor\\b"
        ]
        for word in cpp_keywords:
            self.highlightingRules.append((QRegExp(word), keywordFormat))
        
        # Подсветка для CSS
        css_keywords = [
            "\\bcolor\\b", "\\bbackground-color\\b", "\\bfont-size\\b", "\\bmargin\\b",
            "\\bpadding\\b", "\\bborder\\b", "\\bwidth\\b", "\\bheight\\b"
        ]
        for word in css_keywords:
            self.highlightingRules.append((QRegExp(word), keywordFormat))
        
        # Подсветка для HTML
        html_keywords = [
            "<[^>]*>"
        ]
        htmlFormat = QTextCharFormat()
        htmlFormat.setForeground(QColor("red"))
        for word in html_keywords:
            self.highlightingRules.append((QRegExp(word), htmlFormat))

    def highlightBlock(self, text):
        for pattern, text_format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, text_format)
                index = expression.indexIn(text, index + length)

class CodeViewer(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Courier", 10))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Syntax Highlighter")
        self.setGeometry(100, 100, 800, 600)
        
        self.editor = CodeViewer()
        self.setCentralWidget(self.editor)
        
        # Инициализация подсветки синтаксиса для Python
        highlighter = SyntaxHighlighter(self.editor.document())
        
        # Пример кода для подсветки
        example_code = '''
# Пример кода на Python
def hello_world():
    print("Hello, world!")

# Пример кода на C++
int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}

/* Пример кода на CSS */
body {
    background-color: #f0f0f0;
}

/* Пример кода на HTML */
<!DOCTYPE html>
<html>
<head>
    <title>Пример
'''
        self.editor.setPlainText(example_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
