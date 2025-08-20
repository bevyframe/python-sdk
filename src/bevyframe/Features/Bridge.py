class JavaScript:
    def __init__(self, script: str | object | list = None, src: str = None) -> None:
        if src:
            self.src = src
            self.script = ""
            return
        self.src = None
        if isinstance(script, list):
            script = ''.join([
                str(i)
                for i in script
            ])
        self.script: str = script

    def bf_widget(self) -> list[str | dict | list]:
        return ['script', {"src": self.src} if self.src else {}, [self.script]]

    def __repr__(self) -> str:
        return self.script

    def __str__(self) -> str:
        return self.script


class change_html:
    def __init__(self, tag: str, html) -> None:
        self.tag: str = tag
        self.html = html
        if hasattr(self.html, "bf_widget"):
            self.html = self.html.bf_widget()
        elif isinstance(self.html, list):
            l = self.html
            self.html = []
            for html in l:
                if hasattr(html, "bf_widget"):
                    self.html += [html.bf_widget()]
                else:
                    self.html += [html]

    def __dict__(self) -> dict:
        return {self.tag: self.html}
