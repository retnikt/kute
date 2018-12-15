from PyQt5 import QtCore, QtGui
from keyword import kwlist


def make_style(color, weight: int=QtGui.QFont.Normal, italic: bool=False,
               capitalization: QtGui.QFont.Capitalization=QtGui.QFont.MixedCase,
               overline: bool=False, underline: bool=False, strikeout: bool=False,
               underline_color: QtGui.QColor=None,
               underline_style: QtGui.QTextCharFormat.UnderlineStyle=QtGui.QTextCharFormat.NoUnderline) \
        -> QtGui.QTextCharFormat:
    format_ = QtGui.QTextCharFormat()
    format_.setForeground(QtGui.QColor(color))
    format_.setFontWeight(weight)
    format_.setFontItalic(italic)
    format_.setFontCapitalization(capitalization)
    format_.setFontOverline(overline)
    format_.setFontUnderline(underline)
    format_.setFontStrikeOut(strikeout)
    if underline_color:
        format_.setUnderlineColor(underline_color)
    format_.setUnderlineStyle(underline_style)
    return format_


class SyntaxHighlightStyles:
    keyword = make_style("yellow")
    operator = make_style("red")
    bracket = make_style("purple")
    identifier = make_style("blue")
    string = make_style("green")
    comment = make_style("gray", italic=True)
    self = make_style("purple", QtGui.QFont.Bold)
    number = make_style("black")


class PythonSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    operators = [
        '=', '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', '//', '%', '**', '^', '|', '&', '~', '<<', '>>',
        '+=', '-=', '*=', '/=', '//=', '%=', '%=', '**=', '^=', '|=', '&=', '~=', '<<=', '>>=', '@', '@='
    ]
    brackets = ['{', '}', '[', ']', '(', ')']
    triple_single = ("'" * 3)
    triple_double = ('"' * 3)

    def __init__(self, style: SyntaxHighlightStyles, parent: QtGui.QTextDocument):
        super().__init__(parent)
        self.style = style
        rules = []
        for kw in kwlist:
            rules.append(((r'\b' + kw + r'\b'), 0, self.style.keyword))
        for op in self.operators:
            rules.append((op, 0, self.style.operator))
        for bracket in self.brackets:
            rules.append((bracket, 0, self.style.bracket))
        rules += [(r'\bself\b', 0, self.style.self),  # self token
                  (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.style.string),  # double quote string
                  (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.style.string),  # single quote string
                  (r'\bdef\b\s*(\w+)', 1, self.style.identifier),  # identifier after function
                  (r'\bclass\b\s*(\w+)', 1, self.style.identifier),  # identifier after class
                  (r'#[^\n]*', 0, self.style.comment),  # comment
                  (r'\b[+-]?([0-9]*\.)?[0-9]+([eE][+-]?[0-9]+)?\b', 0, self.style.number),  # decimal number
                  (r'\b[+-]?0[xX][0-9a-fA-F]+\b', 0, self.style.number),  # hex number
                  (r'\b[+-]?0[bB][01]+\b', 0, self.style.number),  # binary number
                  (r'\b[+-]?0[oO][0-7]+\b', 0, self.style.number),  # octal number
                  ]
        self.rules = [(QtCore.QRegExp(pattern), index, format_) for pattern, index, format_ in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format_ in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format_)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.triple_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.triple_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = text.length() - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        return self.currentBlockState() == in_state
