from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageGrab

vers = "1.5"
color = "white"
size = 32

def draw_pix(x, y, color):
    global size
    mul = 256 / size
    view.create_rectangle((x*mul,y*mul),(x*mul+mul,y*mul+mul),fill=color, outline="")

def syntax():
    for tag in editor.tag_names():
        editor.tag_delete(tag)

    editor.tag_config("blue_tag", foreground="#006FFF")
    editor.tag_config("green_tag", foreground="#00FFC6")
    editor.tag_config("orange_tag", foreground="#FF8000")
    editor.tag_config("gray_tag", foreground="gray")

    syntax_tag("pix", "orange_tag", 3)
    syntax_tag("rect", "orange_tag", 4)
    syntax_tag("fill", "green_tag", 4)
    syntax_tag("size", "green_tag", 4)
    syntax_tag("//", "gray_tag", END)
	
    for i in range(10):
        syntax_tag(str(i), "blue_tag", 1)

    root.after(10, syntax)

def syntax_tag(string, tag, offset):
    string_start = editor.search(string, '1.0', END)
    while string_start:
        if string == "//":
            string_end = string_start + " lineend"
        else:
            string_end = string_start + "+" + str(offset) + "c"
        editor.tag_add(tag, string_start, string_end)
        string_start = editor.search(string, string_end, END)

def save(event):
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".jpg")
    except:
        pass
    x=root.winfo_rootx()+view.winfo_x()
    y=root.winfo_rooty()+view.winfo_y()
    x1=x+view.winfo_width()
    y1=y+view.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save(filename)
    root.title("Gedu " + vers + " ~ " + filename)

def run(event):
    global color, size
    color = "white"
    ges = []
    view.delete("all")
    text = editor.get(1.0, END)
    text = list(filter(None, text.split("\n")))
    for line in text:
        if line.lower().islower():
            ges.append(line)
    for line in ges:
        try:
            if line[0:2] == "//":
                pass
            else:
                line = line.split()
                line = "".join(line)
                #print(line)
                splitted = line.split(">")
                if splitted[0] == "pix":
                    draw_pix(int(splitted[1].split(",")[0]), int(splitted[1].split(",")[1]), color)
                elif splitted[0] == "fill":
                    color = splitted[1]
                elif splitted[0] == "rect":
                    for x in range(int(splitted[1].split(",")[0]), int(splitted[1].split(",")[2]) + 1):
                        for y in range(int(splitted[1].split(",")[1]), int(splitted[1].split(",")[3]) + 1):
                            draw_pix(x,y,color)
                elif splitted[0] == "size":
                    size = int(splitted[1])
        except Exception as e:
            console.config(state=NORMAL)
            console.insert(END,"\n" + str(e))
            console.config(state=DISABLED)
            console.see(END)

def clear(event):
    view.delete("all")
    console.config(state=NORMAL)
    console.delete(1.0, END)
    console.insert(1.0, "Gedu ~ Graphic Education\nVersion: " + vers + "\nDeveloper: Flederossi\nF5: Render project")
    console.config(state=DISABLED)

root = Tk()
root.title("Gedu " + vers + " ~ Untitled")
root.geometry("900x700")
root.resizable(0,0)
root.config(bg="#2e2e2e")

root.call('wm', 'iconphoto', root._w, PhotoImage(file='data/Alpha.png'))

root.bind("<F4>", clear)
root.bind("<F5>", run)
root.bind("<Control-s>", save)

img1 = ImageTk.PhotoImage(Image.open("data/view.png"))
img2 = ImageTk.PhotoImage(Image.open("data/code.png"))
img3 = ImageTk.PhotoImage(Image.open("data/console.png"))

#lbl1 = Label(text="Graphicsview", fg="white", bg="#1e1e1e", font="Consolas")
lbl1 = Label(image=img1, borderwidth=0)
lbl1.place(x=23, y=-4)

lbl2 = Label(image=img2, borderwidth=0)
lbl2.place(x=302, y=-4)

#lbl3 = Label(text="Console", fg="white", bg="#1e1e1e", font="Consolas")
lbl3 = Label(image=img3, borderwidth=0)
lbl3.place(x=24, y=284)

editor = Text(width=64, borderwidth=0, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 12), blockcursor=True, selectbackground="gray", spacing1=5)
editor.pack(side=RIGHT, fill=Y, padx=(0, 20), pady=(30, 20))

editor.insert(1.0, "//Gedu ~ Graphic Education\n\n//Setup\nsize > 8\nfill > white\nrect > 0,0,7,7\n\n//Main\n")

editor.focus()

console = Text(bg="#1e1e1e", height=15, width=28, fg="gray", borderwidth=0, font=("Consolas", 12), state=NORMAL, selectbackground="gray", spacing1=5)
console.pack(side=BOTTOM, padx=20, pady=(0, 20))

console.insert(1.0, "Gedu ~ Graphic Education\nVersion: " + vers + "\nDeveloper: Flederossi\nF5: Render project")

console.config(state=DISABLED)

view = Canvas(bg="#1e1e1e", width="256", height="256", highlightthickness=0)
view.pack(side=TOP, padx=20, pady=(30, 0))

img = ImageTk.PhotoImage(Image.open("data/Gedu.png"))
image = Label(image=img, borderwidth=0)
image.place(x=810, y=35)

syntax()

root.mainloop()