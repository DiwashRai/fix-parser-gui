    
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import xml.etree.ElementTree as ET
import re


class ParseFIX(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.root.geometry("1050x600")
        self.mainframe = tk.Frame(self.root, padx=20, pady=20)
        self.mainframe.pack(fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(master=self.mainframe, padx=5, pady=5)
        self.entry_frame.pack(anchor="nw")

        data_dictionary_label = tk.Label(master=self.entry_frame, text="Data Dictionary: ", width=12)
        data_dictionary_label.grid(row=0, column=0)
        self.data_dictionary_path = tk.StringVar()
        data_dictionary_path_entry = tk.Entry(master=self.entry_frame, width=77, textvariable=self.data_dictionary_path, disabledbackground="white")
        data_dictionary_path_entry.grid(row=0, column=1)
        data_dictionary_path_entry.configure(state="disabled")
        load_btn = ttk.Button(master=self.entry_frame, text="Load", command=self.load_dd)
        load_btn.grid(row=0, column=2)

        empty_label = tk.Label(master=self.entry_frame, text ="")
        empty_label.grid(row=1, column=0)

        text_box_label = tk.Label(master=self.entry_frame, text="Fix Strings: ")
        text_box_label.grid(row=2, column=0, sticky="n")
        load_strings_btn = ttk.Button(master=self.entry_frame, text="Import", command=self.load_fix_file)
        load_strings_btn.grid(row=2, column=2, sticky="n")
        self.text_box = ScrolledText(master=self.entry_frame, width=100, height=10, wrap="none")
        self.text_box.grid(row=2, column=1)
        button_pane = tk.Frame(master=self.entry_frame)
        button_pane.grid(row=3, column=1)
        clear_btn = ttk.Button(master=button_pane, text="Clear", command=self.clear)
        clear_btn.pack(side=tk.LEFT)
        parse_btn = ttk.Button(master=button_pane, text="Parse", command=self.parse)
        parse_btn.pack(side=tk.LEFT)

        search_pane = tk.Frame(master=self.mainframe)
        search_pane.pack()
        self.search_str = tk.StringVar()
        search_entry = tk.Entry(master=search_pane, width=50, textvariable=self.search_str)
        search_entry.pack(side=tk.LEFT)
        search_btn = ttk.Button(master=search_pane, text="Search", command=self.search)
        search_btn.pack(side=tk.LEFT)

        self.output_notebook = ttk.Notebook(master=self.mainframe)
        self.output_notebook.pack(fill=tk.BOTH, expand=True)
        self.text_widget_list = []


    def clear(self):
        self.text_box.delete("1.0", tk.END)


    def search(self):
        search_str = self.search_str.get().lower()
        search_list = [x.strip() for x in search_str.split(",")]
        for search in search_list:
            if not search:
                continue
            for text_widget in self.text_widget_list:
                if text_widget.get("1.0", "end-1c").lower() == search:
                    text_widget.configure(bg="yellow")


    def load_dd(self):
        filepath = askopenfilename(
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        tree = ET.parse(filepath)
        root = tree.getroot()
        for child in root:
            if child.tag == "fields":
                self.fields = child
        self.data_dictionary_path.set(filepath)


    def load_fix_file(self):
        filepath = askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, "r") as input_file:
            line = input_file.readline().lstrip(" ")
            while line:
                if line[0] == "#" or line[0] == "\n":
                    line = input_file.readline().lstrip(" ")
                    continue
                self.text_box.insert(tk.END, line)
                line = input_file.readline().lstrip(" ")



    def add_fix_tab(self, line, tab_name):
        tab_container_frame = tk.Frame(master=self.output_notebook)
        self.output_notebook.add(tab_container_frame, text=tab_name)

        tab_canvas = tk.Canvas(master=tab_container_frame, highlightthickness=0)
        output_frame = tk.Frame(tab_canvas)
        container_scrollbar = tk.Scrollbar(master=tab_container_frame, orient="vertical", command=tab_canvas.yview)
        tab_canvas.configure(yscrollcommand=container_scrollbar.set)
        tab_canvas.bind("<Configure>", lambda e: tab_canvas.config(scrollregion=tab_canvas.bbox(tk.ALL)))

        container_scrollbar.pack(side=tk.RIGHT, fill="y")
        tab_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tab_canvas.create_window((4,4), window=output_frame, anchor="nw")

        header1 = tk.Label(master=output_frame, height=1, text="Tag")
        header2 = tk.Label(master=output_frame, height=1, text="Tag Name")
        header3 = tk.Label(master=output_frame, height=1, text="Value")
        header4 = tk.Label(master=output_frame, height=1, text="Enums")
        header1.grid(row=0, column=0)
        header2.grid(row=0, column=1)
        header3.grid(row=0, column=2)
        header4.grid(row=0, column=3)

        tags_list = re.split("\||\^|", line)
        for i in range(1, len(tags_list) + 1):
            pair = tags_list[i - 1].split("=")
            if len(pair) == 1:
                continue

            tag_number = pair[0]
            tag_value = pair[1]

            tag_number_text = tk.Text(master=output_frame, height=1, width=6)
            self.text_widget_list.append(tag_number_text)
            tag_number_text.insert(tk.END, tag_number)
            tag_number_text.grid(row=i, column=0)

            tag_name = self.fields.find(f"./field[@number='{tag_number}']").get("name")
            tag_name_text = tk.Text(master=output_frame, height=1, width=25)
            self.text_widget_list.append(tag_name_text)
            tag_name_text.insert(tk.END, tag_name)
            tag_name_text.grid(row=i, column=1)

            tag_value_text = tk.Text(master=output_frame, height=1, width=40)
            self.text_widget_list.append(tag_value_text)
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
                combo = ttk.Combobox(master=output_frame, values=enum_arr, state="readonly", width=40)
                combo.grid(row=i, column=3)
                meaning = field.find(f"./value[@enum='{tag_value}']")
                enum = " (" + meaning.get("description") + ")"
                combo.current(list_pos)

            tag_number_text.configure(state="disabled")
            tag_name_text.configure(state="disabled")
            tag_value_text.configure(state="disabled")


    def parse(self):
        self.text_widget_list = []
        for child in self.output_notebook.winfo_children():
            child.destroy()
        while self.output_notebook.tabs():
            self.output_notebook.forget(0)
        input_lines = self.text_box.get("1.0", "end").splitlines()

        tab_number = 1
        for line in input_lines:
            if not line or line[0] == "#":
                continue

            self.add_fix_tab(line, "Msg " + str(tab_number))
            tab_number += 1


if __name__ == "__main__":
    root = tk.Tk(className="FIX Parser GUI")
    ParseFIX(root)
    root.mainloop()
