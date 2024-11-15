import sys
import re
import ast
import operator as op
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLineEdit, QTabWidget,
                            QGridLayout, QLabel, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QKeyEvent

class CalculatorButton(QPushButton):
    def __init__(self, text, color="default"):
        super().__init__(text)
        self.setFixedSize(60, 60)
        self.setFont(QFont('Arial', 12))
        
        if color == "operator":
            style = """
                QPushButton {
                    background-color: #FF9500;
                    color: white;
                    border-radius: 30px;
                }
                QPushButton:pressed {
                    background-color: #CC7700;
                }
            """
        elif color == "number":
            style = """
                QPushButton {
                    background-color: #505050;
                    color: white;
                    border-radius: 30px;
                }
                QPushButton:pressed {
                    background-color: #404040;
                }
            """
        elif color == "function":
            style = """
                QPushButton {
                    background-color: #333333;
                    color: white;
                    border-radius: 30px;
                }
                QPushButton:pressed {
                    background-color: #2A2A2A;
                }
            """
        else:
            style = """
                QPushButton {
                    background-color: #737373;
                    color: white;
                    border-radius: 30px;
                }
                QPushButton:pressed {
                    background-color: #606060;
                }
            """
        self.setStyleSheet(style)

class ModernCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Calculator")
        self.setFixedSize(400, 600)
        self.setStyleSheet("background-color: #1C1C1C;")
        
        # Initialize calculator state
        self.current_input = ""
        self.memory = 0
        self.history = []
        self.last_result = ""
        
        # Key mappings for keyboard support
        self.key_mappings = {
            Qt.Key.Key_0: '0', Qt.Key.Key_1: '1', Qt.Key.Key_2: '2',
            Qt.Key.Key_3: '3', Qt.Key.Key_4: '4', Qt.Key.Key_5: '5',
            Qt.Key.Key_6: '6', Qt.Key.Key_7: '7', Qt.Key.Key_8: '8',
            Qt.Key.Key_9: '9', Qt.Key.Key_Plus: '+', Qt.Key.Key_Minus: '-',
            Qt.Key.Key_Asterisk: '×', Qt.Key.Key_Slash: '÷',
            Qt.Key.Key_Period: '.', Qt.Key.Key_ParenLeft: '(',
            Qt.Key.Key_ParenRight: ')', Qt.Key.Key_AsciiCircum: '^',
            Qt.Key.Key_Enter: '=', Qt.Key.Key_Return: '=',
            Qt.Key.Key_Backspace: 'backspace', Qt.Key.Key_Delete: 'C',
            Qt.Key.Key_Escape: 'C'
        }
        
        # Supported operators
        self.operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.Mod: op.mod,
            ast.USub: op.neg,
            ast.UAdd: op.pos,
        }

        # Supported functions
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log10,
            'ln': math.log,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e,
            'fact': math.factorial,
        }
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create displays container that will be above tabs
        displays_widget = QWidget()
        displays_layout = QVBoxLayout(displays_widget)
        displays_layout.setSpacing(5)
        displays_layout.setContentsMargins(10, 10, 10, 0)
        
        # Main display for input
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont('Arial', 24))
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #1C1C1C;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px;
            }
        """)
        displays_layout.addWidget(self.display)
        
        # Sub-display for real-time results
        self.sub_display = QLabel()
        self.sub_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.sub_display.setFont(QFont('Arial', 16))
        self.sub_display.setStyleSheet("""
            QLabel {
                color: #888888;
                padding: 5px 10px;
                margin-bottom: 10px;
                min-height: 25px;
            }
        """)
        displays_layout.addWidget(self.sub_display)
        
        # Add displays to main layout
        layout.addWidget(displays_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #1C1C1C;
            }
            QTabBar::tab {
                background: #333333;
                color: white;
                padding: 8px 20px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #FF9500;
            }
        """)
        
        # Create basic calculator tab
        basic_tab = QWidget()
        basic_layout = QVBoxLayout(basic_tab)
        
        # Button grid for basic tab
        button_grid = QGridLayout()
        button_grid.setSpacing(5)
        
        # Define buttons with positions
        buttons = [
            {'pos': (0, 0), 'text': 'C', 'color': 'function'},
            {'pos': (0, 1), 'text': 'DEL', 'color': 'function'},
            {'pos': (0, 2), 'text': '%', 'color': 'function'},
            {'pos': (0, 3), 'text': '÷', 'color': 'operator'},
            {'pos': (1, 0), 'text': '7', 'color': 'number'},
            {'pos': (1, 1), 'text': '8', 'color': 'number'},
            {'pos': (1, 2), 'text': '9', 'color': 'number'},
            {'pos': (1, 3), 'text': '×', 'color': 'operator'},
            {'pos': (2, 0), 'text': '4', 'color': 'number'},
            {'pos': (2, 1), 'text': '5', 'color': 'number'},
            {'pos': (2, 2), 'text': '6', 'color': 'number'},
            {'pos': (2, 3), 'text': '-', 'color': 'operator'},
            {'pos': (3, 0), 'text': '1', 'color': 'number'},
            {'pos': (3, 1), 'text': '2', 'color': 'number'},
            {'pos': (3, 2), 'text': '3', 'color': 'number'},
            {'pos': (3, 3), 'text': '+', 'color': 'operator'},
            {'pos': (4, 0), 'text': '±', 'color': 'function'},
            {'pos': (4, 1), 'text': '0', 'color': 'number'},
            {'pos': (4, 2), 'text': '.', 'color': 'number'},
            {'pos': (4, 3), 'text': '=', 'color': 'operator'},
        ]
        
        # Add buttons to grid
        for button_info in buttons:
            pos = button_info['pos']
            text = button_info['text']
            color = button_info['color']
            button = CalculatorButton(text, color)
            button.clicked.connect(self.button_clicked)
            span = button_info.get('span', (1, 1))
            button_grid.addWidget(button, pos[0], pos[1], span[0], span[1])
        
        basic_layout.addLayout(button_grid)
        
        # Scientific calculator tab
        scientific_tab = QWidget()
        scientific_layout = QVBoxLayout(scientific_tab)
        
        # Scientific functions buttons
        scientific_grid = QGridLayout()
        scientific_functions = [
            ('sin', 'function'), ('cos', 'function'), ('tan', 'function'),
            ('log', 'function'), ('ln', 'function'), ('√', 'function'),
            ('π', 'function'), ('e', 'function'), ('^', 'operator'),
            ('(', 'function'), (')', 'function'), ('!', 'operator')
        ]
        
        for i, (text, color) in enumerate(scientific_functions):
            button = CalculatorButton(text, color)
            button.clicked.connect(self.button_clicked)
            scientific_grid.addWidget(button, i // 3, i % 3)
                
        scientific_layout.addLayout(scientific_grid)
        
        # Add basic number pad to scientific tab
        scientific_layout.addLayout(button_grid)
        
        # History tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setStyleSheet("""
            QTextEdit {
                background-color: #1C1C1C;
                color: white;
                border: none;
                font-size: 14px;
            }
        """)
        history_layout.addWidget(self.history_display)
        
        # Add tabs to tab widget
        tab_widget.addTab(basic_tab, "Basic")
        tab_widget.addTab(scientific_tab, "Scientific")
        tab_widget.addTab(history_tab, "History")
        
        layout.addWidget(tab_widget)
        
        # Set focus policy to accept keyboard input
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key in self.key_mappings:
            text = self.key_mappings[key]
            self.handle_input(text)
        event.accept()

    def handle_input(self, text):
        if text == 'C':
            self.current_input = ""
            self.display.setText("0")
            self.sub_display.setText("")
            self.last_result = ""
        elif text == 'DEL' or text == 'backspace':
            self.current_input = self.current_input[:-1]
            self.display.setText(self.current_input if self.current_input else "0")
            result = self.calculate_result(self.current_input)
            if result:
                self.sub_display.setText(f"= {result}")
                self.last_result = result
            else:
                self.sub_display.setText("")
                self.last_result = ""
        elif text == '=':
            if self.last_result:
                self.history.append(f"{self.current_input} = {self.last_result}")
                self.update_history()
                self.current_input = self.last_result
                self.display.setText(self.current_input)
                self.sub_display.setText("")
                self.last_result = ""
        elif text == '±':
            if self.current_input and self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display.setText(self.current_input)
            result = self.calculate_result(self.current_input)
            if result:
                self.sub_display.setText(f"= {result}")
                self.last_result = result
        else:
            if text in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
                self.current_input += text + '('
            else:
                self.current_input += text
            
            self.display.setText(self.current_input)
            result = self.calculate_result(self.current_input)
            if result:
                self.sub_display.setText(f"= {result}")
                self.last_result = result
            else:
                self.sub_display.setText("")
                self.last_result = ""

    def button_clicked(self):
        button = self.sender()
        self.handle_input(button.text())

    def calculate_result(self, expression):
        try:
            if not expression:
                return ""
            # Preprocess expression
            expression = self.preprocess_expression(expression)
            # Evaluate expression safely
            result = self.safe_eval(expression)
            # Format result
            if isinstance(result, (int, float)):
                if float(result).is_integer():
                    return str(int(result))
                return f"{result:.8g}"
            return str(result)
        except Exception as e:
            return ""

    def preprocess_expression(self, expr):
        # Replace symbols with Python equivalents
        expr = expr.replace('×', '*')
        expr = expr.replace('÷', '/')
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'pi')
        expr = expr.replace('e', 'e')
        expr = expr.replace('√', 'sqrt')
        # Handle factorial: replace 'expression!' with 'fact(expression)'
        expr = re.sub(r'(\d+|\([^()]*\))!', r'fact(\1)', expr)
        # Remove spaces
        expr = expr.replace(' ', '')
        return expr

    def safe_eval(self, expr):
        try:
            node = ast.parse(expr, mode='eval')
            return self.eval_node(node.body)
        except:
            return None

    def eval_node(self, node):
        if isinstance(node, ast.BinOp):
            left = self.eval_node(node.left)
            right = self.eval_node(node.right)
            operator = self.operators[type(node.op)]
            return operator(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self.eval_node(node.operand)
            operator = self.operators[type(node.op)]
            return operator(operand)
        elif isinstance(node, ast.Call):
            func = node.func.id
            if func in self.functions:
                args = [self.eval_node(arg) for arg in node.args]
                return self.functions[func](*args)
            else:
                raise Exception(f"Unsupported function '{func}'")
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):  # For Python 3.8+
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in self.functions:
                return self.functions[node.id]
            else:
                raise Exception(f"Unsupported variable '{node.id}'")
        else:
            raise Exception(f"Unsupported type '{type(node)}'")

    def update_history(self):
        self.history_display.setText("\n".join(self.history))

def main():
    app = QApplication(sys.argv)
    calculator = ModernCalculator()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

