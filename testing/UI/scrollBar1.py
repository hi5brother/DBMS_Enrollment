#Testing a scroll bar with checkbuttons

import Tkinter as tk

root = tk.Tk()  
vsb = tk.Scrollbar(orient="vertical")
text = tk.Text(root, width=40, height=20, yscrollcommand=vsb.set)
vsb.config(command=text.yview)
vsb.pack(side="right",fill="y")
text.pack(side="top",fill="both",expand=True)
for i in range(1000):
	bg = 'grey'
	if i % 2 == 0:
		bg = 'white'
	cb = tk.Checkbutton(text="checkbutton #%s" % i, bg=bg, width=40, justify=tk.LEFT)
	text.window_create("end", window=cb)

	cb.bind('<Button-4>', lambda event: text.yview_scroll(-1, tk.UNITS))
	cb.bind('<Button-5>', lambda event: text.yview_scroll( 1, tk.UNITS))

	text.insert("end", "\n") # to force one checkbox per line

root.mainloop()