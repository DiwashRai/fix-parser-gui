    
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

        data_dictionary_label = tk.Label(master=self.entry_frame, text="Data Dictionary: ", width=25)
        data_dictionary_label.grid(row=0, column=0)
        self.data_dictionary_path = tk.StringVar()
        data_dictionary_path_entry = tk.Entry(master=self.entry_frame, width=100, textvariable=self.data_dictionary_path, disabledbackground="white")
        data_dictionary_path_entry.grid(row=0, column=1)
        data_dictionary_path_entry.configure(state="disabled")
        load_btn = tk.Button(master=self.entry_frame, text="LOAD", command=self.load)
        load_btn.grid(row=1, column=0)

        entry_label1 = tk.Label(master=self.entry_frame, text="FIX String: ", width=25)
        entry_label1.grid(row=2, column=0)
        self.fix_string = tk.StringVar()
        fix_string_entry = tk.Entry(master=self.entry_frame, width=100, textvariable=self.fix_string)
        fix_string_entry.grid(row=2, column=1)
        parse_btn = tk.Button(master=self.entry_frame, text="PARSE", command=self.parse)
        parse_btn.grid(row=3, column=0)

        self.output_canvas = tk.Canvas(master=self.mainframe, highlightthickness=0)
        self.output_frame = tk.Frame(master=self.output_canvas, padx=5, pady=5, relief=tk.SOLID, borderwidth=1)
        self.output_scrollbar = tk.Scrollbar(master=self.mainframe, orient="vertical", command=self.output_canvas.yview)
        self.output_canvas.configure(yscrollcommand=self.output_scrollbar.set)

        self.output_scrollbar.pack(side="right", fill="y")
        self.output_canvas.pack(side="left", fill="both", expand=True)
        self.output_canvas.create_window((4,4), window=self.output_frame, anchor="nw", tags="self.output_frame")
        self.output_frame.bind("<Configure>", self.onFrameConfigure)

        self.fix_string.set("8=FIX.4.4|9=954|35=AE|34=470|49=CMEGROUP|50=STP|52=20200708-21:26:50.297|56=GFE_GFEU1|57=URU27|571=1732375C2B41018D15D462404335766459502|487=0|856=101|568=3|828=0|820=140008662|880=4219245|17=4290:M:1187TN0028998|423=9|55=U07-25:R4TWM6TTV63R|48=U07-25|22=H|454=1|455=9128286F2|456=1|167=REPO|762=SPEC|207=BTUS|107=2_1/2_02/26 REG|916=20200709|917=20200710|711=1|311=[N/A]|810=111.82421875|882=112.625|32=1000|31=1.000000000|75=20200708|715=20200708|442=1|60=20200708-21:07:05.570212592Z|64=20200709|552=1|54=2|37=42202810|11=234|453=5|448=GFEU2|447=D|452=1|802=2|523=AUTO CERT TEST FIRM GFEU2|803=5|523=G8ZTNESVNKW4NN761W05|803=84|448=gfe_btec_qai_us2|447=C|452=7|448=FICC|447=C|452=21|448=URU22|452=44|448=EED|452=55|578=GLBX|921=1126250000.00|922=1126281284.72|1016=1|1012=20200708-21:07:05.570212592Z|1013=1|1057=N|779=20200708-21:07:05.671000000Z|1003=260819|1040=1732375C2B41018D15D48|939=0|1430=E|10026=USD|1832=1|37513=644707884226771825|10053=N|20056=R0000260819|20011=101124|2490=28998|10=176|")


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


    def parse(self):
        fix_str = self.fix_string.get()
        tags_list = re.split("\||\^|", fix_str)
        for i in range(len(tags_list)):
            pair = tags_list[i].split("=")
            if len(pair) == 1:
                continue

            tag_number = pair[0]
            tag_value = pair[1]

            tag_number_text = tk.Text(master=self.output_frame, height=1, width=6)
            tag_number_text.insert(tk.END, tag_number)
            tag_number_text.grid(row=i, column=0)

            tag_name = self.fields.find(f"./field[@number='{tag_number}']").get("name")
            tag_name_text = tk.Text(master=self.output_frame, height=1, width=25)
            tag_name_text.insert(tk.END, tag_name)
            tag_name_text.grid(row=i, column=1)

            tag_value_text = tk.Text(master=self.output_frame, height=1, width=40)
            tag_value_text.insert(tk.END, tag_value)
            tag_value_text.grid(row=i, column=2)

            field = self.fields.find(f"./field[@number='{tag_number}']")
            firstVal = field.find("./value")
            if not firstVal is None:
                meaning = field.find(f"./value[@enum='{tag_value}']")
                if not meaning is None:
                    enum = " (" + meaning.get("description") + ")"
                    combo = ttk.Combobox(master=self.output_frame, values=[tag_value + " : " + enum], state="readonly")
                    combo.current(0)
                    combo.grid(row=i, column=3)

            tag_number_text.configure(state="disabled")
            tag_name_text.configure(state="disabled")
            tag_value_text.configure(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    ParseFIX(root)
    root.mainloop()
