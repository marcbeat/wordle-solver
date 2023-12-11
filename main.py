import json
from tkinter import *
from tkinter import ttk, messagebox

root = Tk()
root.title("Wordle lösen")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=2, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

rf_frame = ttk.Frame(mainframe)
rf_frame.grid(column=1, row=0, rowspan=2, columnspan=2, sticky=(N, W, E, S))

json_pfad = 'dict.json'

wortliste = []

def load_file():
    global laden_btt
    global such_btt
    global wortliste
    with open(json_pfad, 'r', encoding='utf-8') as file:
        # Initialize an empty list to store filtered data
        wortliste = json.load(file)
    woerter_anzahl = len(wortliste)
    woerter_anzahl_var.set('Wörter geladen: ' + str(woerter_anzahl))
    # messagebox.showinfo("Wörterbuch geladen", str(len(wortliste)) + " Wörter wurden geladen.")

start_wort = 'adieu'
passende_woerter = [start_wort]

r_lbl = ttk.Label(mainframe, text='Richtige Stelle:')
r_lbl.grid(column=0, row=0, sticky=E)
r1_var = StringVar()
r2_var = StringVar()
r3_var = StringVar()
r4_var = StringVar()
r5_var = StringVar()
r1_entry = ttk.Entry(rf_frame, textvariable=r1_var, width=3)
r1_entry.grid(column=0, row=0, sticky=W)
r2_entry = ttk.Entry(rf_frame, textvariable=r2_var, width=3)
r2_entry.grid(column=1, row=0, sticky=W)
r3_entry = ttk.Entry(rf_frame, textvariable=r3_var, width=3)
r3_entry.grid(column=2, row=0, sticky=W)
r4_entry = ttk.Entry(rf_frame, textvariable=r4_var, width=3)
r4_entry.grid(column=3, row=0, sticky=W)
r5_entry = ttk.Entry(rf_frame, textvariable=r5_var, width=3)
r5_entry.grid(column=4, row=0, sticky=W)

f_lbl = ttk.Label(mainframe, text='Falsche Stelle:')
f_lbl.grid(column=0, row=1, sticky=E)
f1_var = StringVar()
f2_var = StringVar()
f3_var = StringVar()
f4_var = StringVar()
f5_var = StringVar()
f1_entry = ttk.Entry(rf_frame, textvariable=f1_var, width=3)
f1_entry.grid(column=0, row=1, sticky=W)
f2_entry = ttk.Entry(rf_frame, textvariable=f2_var, width=3)
f2_entry.grid(column=1, row=1, sticky=W)
f3_entry = ttk.Entry(rf_frame, textvariable=f3_var, width=3)
f3_entry.grid(column=2, row=1, sticky=W)
f4_entry = ttk.Entry(rf_frame, textvariable=f4_var, width=3)
f4_entry.grid(column=3, row=1, sticky=W)
f5_entry = ttk.Entry(rf_frame, textvariable=f5_var, width=3)
f5_entry.grid(column=4, row=1, sticky=W)

nt_lbl = ttk.Label(mainframe, text='Ausgeschlossen:').grid(column=0, row=2, sticky=E)
nt_var = StringVar()
nt_entry = ttk.Entry(mainframe, textvariable=nt_var)
nt_entry.grid(column=1, row=2, sticky=W)

vorschlaege_lbl = ttk.Label(mainframe, text='Vorschläge:').grid(column=0, row=5, sticky=NE)
vorschlaege_var = StringVar()
vorschlaege_var.set([start_wort])
vorschlaege_lstbx = Listbox(mainframe, height=10, listvariable=vorschlaege_var)
vorschlaege_lstbx.grid(column=1, row=5, sticky=W)

gefunden_var = StringVar()
gefunden_var.set('Gefunden: ' + str(len(passende_woerter)))
gefunden_lbl = ttk.Label(mainframe, textvariable=gefunden_var)
gefunden_lbl.grid(column=1, row=6, sticky=NW)

woerter_anzahl = 0
woerter_anzahl_var = StringVar()
woerter_anzahl_var.set('Wörter geladen: ' + str(woerter_anzahl))
anzahl_lbl = ttk.Label(mainframe, textvariable=woerter_anzahl_var)
anzahl_lbl.grid(column=0, row=8, sticky=W)

iterationen = 0
iterationen_var = StringVar()
iterationen_var.set('Suchvorgänge: ' + str(iterationen))
iterationen_lbl = ttk.Label(mainframe, textvariable=iterationen_var)
iterationen_lbl.grid(column=1, row=8, sticky=E)


def wort_wert(wort):
    # Berechne gewichteten Wert anhand Buchstaben in einem Wort
    vokale = ['a', 'e', 'i', 'o', 'u']
    vokal_gewicht = 2
    buchstaben_stat = { # Prozentualer anteil
        'e': 0.1740,
        'n': 0.978,
        'i': 0.755,
        's': 0.727,
        'r': 0.700,
        'a': 0.651,
        't': 0.615,
        'd': 0.508,
        'h': 0.476,
        'u': 0.435,
        'l': 0.344,
        'c': 0.306,
        'g': 0.301,
        'm': 0.253,
        'o': 0.251,
        'b': 0.189,
        'w': 0.189,
        'f': 0.166,
        'k': 0.121,
        'z': 0.113,
        'p': 0.079,
        'v': 0.067,
        # 'ß': 0.031,
        'j': 0.027,
        'y': 0.004,
        'x': 0.003,
        'q': 0.002,
    }

    wert = 0.00
    for buchstabe in wort:
        gewichtung = 1
        if buchstabe in vokale:
            gewichtung = vokal_gewicht
        wert += (buchstaben_stat[buchstabe] * gewichtung)
    return wert


def filtern(woerter):
    gefiltert = woerter

    # Textfelder auslesen
    ## Buchstaben an der richtigen Stelle
    r1 = r1_var.get()
    r2 = r2_var.get()
    r3 = r3_var.get()
    r4 = r4_var.get()
    r5 = r5_var.get()
    ## Buchstaben an der falschen Stelle
    f1 = f1_var.get()
    f2 = f2_var.get()
    f3 = f3_var.get()
    f4 = f4_var.get()
    f5 = f5_var.get()
    ## Buchstaben ausgeschlossen
    nt = nt_var.get()

    # Richtig positionierte Buchstaben filtern
    if len(r1) > 0:
        gefiltert = [wort for wort in gefiltert if wort[0] == r1.lower()]
    if len(r2) > 0:
        gefiltert = [wort for wort in gefiltert if wort[1] == r2.lower()]
    if len(r3) > 0:
        gefiltert = [wort for wort in gefiltert if wort[2] == r3.lower()]
    if len(r4) > 0:
        gefiltert = [wort for wort in gefiltert if wort[3] == r4.lower()]
    if len(r5) > 0:
        gefiltert = [wort for wort in gefiltert if wort[4] == r5.lower()]
    # Falsch positionierte Buchstaben filtern
    if len(f1) > 0:
        gefiltert = [wort for wort in gefiltert if wort[0] not in f1.lower()]
        gefiltert = [wort for wort in gefiltert if all(buchstabe in wort for buchstabe in f1.lower())]
    if len(f2) > 0:
        gefiltert = [wort for wort in gefiltert if wort[1] not in f2.lower()]
        gefiltert = [wort for wort in gefiltert if all(buchstabe in wort for buchstabe in f2.lower())]
    if len(f3) > 0:
        gefiltert = [wort for wort in gefiltert if wort[2] not in f3.lower()]
        gefiltert = [wort for wort in gefiltert if all(buchstabe in wort for buchstabe in f3.lower())]
    if len(f4) > 0:
        gefiltert = [wort for wort in gefiltert if wort[3] not in f4.lower()]
        gefiltert = [wort for wort in gefiltert if all(buchstabe in wort for buchstabe in f4.lower())]
    if len(f5) > 0:
        gefiltert = [wort for wort in gefiltert if wort[4] not in f5.lower()]
        gefiltert = [wort for wort in gefiltert if all(buchstabe in wort for buchstabe in f5.lower())]    

    # Ausgeschlossene Buchstaben filtern
    if len(nt) > 0:
        gefiltert_temp = []
        for wort in gefiltert:
            wort_gefiltert = wort
            buchstabe_in_wort = False
            for buchstabe in nt:
                if buchstabe == r1.lower():
                    wort_gefiltert = '_' + wort_gefiltert[1:]
                if buchstabe == r2.lower():
                    wort_gefiltert = wort_gefiltert[0] + '_' + wort_gefiltert[2:]
                if buchstabe == r3.lower():
                    wort_gefiltert = wort_gefiltert[:1] + '_' + wort_gefiltert[3:]
                if buchstabe == r4.lower():
                    wort_gefiltert = wort_gefiltert[:2] + '_' + wort_gefiltert[4]
                if buchstabe == r4.lower():
                    wort_gefiltert = wort_gefiltert[:3] + '_'
                
                wort_gefiltert.replace('_', '')

                if buchstabe in wort_gefiltert:
                    buchstabe_in_wort = True
            
            if not buchstabe_in_wort:
                gefiltert_temp.append(wort)
        
        gefiltert = gefiltert_temp
        # gefiltert = [wort for wort in gefiltert if not any(buchstabe in nt for buchstabe in wort)]

    gefiltert.sort(key=wort_wert, reverse=True)
    return gefiltert

def suchen(*args):
    global iterationen
    global start_wort
    global wortliste
    global passende_woerter
    if iterationen == 0 and len(nt_var.get()) == 0 and len(r1_var.get()) == 0 and len(r2_var.get()) == 0 \
        and len(r3_var.get()) == 0  and len(r4_var.get()) == 0  and len(r5_var.get()) == 0 \
        and len(f1_var.get()) == 0 and len(f2_var.get()) == 0 \
        and len(f3_var.get()) == 0  and len(f4_var.get()) == 0  and len(f5_var.get()) == 0:
        vorschlaege_var.set(start_wort)
    else:
        passende_woerter = filtern(wortliste)
        vorschlaege_var.set(passende_woerter)
    iterationen += 1
    iterationen_var.set('Suchvorgänge: ' + str(iterationen))

def update_gefunden(*args):
    gefunden_var.set('Gefunden: ' + str(len(passende_woerter)))

def remove_all_traces():
    r1_var.trace_remove("write", r1_var.trace_id)
    r2_var.trace_remove("write", r2_var.trace_id)
    r3_var.trace_remove("write", r3_var.trace_id)
    r4_var.trace_remove("write", r4_var.trace_id)
    r5_var.trace_remove("write", r5_var.trace_id)
    f1_var.trace_remove("write", f1_var.trace_id)
    f2_var.trace_remove("write", f2_var.trace_id)
    f3_var.trace_remove("write", f3_var.trace_id)
    f4_var.trace_remove("write", f4_var.trace_id)
    f5_var.trace_remove("write", f5_var.trace_id)
    nt_var.trace_remove("write", nt_var.trace_id)

def add_all_traces():
    r1_var.trace_id = r1_var.trace_add("write", suchen)
    r2_var.trace_id = r2_var.trace_add("write", suchen)
    r3_var.trace_id = r3_var.trace_add("write", suchen)
    r4_var.trace_id = r4_var.trace_add("write", suchen)
    r5_var.trace_id = r5_var.trace_add("write", suchen)
    f1_var.trace_id = f1_var.trace_add("write", suchen)
    f2_var.trace_id = f2_var.trace_add("write", suchen)
    f3_var.trace_id = f3_var.trace_add("write", suchen)
    f4_var.trace_id = f4_var.trace_add("write", suchen)
    f5_var.trace_id = f5_var.trace_add("write", suchen)
    nt_var.trace_id = nt_var.trace_add("write", suchen)

def reset_form():
    global iterationen
    iterationen = 0
    remove_all_traces()
    r1_var.set('')
    r2_var.set('')
    r3_var.set('')
    r4_var.set('')
    r5_var.set('')
    f1_var.set('')
    f2_var.set('')
    f3_var.set('')
    f4_var.set('')
    f5_var.set('')
    nt_var.set('')
    iterationen_var.set('Suchvorgänge: ' + str(iterationen))
    passende_woerter = [start_wort]
    vorschlaege_var.set(passende_woerter)
    gefunden_var.set('Gefunden: ' + str(len(passende_woerter)))
    add_all_traces()

erneut_btt = ttk.Button(mainframe, text="Erneut", command=reset_form)
erneut_btt.grid(column=1, row=7, sticky=E)

add_all_traces()
vorschlaege_var.trace_id = vorschlaege_var.trace_add("write", update_gefunden)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
for child in rf_frame.winfo_children(): 
    child.grid_configure(padx=1,pady=5)

root.bind("<Return>", suchen)

load_file()

root.mainloop()