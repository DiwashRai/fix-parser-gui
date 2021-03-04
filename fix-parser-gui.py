
import tkinter as tk
import re


class ParseFIX(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.mainframe = tk.Frame(self.root, padx=20, pady=20)
        self.mainframe.pack(fill="both", expand=True)

        self.entry_frame = tk.Frame(master=self.mainframe, padx=5, pady=5, relief=tk.SOLID, borderwidth=1)
        self.entry_frame.pack(anchor="nw")

        entry_label1 = tk.Label(master=self.entry_frame, text="FIX String: ", width=25)
        entry_label1.grid(row=0, column=0)
        self.fix_string = tk.StringVar()
        fix_string_entry = tk.Entry(master=self.entry_frame, width=100, textvariable=self.fix_string)
        fix_string_entry.grid(row=0, column=1)
        parse_btn = tk.Button(master=self.entry_frame, text="PARSE", command=self.parse)
        parse_btn.grid(row=1, column=0)

        self.output_canvas = tk.Canvas(master=self.mainframe, highlightthickness=0)
        self.output_frame = tk.Frame(master=self.output_canvas, padx=5, pady=5, relief=tk.SOLID, borderwidth=1)
        self.output_scrollbar = tk.Scrollbar(master=self.mainframe, orient="vertical", command=self.output_canvas.yview)
        self.output_canvas.configure(yscrollcommand=self.output_scrollbar.set)

        self.output_scrollbar.pack(side="right", fill="y")
        self.output_canvas.pack(side="left", fill="both", expand=True)
        self.output_canvas.create_window((4,4), window=self.output_frame, anchor="nw", tags="self.output_frame")
        self.output_frame.bind("<Configure>", self.onFrameConfigure)

        self.parse()


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.output_canvas.configure(scrollregion=self.output_canvas.bbox("all"))


    def parse(self):
        # fix_str = self.fix_string.get()
        fix_str = "8=FIX.4.19=6135=A34=149=EXEC52=20121105-23:24:0656=BANZAI98=0108=3010=0038=FIX.4.19=6135=A34=149=BANZAI52=20121105-23:24:0656=EXEC98=0108=3010=0038=FIX.4.19=4935=034=249=BANZAI52=20121105-23:24:3756=EXEC10=2288=FIX.4.19=4935=034=249=EXEC52=20121105-23:24:3756=BANZAI10=2288=FIX.4.19=10335=D34=349=BANZAI52=20121105-23:24:4256=EXEC11=135215788257721=138=1000040=154=155=MSFT59=010=0628=FIX.4.19=13935=834=349=EXEC52=20121105-23:24:4256=BANZAI6=011=135215788257714=017=120=031=032=037=138=1000039=054=155=MSFT150=2151=010=0598=FIX.4.19=15335=834=449=EXEC52=20121105-23:24:4256=BANZAI6=12.311=135215788257714=1000017=220=031=12.332=1000037=238=1000039=254=155=MSFT150=2151=010=2308=FIX.4.19=10335=D34=449=BANZAI52=20121105-23:24:5556=EXEC11=135215789503221=138=1000040=154=155=ORCL59=010=0478=FIX.4.19=13935=834=549=EXEC52=20121105-23:24:5556=BANZAI6=011=135215789503214=017=320=031=032=037=338=1000039=054=155=ORCL150=2151=010=0498=FIX.4.19=15335=834=649=EXEC52=20121105-23:24:5556=BANZAI6=12.311=135215789503214=1000017=420=031=12.332=1000037=438=1000039=254=155=ORCL150=2151=010=2208=FIX.4.19=10835=D34=549=BANZAI52=20121105-23:25:1256=EXEC11=135215791235721=138=1000040=244=1054=155=SPY59=010=0038=FIX.4.19=13835=834=749=EXEC52=20121105-23:25:1256=BANZAI6=011=135215791235714=017=520=031=032=037=538=1000039=054=155=SPY150=2151=010=2528=FIX.4.19=10435=F34=649=BANZAI52=20121105-23:25:1656=EXEC11=135215791643738=1000041=135215791235754=155=SPY10=1988=FIX.4.19=8235=334=849=EXEC52=20121105-23:25:1656=BANZAI45=658=Unsupported message type10=0008=FIX.4.19=10435=F34=749=BANZAI52=20121105-23:25:2556=EXEC11=135215792530938=1000041=135215791235754=155=SPY10=1978=FIX.4.19=8235=334=949=EXEC52=20121105-23:25:2556=BANZAI45=758=Unsupported message type10=002"
        tags_list = re.split("\||\^|", fix_str)
        for i in range(len(tags_list)):
            pair = tags_list[i].split("=")
            print(pair)
            if len(pair) == 1:
                continue

            tag_number = pair[0]
            tag_value = pair[1]

            entry1 = tk.Entry(master=self.output_frame)
            entry1.insert(0, tag_number)
            entry1.grid(row=i, column=0)
            entry2 = tk.Entry(master=self.output_frame)
            entry2.insert(0, tag_value)
            entry2.grid(row=i, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    ParseFIX(root)
    root.mainloop()
