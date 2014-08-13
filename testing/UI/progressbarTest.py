# import Tkinter
# import ttk

# def main():
# 	root = Tkinter.Tk()

# 	ft = ttk.Frame()
# 	fb = ttk.Frame()
# 	ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
# 	fb.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

# 	pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')


# 	pb_hD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

# 	pb_hD.start(50)


# 	root.mainloop()


# if __name__ == '__main__':
# 	main()

import Tkinter
import webbrowser

class App:
    def __init__(self, root):
        self.root = root
        for text in ("link1", "link2", "link3"):
            link = Tkinter.Text(self.root,height = 22, width =40)
            link.pack(side = LEFT)
            link.insert(END, text)
            link.bind("<1>", lambda event, text=text: \
                          self.click_link(event, text))
            link.pack()
    def click_link(self, event, text):
        webbrowser.open_new_tab("https://github.com/hi5brother/DBMS_Enrollment")

root=Tkinter.Tk()
app = App(root)
root.mainloop()