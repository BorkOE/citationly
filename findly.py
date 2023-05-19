import tkinter as tk
import requests

# TODO
'''
Ha en till datavariabel, dict, som sparar de tillagda titlarna. Så vi kan söka vidare och forfarande ha kvar 
On export, gå igenom id i vald data och hämta bibtex
'''

ignore = {'urls', 'VtiD'}
data = {}
data_choosen = {}
entry_width = 80

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
    export_to_biblatex(selected_items)

def on_search():
    search_query = search_entry.get()
    if not search_query:
        return
    search_results = search_data(search_query)
    update_listbox(search_results)

def display_data(selected_data):
    # Clear previous data
    # data_frame['state'] = tk.NORMAL
    data_frame.delete(1.0, tk.END)

    # Display selected data in the data_frame
    for key, value in selected_data.items():
        data_frame.insert(tk.END, f"{key}: {value}\n")

def export_to_biblatex(selected_items):
    pass
    # Generate the BibLaTeX file
    # Add the selected items to the file
    # Save the file

def parse_data(json_data):
    '''turns list of dicts into one data dict'''
    parsed_data = {}
    data_list = json_data['xsearch']['list']
    for lst in data_list:
        title = lst.get('title')
        if title in parsed_data:
            lst.update({'title': f'{title}_dup'})
            title = lst.get('title')
        parsed_data.update(
            {title: {k: v for k, v in lst.items() if k not in ignore | {'title'}}})
    
    return parsed_data

def search_data(query):
    '''Search libris and parse result, updates data'''
    global data
    url = f'http://libris.kb.se/xsearch?query={query}&format=json&n=50'
    response = requests.get(url)
    json_data = response.json()
    data = parse_data(json_data)
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
