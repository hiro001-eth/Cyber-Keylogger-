# ui/widgets/rounded_button.py

import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, radius, bg, fg, text, command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, relief="flat", highlightthickness=0)
        self.command = command
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.width = width
        self.height = height
        self.create_rounded_rect(0, 0, width, height, radius, fill=bg)
        self.text_id = self.create_text(width//2, height//2, text=text, fill=fg, font=("Arial", 12, "bold"))
        self.bind("<ButtonPress-1>", self._on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event):
        if self.command:
            self.command()
