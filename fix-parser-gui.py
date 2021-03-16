    
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
import xml.etree.ElementTree as ET
import re


class ParseFIX(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.mainframe = tk.Frame(self.root, padx=20, pady=20)
        self.mainframe.pack(fill="both", expand=True)

        self.entry_frame = tk.Frame(master=self.mainframe, padx=5, pady=5, relief=tk.SOLID, borderwidth=1)
        self.entry_frame.pack(anchor="nw")

        data_dictionary_label = tk.Label(master=self.entry_frame, text="Data Dictionary: ", width=12)
        data_dictionary_label.grid(row=0, column=0)
        self.data_dictionary_path = tk.StringVar()
        data_dictionary_path_entry = tk.Entry(master=self.entry_frame, width=100, textvariable=self.data_dictionary_path, disabledbackground="white")
        data_dictionary_path_entry.grid(row=0, column=1)
        data_dictionary_path_entry.configure(state="disabled")
        load_btn = tk.Button(master=self.entry_frame, text="LOAD", command=self.load)
        load_btn.grid(row=0, column=2)

        empty_label = tk.Label(master=self.entry_frame, text ="")
        empty_label.grid(row=1, column=0)

        self.output_notebook = ttk.Notebook(master=self.mainframe)
        self.output_notebook.pack(side="left", fill="both", expand=True)

        # self.output_canvas = tk.Canvas(master=self.output_notebook, highlightthickness=0)
        # self.output_scrollbar = tk.Scrollbar(master=self.mainframe, orient="vertical", command=self.output_canvas.yview)
        # self.output_canvas.configure(yscrollcommand=self.output_scrollbar.set)
        # self.output_scrollbar.pack(side="right", fill="y")

        self.text_box = tk.Text(master=self.entry_frame, width=100, height=10, wrap="none")
        self.text_box.grid(row=6, column=1)
        parse_btn = tk.Button(master=self.entry_frame, text="PARSE", command=self.parse)
        parse_btn.grid(row=7, column=1)


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.output_canvas.configure(scrollregion=self.output_canvas.bbox("all"))


    def load(self):
        filepath = askopenfilename(
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
        )
        tree = ET.parse(filepath)
        root = tree.getroot()
        for child in root:
            if child.tag == "fields":
                self.fields = child
        self.data_dictionary_path.set(filepath)


    def addFIXTab(self, line, tab_name):
        tags_list = re.split("\||\^|", line)
        # output_frame = tk.Frame(master=self.output_canvas, padx=5, pady=5, relief=tk.SOLID, borderwidth=1)
        # self.output_canvas.create_window((4,4), window=output_frame, anchor="nw", tags="output_frame")
        # self.output_notebook.add(output_frame, text="Msg 1")
        output_frame = tk.Frame(master=self.output_notebook)
        self.output_notebook.add(output_frame, text=tab_name)

        header1 = tk.Label(master=output_frame, height=1, text="Tag")
        header2 = tk.Label(master=output_frame, height=1, text="Tag Name")
        header3 = tk.Label(master=output_frame, height=1, text="Value")
        header4 = tk.Label(master=output_frame, height=1, text="Enums")
        header1.grid(row=0, column=0)
        header2.grid(row=0, column=1)
        header3.grid(row=0, column=2)
        header4.grid(row=0, column=3)
        for i in range(1, len(tags_list) + 1):
            pair = tags_list[i - 1].split("=")
            if len(pair) == 1:
                continue

            tag_number = pair[0]
            tag_value = pair[1]

            tag_number_text = tk.Text(master=output_frame, height=1, width=6)
            tag_number_text.insert(tk.END, tag_number)
            tag_number_text.grid(row=i, column=0)

            tag_name = self.fields.find(f"./field[@number='{tag_number}']").get("name")
            tag_name_text = tk.Text(master=output_frame, height=1, width=25)
            tag_name_text.insert(tk.END, tag_name)
            tag_name_text.grid(row=i, column=1)

            tag_value_text = tk.Text(master=output_frame, height=1, width=40)
            tag_value_text.insert(tk.END, tag_value)
            tag_value_text.grid(row=i, column=2)

            field = self.fields.find(f"./field[@number='{tag_number}']")
            enum_arr = []
            list_pos = 0
            for enum in field:
                if enum.get("enum") == tag_value:
                    list_pos = len(enum_arr)
                enum_arr.append(enum.get("enum") + " : " + enum.get("description"))

            if enum_arr:
                combo = ttk.Combobox(master=output_frame, values=enum_arr, state="readonly")
                combo.grid(row=i, column=3)
                meaning = field.find(f"./value[@enum='{tag_value}']")
                enum = " (" + meaning.get("description") + ")"
                combo.current(list_pos)

            tag_number_text.configure(state="disabled")
            tag_name_text.configure(state="disabled")
            tag_value_text.configure(state="disabled")


    def parse(self):
        # for widget in self.output_frame.winfo_children():
        #     widget.destroy()
        input_lines = self.text_box.get("1.0", "end").splitlines()

        for i in range(len(input_lines)):
            self.addFIXTab(input_lines[i], "Msg " + str(i))

        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    ParseFIX(root)
    root.mainloop()
