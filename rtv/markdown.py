import curses
import mistune
import html.parser

from .objects import Color

class html_parser(html.parser.HTMLParser):

    chunks = []

    tag_stack = []

    counter = 1

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == "ul":
            self.counter = 1
        elif tag == "li" and self.tag_stack == ["ol", "li"]:
            self.chunks.append(("{}: ".format(self.counter), 0))
            self.counter += 1
        elif tag == "li" and self.tag_stack == ["ul", "li"]:
            self.chunks.append(("* ", 0))

    def handle_endtag(self, tag):
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
