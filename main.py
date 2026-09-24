import tkinter as tk
import random

W, H = 360, 420
GROUND = H - 28

class Ben10Pet:
    def __init__(self, root):
        self.root = root
        root.title('Ben 10 Desktop Pet')
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-transparentcolor', '#101010')
        root.configure(bg='#101010')
        self.canvas = tk.Canvas(root, width=W, height=H, bg='#101010', highlightthickness=0)
        self.canvas.pack()
        self.x, self.y = 80, 80
        self.dx = 2
        self.mode = 'ben'
        self.frame = 0
        self.transform_frame = 0
        self.drag = None
        self.canvas.bind('<ButtonPress-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.drag_window)
        self.canvas.bind('<Button-3>', lambda e: root.destroy())
        self.canvas.bind('<Double-Button-1>', lambda e: self.transform())
        root.bind('<space>', lambda e: self.transform())
        self.animate()

    def start_drag(self, event):
        self.drag = (event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y())

    def drag_window(self, event):
        if self.drag:
            self.root.geometry(f'+{event.x_root-self.drag[0]}+{event.y_root-self.drag[1]}')

    def transform(self):
        if self.mode == 'transform':
            return
        self.mode = 'transform'
        self.transform_frame = 0

    def draw_omnitrix(self, x, y, glow=False):
        color = '#baff00' if glow else '#202020'
        self.canvas.create_oval(x-13, y-8, x+13, y+8, fill=color, outline='#9cff00', width=2)
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='#111111', outline='#ffffff')
        self.canvas.create_line(x-2, y-3, x+3, y+3, fill='#9cff00', width=2)

    def draw_ben(self):
        x, y = 180, GROUND-100
        # head, hair, shirt, arms, legs; deliberately simple original vector art
        self.canvas.create_oval(x-22, y-78, x+22, y-34, fill='#f0b184', outline='#202020')
        self.canvas.create_arc(x-23, y-84, x+23, y-35, start=0, extent=180, fill='#202020', outline='#202020')
        self.canvas.create_rectangle(x-25, y-34, x+25, y+25, fill='#242424', outline='#101010')
        self.canvas.create_rectangle(x-19, y-28, x+19, y+19, fill='#e8e8e8', outline='#e8e8e8')
        self.canvas.create_rectangle(x-19, y-28, x+19, y-2, fill='#252525', outline='#252525')
        self.canvas.create_line(x-25, y-25, x-49, y+8, fill='#f0b184', width=11)
        self.canvas.create_line(x+25, y-25, x+49, y+8, fill='#f0b184', width=11)
        self.draw_omnitrix(x-48, y+1)
        self.canvas.create_line(x-10, y+25, x-16, y+72, fill='#252525', width=13)
        self.canvas.create_line(x+10, y+25, x+16, y+72, fill='#252525', width=13)
        self.canvas.create_line(x-20, y+75, x-5, y+75, fill='#ffffff', width=7)
        self.canvas.create_line(x+5, y+75, x+20, y+75, fill='#ffffff', width=7)

    def draw_heatblast(self):
        x, y = 180, GROUND-100
        pulse = 8 + (self.transform_frame % 10)
        self.canvas.create_oval(x-40-pulse, y-105-pulse, x+40+pulse, y+85+pulse, fill='#ff6a00', outline='#baff00', width=3)
        self.canvas.create_polygon(x-28,y-45, x-50,y-100, x-18,y-78, x,y-125, x+18,y-78, x+50,y-100, x+28,y-45, fill='#ff9d00', outline='#ffdf38')
        self.canvas.create_oval(x-25, y-75, x+25, y-25, fill='#ffb12b', outline='#ffdf38')
        self.canvas.create_rectangle(x-28, y-25, x+28, y+38, fill='#d93600', outline='#ffdf38')
        self.canvas.create_line(x-28, y-18, x-55, y+15, fill='#ffb12b', width=14)
        self.canvas.create_line(x+28, y-18, x+55, y+15, fill='#ffb12b', width=14)
        self.canvas.create_line(x-12, y+38, x-20, y+78, fill='#d93600', width=15)
        self.canvas.create_line(x+12, y+38, x+20, y+78, fill='#d93600', width=15)

    def animate(self):
        self.canvas.delete('all')
        if self.mode == 'ben':
            self.draw_ben()
        elif self.mode == 'transform':
            self.transform_frame += 1
            if self.transform_frame < 18:
                self.draw_ben()
                self.draw_omnitrix(132, GROUND-99, glow=True)
                self.canvas.create_oval(80, 90, 280, 300, outline='#baff00', width=4)
            else:
                self.mode = 'heatblast'
                self.transform_frame = 0
                self.draw_heatblast()
        else:
            self.transform_frame += 1
            self.draw_heatblast()
            if self.transform_frame > 180:
                self.mode = 'ben'
                self.transform_frame = 0
        self.canvas.create_text(8, 8, anchor='nw', text='Double-click / SPACE: Transform | Right-click: Exit', fill='#baff00', font=('Segoe UI', 8))
        self.root.after(70, self.animate)

if __name__ == '__main__':
    root = tk.Tk()
    app = Ben10Pet(root)
    root.mainloop()
