from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import (QFont, QSyntaxHighlighter, QTextCharFormat, QColor)


def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages

STYLES = {
    'keyword': format([200, 120, 50], 'bold'),
    'operator': format([150, 150, 150]),
    'brace': format('darkGray'),
    'function': format([220, 220, 255], 'bold'),
    'string': format([20, 110, 100]),
    'comment': format([128, 128, 128]),
    'number': format([100, 150, 190]),
    'boolean': format([255, 100, 100]),
    'nil': format([150, 85, 140], 'italic'),
    'custom': format([123, 85, 255]),
    'custom2': format([85, 123, 165]),
}


class CommonHighlighter(QSyntaxHighlighter):
    keywords = [
        'and', 'break', 'do', 'else', 'elseif', 'end',
        'false', 'for', 'function', 'if', 'in',
        'local', 'nil', 'not', 'or', 'repeat',
        'return', 'then', 'true', 'until', 'while'
    ]

    operators = [
        '=', '==', '~=', '<', '<=', '>', '>=',
        '+', '-', '*', '/', '//', '%', '^',
        '+=', '-=', '*=', '/=', '%=', '^=',
    ]

    # Python braces
    braces = [
        '{', '}', '(', ')', '[', ']',
    ]

    custom = [
        'Cast', 'Idle'
    ]

    custom2 = [
        'Prop', 'CoolDown',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegularExpression("'''"), 1, STYLES['comment'])
        self.tri_double = (QRegularExpression('"""'), 2, STYLES['comment'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in CommonHighlighter.keywords]
        rules += [(r'%s' % o, 0, STYLES['operator'])
                  for o in CommonHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
                  for b in CommonHighlighter.braces]
        rules += [(r'%s' % b, 0, STYLES['custom'])
                  for b in CommonHighlighter.custom]
        rules += [(r'%s' % b, 0, STYLES['custom2'])
                  for b in CommonHighlighter.custom2]

        # All other rules
        rules += [

            # 双引号字符串，可能包含转义序列
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # 单引号字符串，可能包含转义序列
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # 注释，从 '--' 开始到行尾
            (r'--[^\n]*', 0, STYLES['comment']),

            # 数字字面量
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['number']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['number']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['number']),

            # 布尔值（true 和 false）
            (r'\b(true|false)\b', 0, STYLES['boolean']),

            # nil
            (r'\b(nil)\b', 0, STYLES['nil']),

            # 函数定义
            (r'\bfunction\b\s*(\w+)', 1, STYLES['function']),

            # 关键字
            (r'\b(' + '|'.join(CommonHighlighter.keywords) + r')\b', 0, STYLES['keyword']),

            # 运算符
            (r'(' + '|'.join(CommonHighlighter.operators) + r')', 0, STYLES['operator']),

            # 括号
            (r'[' + ''.join(CommonHighlighter.braces) + r']', 0, STYLES['brace']),

            # 自定义标识符
            (r'\b(' + '|'.join(CommonHighlighter.custom) + r')\b', 0, STYLES['custom']),
            (r'\b(' + '|'.join(CommonHighlighter.custom2) + r')\b', 0, STYLES['custom2']),
        ]

        # Build a QRegularExpression for each pattern
        self.rules = [(QRegularExpression(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                # print(rule.pattern.pattern())
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
            # end = 0
        # Otherwise, look for the delimiter on this line
        else:
            match = delimiter.match(text)
            start = match.capturedStart()
            # Move past this match
            add = match.capturedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            match = delimiter.match(text, start + add)
            end = match.capturedStart()
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + match.capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.match(text, start + length).capturedStart()

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
