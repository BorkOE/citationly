import tkinter as tk
import requests
from re import findall

# TODO
'''
Ändra från json till bibtex
'''

ignore = {'urls', 'VtiD'}
data = {}
data_choosen = {}
entry_width = 80

def fix_symbols(s):
    s_fixed = (s
               .replace(r'{\AA}', 'Å')
               .replace(r'{\aa}', 'å')
               .replace(r'{\"A}', 'Ä')
               .replace(r'{\"a}', 'ä')
               .replace(r'{\"O}', 'Ö')
               .replace(r'{\"o}', 'ö')
               .replace(r'{\O}', 'Ø')
               .replace(r'{\o}', 'ø')
               .replace(r'{\&}', '&')
               )
    return s_fixed

def on_item_select(event):
    '''Gets data on listbox selection and calls display_data'''
    global selected_data
    a_lb, p_lb = find_selected_listbox()
    idx = a_lb.curselection()     # Obs, om vi är i select_box
    if idx == ():       # Deselect listbox
        return
    selected_item = a_lb.get(idx)
    selected_data = (data | data_choosen)[selected_item]
    if a_lb == listbox:
        data_choosen.update({selected_item: selected_data})
    display_data(selected_data)

def on_export():
    selected_items = [listbox.get(idx) for idx in listbox.curselection()]
    export_to_biblatex()

def on_search():
    search_query = search_entry.get()
    if not search_query:
        return
    search_results = search_data(search_query)
    update_listbox(search_results)

def display_data(selected_data):
    '''Clears previous data and insert new'''
    data_frame.delete(1.0, tk.END)
    data_frame.insert(tk.END, f"{fix_symbols(selected_data)}")

def export_to_biblatex():
    bib_data = '\n\n'.join([(data | data_choosen)[k] for k in selected_listbox.get(0, tk.END)])
    with open("output.bib", 'w') as bib_file:
        bib_file.write(bib_data)

def parse_data(in_data):
    out_data = {}
    split_me = in_data.replace('\n\n\n', '\n')
    for entry in split_me.split('\n@'):
        if not entry:
            continue
        entry_fix = fix_symbols(entry)
        title = findall(r'title={([^}]+)}', entry_fix)[0]
        if title in out_data:
            title += '_dup'
        out_data.update({fix_symbols(title): '@'+entry})


    return out_data

def search_data(query):
    '''Search libris and parse result, updates data'''
    global data
    # url = f'http://libris.kb.se/xsearch?query={query}&format=json&n=50'
    url = f'http://libris.kb.se/xsearch?query={query}&format=bibtex&n=50'
    response = requests.get(url)
    # json_data = response.json()
    data = parse_data(response.text)
    return data

def update_listbox(items):
    # Clear previous items
    listbox.delete(0, tk.END)

    # Add new items to the listbox
    for item in items:
        listbox.insert(tk.END, item)

def find_selected_listbox():
    '''returns active lb, passive lb'''
    idx = listbox.curselection()
    if idx != ():
        return listbox, selected_listbox
    return selected_listbox, listbox

def move_selected_item():
    a_lb, p_lb = find_selected_listbox()
    a_idx = a_lb.curselection()                 # Active index
    selected_item = a_lb.get(a_idx)             
    selected_data = data[selected_item]
    p_lb.insert(tk.END, selected_item)
    a_lb.delete(a_idx, a_idx)
    display_data(selected_data)

# Create the main tkinter window
window = tk.Tk()
window.title("BibLaTeX Exporter")

# Create the search box and search button
search_entry = tk.Entry(window, width=entry_width)
search_entry.pack()
search_entry.bind("<Return>", lambda event: on_search())

search_button = tk.Button(window, text="Search", command=on_search)
search_button.pack()

# Create the listbox
listbox = tk.Listbox(window, width=entry_width)
listbox.pack()

# Populate the listbox with titles
update_listbox(data.keys())

# Bind the item select event to the listbox
listbox.bind("<<ListboxSelect>>", on_item_select)
listbox.bind("<Return>", lambda event: move_selected_item())

# Create the button to move selected item
move_button = tk.Button(window, text="Move", command=move_selected_item)
move_button.pack()

# Create the data display frame
data_frame = tk.Text(window, height=14, width=80, state=tk.NORMAL)
data_frame.pack()

# Create the export button
export_button = tk.Button(window, text="Export to BibLaTeX", command=on_export)
export_button.pack()

# Create the selected items listbox
selected_listbox = tk.Listbox(window, width=entry_width)
selected_listbox.pack()
selected_listbox.bind("<<ListboxSelect>>", on_item_select)
selected_listbox.bind("<Return>", lambda event: move_selected_item())

# Start the tkinter event loop
window.mainloop()
