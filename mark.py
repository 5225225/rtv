import mistune
import sys
import html.parser
import curses

class Color(object):
    """
    Color attributes for curses.
    """

    RED = curses.A_NORMAL
    GREEN = curses.A_NORMAL
    YELLOW = curses.A_NORMAL
    BLUE = curses.A_NORMAL
    MAGENTA = curses.A_NORMAL
    CYAN = curses.A_NORMAL
    WHITE = curses.A_NORMAL

    _colors = {
        'RED': (curses.COLOR_RED, 0),
        'GREEN': (curses.COLOR_GREEN, 0),
        'YELLOW': (curses.COLOR_YELLOW, 0),
        'BLUE': (curses.COLOR_BLUE, 0),
        'MAGENTA': (curses.COLOR_MAGENTA, 0),
        'CYAN': (curses.COLOR_CYAN, 0),
        'WHITE': (curses.COLOR_WHITE, 0),
    }

    @classmethod
    def init(cls):
        """
        Initialize color pairs inside of curses using the default background.

        This should be called once during the curses initial setup. Afterwards,
        curses color pairs can be accessed directly through class attributes.
        """

        for index, (attr, code) in enumerate(cls._colors.items(), start=1):
            print(index)
            print(attr)
            print(code)
            curses.init_pair(index, code[0], code[1])
            setattr(cls, attr, curses.color_pair(index))


class html_parser(html.parser.HTMLParser):

    chunks = []

    tag_stack = []

    counter = 1

    def handle_starttag(self, tag, attrs):
#        print("Encountered a start tag:", tag)
        self.tag_stack.append(tag)
        if tag == "ul":
            self.counter = 1
        elif tag == "li" and self.tag_stack == ["ol", "li"]:
            self.chunks.append(("{}: ".format(self.counter), 0))
            self.counter += 1
        elif tag == "li" and self.tag_stack == ["ul", "li"]:
            self.chunks.append(("* ", 0))

    def handle_endtag(self, tag):
#        print("Encountered an end tag :", tag)
        assert self.tag_stack[-1] == tag
        self.tag_stack.pop()

        if tag in ["p", "h1", "h2", "h3", "h4", "h5", "h6"]:
            self.chunks.append(("\n\n",0))

        elif tag in ["ol", "ul", "li"]:
            self.chunks.append(("\n", 0))


    def handle_data(self, data):
        if data.strip() != "":
            print(data)
            print(self.tag_stack)

            currattr = 0

            if "strong" in self.tag_stack:
                currattr |= curses.A_BOLD
            if "em" in self.tag_stack:
                currattr |= curses.A_UNDERLINE
            if "strikethrough" in self.tag_stack:
                currattr |= curses.A_DIM
            
            self.chunks.append((data, currattr | Color.RED))
    

def format_markdown(md):
    """
    Converts markdown text into a list of tuples of format (text, attr).
    """

    outhtml = mistune.markdown(md)
    print(md)
    print("*"*40)
    print(outhtml)
    print("*"*40)

    parser = html_parser()

    parser.feed(outhtml)

    chunks = parser.chunks

    return chunks

def main(stdscr, chunks):
    Color.init()
    curses.start_color()
    stdscr.clear()

    for text, attr in chunks:
        stdscr.addstr(text, attr)

    stdscr.refresh()

    stdscr.getkey()
    
    

test_markdown_all = """
Numbered list

1. List item 1
2. List item 2
1. List item 3, *wrong* number.

Bulleted list

* Bullet 1
* Bullet 2
* Bullet 3
* Bullet 4 with *italic* text.

Testing headers

#H1

##H2

###H3

####H4

#####H5

######H6

Testing code blocks

    while True:
        print(False)

Testing `inline code`, *italics*, **bold**, ***italics and bold***, ~~strikethrough~~.

Testing non-wrapped paragraph

tahoe apply hotbox curve k9 grape tibia solid abut sepoy katie drill whim blade serve wife paula behind henry enact axes beat awn kw balk mail mno sq serge den ct fate plasm brunch 15 candy tau deus pry 6l

Testing wrapped paragraph.

tahoe apply hotbox curve k9 grape tibia solid abut sepoy katie drill whim blade serve wife paula
behind henry enact axes beat awn kw balk mail mno sq serge den ct fate plasm brunch 15 candy tau
deus pry 6l

"""

small_test = """
This is some *italic* and **bold** text.
"""

chunks = format_markdown(test_markdown_all)

curses.wrapper(main, chunks)

print("*"*40)


