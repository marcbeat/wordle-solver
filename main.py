import json
import re
from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title("Wordle lösen")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=2, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

richtigframe = ttk.Frame(mainframe)
richtigframe.grid(column=1, row=0, rowspan=2, columnspan=2, sticky=(N, W, E, S))

# loader = ttk.Progressbar(mainframe, mode='indeterminate')
# loader.grid(column=0, row=6)

# Specify the path to your JSON file
json_file_path = 'german-words.json'


# Function to filter data based on the length of the 'word' key
def filter_data(word_value):
    # Implement your filtering logic here
    # For example, filter items where the length of 'word' is less than or equal to 5 and does not contain umlaute
    return len(str(word_value)) <= 5 and not re.search(r'[äöüßÄÖÜéèêùùûòóôáàâ]', word_value)

# Function to query the filtered data with a regular expression
def query_data(filtered_data, regex, needed_letters):
    # Return a subarray with matching strings
    regex_search = [item for item in filtered_data if re.search(regex, str(item))]
    if len(needed_letters) == 0:
        return regex_search
    else:
        return [item for item in regex_search if
                all(letter in item for letter in needed_letters)]

# Open the JSON file and read it line by line
filtered_data = []
def load_file():
    global laden_btt
    global such_btt
    global filtered_data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        # Initialize an empty list to store filtered data
        filtered_data = []

        for line in file:
            # Load JSON from the current line
            data = json.loads(line)

            # Get the value of the 'word' key
            word_value = str(data.get('word', None)).lower()

            # Check if the 'word' value meets the filtering criteria
            if word_value is not None and filter_data(word_value):
                # Add the 'word' value to the filtered data list
                filtered_data.append(word_value)
        
        filtered_data = list(set(filtered_data)) # Eliminate duplicates
        # Now, 'filtered_data' contains the filtered 'word' values from the entire JSON file
    messagebox.showinfo("Wörterbuch geladen", str(len(filtered_data)) + " Wörter wurden geladen.")

start_wort = 'adieu'
iterationen = 0

label_pos = ttk.Label(mainframe, text='Richtige Stelle:').grid(column=0, row=0, sticky=E)
richtig_1_var = StringVar()
richtig_2_var = StringVar()
richtig_3_var = StringVar()
richtig_4_var = StringVar()
richtig_5_var = StringVar()
richtig_1 = ttk.Entry(richtigframe, textvariable=richtig_1_var, width=3).grid(column=0, row=0, sticky=W)
richtig_2 = ttk.Entry(richtigframe, textvariable=richtig_2_var, width=3).grid(column=1, row=0, sticky=W)
richtig_3 = ttk.Entry(richtigframe, textvariable=richtig_3_var, width=3).grid(column=2, row=0, sticky=W)
richtig_4 = ttk.Entry(richtigframe, textvariable=richtig_4_var, width=3).grid(column=3, row=0, sticky=W)
richtig_5 = ttk.Entry(richtigframe, textvariable=richtig_5_var, width=3).grid(column=4, row=0, sticky=W)
label_pos_falsch = ttk.Label(mainframe, text='Falsche Stelle:').grid(column=0, row=1, sticky=E)
falsch_1_var = StringVar()
falsch_2_var = StringVar()
falsch_3_var = StringVar()
falsch_4_var = StringVar()
falsch_5_var = StringVar()
falsch_1 = ttk.Entry(richtigframe, textvariable=falsch_1_var, width=3).grid(column=0, row=1, sticky=W)
falsch_2 = ttk.Entry(richtigframe, textvariable=falsch_2_var, width=3).grid(column=1, row=1, sticky=W)
falsch_3 = ttk.Entry(richtigframe, textvariable=falsch_3_var, width=3).grid(column=2, row=1, sticky=W)
falsch_4 = ttk.Entry(richtigframe, textvariable=falsch_4_var, width=3).grid(column=3, row=1, sticky=W)
falsch_5 = ttk.Entry(richtigframe, textvariable=falsch_5_var, width=3).grid(column=4, row=1, sticky=W)


neue_woerter = StringVar()
label_ausg = ttk.Label(mainframe, text='Ausgeschlossen:').grid(column=0, row=2, sticky=E)
ausgeschlossen = StringVar()
ausgeschlossen_ent = ttk.Entry(mainframe, textvariable=ausgeschlossen).grid(column=1, row=2, sticky=W)
label_regex = ttk.Label(mainframe, text='Regex:').grid(column=0, row=4, sticky=E)
regex_var = StringVar()
regex_ent = ttk.Entry(mainframe, textvariable=regex_var, state=DISABLED).grid(column=1, row=4, sticky=W)
label_needed = ttk.Label(mainframe, text='Beinhaltet:').grid(column=0, row=3, sticky=E)
needed_var = StringVar()
needed_ent = ttk.Entry(mainframe, textvariable=needed_var, state=DISABLED).grid(column=1, row=3, sticky=W)
label_vorschlaege = ttk.Label(mainframe, text='Vorschläge:').grid(column=0, row=5, sticky=NE)
listb = Listbox(mainframe, height=10, listvariable=neue_woerter).grid(column=1, row=5, sticky=W)
# lbl_buch = ttk.Label(mainframe, text='Wörter geladen: 0').grid(column=2, row=5, sticky=W)

def calculate(*args):
    global iterationen
    global start_wort
    global needed_letters
    global filtered_data
    if iterationen == 0 and len(ausgeschlossen.get()) == 0 and len(richtig_1_var.get()) == 0 and len(richtig_2_var.get()) == 0 \
        and len(richtig_3_var.get()) == 0  and len(richtig_4_var.get()) == 0  and len(richtig_5_var.get()) == 0 \
        and len(falsch_1_var.get()) == 0 and len(falsch_2_var.get()) == 0 \
        and len(falsch_3_var.get()) == 0  and len(falsch_4_var.get()) == 0  and len(falsch_5_var.get()) == 0:
        neue_woerter.set(start_wort)
        regex_var.set('')
    else:
        needed_letters = []
        if len(falsch_1_var.get()) != 0:
            needed_letters.append(falsch_1_var.get())
        if len(falsch_2_var.get()) != 0:
            needed_letters.append(falsch_2_var.get())
        if len(falsch_3_var.get()) != 0:
            needed_letters.append(falsch_3_var.get())
        if len(falsch_4_var.get()) != 0:
            needed_letters.append(falsch_4_var.get())
        if len(falsch_5_var.get()) != 0:
            needed_letters.append(falsch_5_var.get())
        
        r1 = ''
        r2 = ''
        r3 = ''
        r4 = ''
        r5 = ''
        a1 = ''
        a2 = ''
        a3 = ''
        a4 = ''
        a5 = ''
        if len(richtig_1_var.get()) != 0:
            r1 = re.escape(richtig_1_var.get())
        else:
            if len(ausgeschlossen.get()) != 0 or len(falsch_1_var.get()) != 0:
                a1 = r'[^' + re.escape(ausgeschlossen.get()) + re.escape(falsch_1_var.get()) + r']'
            else:
                a1 = '\w'
        if len(richtig_2_var.get()) != 0:
            r2 = re.escape(richtig_2_var.get())
        else:
            if len(ausgeschlossen.get()) != 0 or len(falsch_2_var.get()) != 0:
                a2 = r'[^' + re.escape(ausgeschlossen.get()) + re.escape(falsch_2_var.get()) + r']'
            else:
                a2 = '\w'
        if len(richtig_3_var.get()) != 0:
            r3 = re.escape(richtig_3_var.get())
        else:
            if len(ausgeschlossen.get()) != 0 or len(falsch_3_var.get()) != 0:
                a3 = r'[^' + re.escape(ausgeschlossen.get()) + re.escape(falsch_3_var.get()) + r']'
            else:
                a3 = '\w'
        if len(richtig_4_var.get()) != 0:
            r4 = re.escape(richtig_4_var.get())
        else:
            if len(ausgeschlossen.get()) != 0 or len(falsch_4_var.get()) != 0:
                a4 = r'[^' + re.escape(ausgeschlossen.get()) + re.escape(falsch_4_var.get()) + r']'
            else:
                a4 = '\w'
        if len(richtig_5_var.get()) != 0:
            r5 = re.escape(richtig_5_var.get())
        else:
            if len(ausgeschlossen.get()) != 0 or len(falsch_5_var.get()) != 0:
                a5 = r'[^' + re.escape(ausgeschlossen.get()) + re.escape(falsch_5_var.get()) + r']'
            else:
                a5 = '\w'
        regex_pattern = r'^' + r1 + a1 + r2 + a2 + r3 + a3 + r4 + a4 + r5 + a5 + r'$'
        regex_var.set(str(regex_pattern))
        needed_var.set(','.join(needed_letters))
        matched_strings = query_data(filtered_data, regex_pattern, needed_letters)
        neue_woerter.set(matched_strings)

def reset_form():
    richtig_1_var.set('')
    richtig_2_var.set('')
    richtig_3_var.set('')
    richtig_4_var.set('')
    richtig_5_var.set('')
    falsch_1_var.set('')
    falsch_2_var.set('')
    falsch_3_var.set('')
    falsch_4_var.set('')
    falsch_5_var.set('')
    ausgeschlossen.set('')
    needed_var.set('')


such_btt = ttk.Button(mainframe, text="Suchen", command=calculate).grid(column=2, row=6, sticky=E)
laden_btt = ttk.Button(mainframe, text="Laden", command=load_file).grid(column=1, row=6, sticky=E)
erneut_btt = ttk.Button(mainframe, text="Erneut", command=reset_form).grid(column=0, row=6, sticky=W)

richtig_1_var.trace_add("write", calculate)
richtig_2_var.trace_add("write", calculate)
richtig_3_var.trace_add("write", calculate)
richtig_4_var.trace_add("write", calculate)
richtig_5_var.trace_add("write", calculate)

falsch_1_var.trace_add("write", calculate)
falsch_2_var.trace_add("write", calculate)
falsch_3_var.trace_add("write", calculate)
falsch_4_var.trace_add("write", calculate)
falsch_5_var.trace_add("write", calculate)

ausgeschlossen.trace_add("write", calculate)



for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
for child in richtigframe.winfo_children(): 
    child.grid_configure(padx=1,pady=5)

root.bind("<Return>", calculate)

root.mainloop()