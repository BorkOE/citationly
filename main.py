'''Interface for adding academic citations to dabase'''

import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database schema
Base = declarative_base()

class Citation(Base):
    __tablename__ = "citations"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    page_numbers = Column(String)
    authors = Column(String)
    book_title = Column(String)
    year = Column(String)       # should be Integer?
    key1 = Column(String)
    key2 = Column(String)
    course = Column(String)
    extra1 = Column(String)
    extra2 = Column(String)


# Create the database engine and session
engine = create_engine("sqlite:///citations.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


root = tk.Tk()
root.title("Academic Citation Helper")

# Create labels and input boxes for text to be cited, page numbers, authors, and book title
text_label = tk.Label(root, text="Text to be cited:")
text_label.grid(row=0, column=0, padx=5, pady=5)
text_box = tk.Entry(root)
text_box.grid(row=0, column=1, padx=5, pady=5)

page_label = tk.Label(root, text="Page numbers:")
page_label.grid(row=1, column=0, padx=5, pady=5)
page_box = tk.Entry(root)
page_box.grid(row=1, column=1, padx=5, pady=5)

author_label = tk.Label(root, text="Author(s):")
author_label.grid(row=2, column=0, padx=5, pady=5)
author_box = tk.Entry(root)
author_box.grid(row=2, column=1, padx=5, pady=5)

book_label = tk.Label(root, text="Book title:")
book_label.grid(row=3, column=0, padx=5, pady=5)
book_box = tk.Entry(root)
book_box.grid(row=3, column=1, padx=5, pady=5)

key1_label = tk.Label(root, text="Keyword 1:")
key1_label.grid(row=4, column=0, padx=5, pady=5)
key1_box = tk.Entry(root)
key1_box.grid(row=4, column=1, padx=5, pady=5)

key2_label = tk.Label(root, text="Keyword 2:")
key2_label.grid(row=5, column=0, padx=5, pady=5)
key2_box = tk.Entry(root)
key2_box.grid(row=5, column=1, padx=5, pady=5)

def clean_string(cit_string):
    string_out = (str(cit_string)
                  .replace('\t', ' ')
                  .replace('\n', '')
                  )
    return string_out
    
def submit_citation():
    # Create a new citation object and add it to the database
    text = clean_string(text_box.get())
    if not text:
        return
    
    citation = Citation(
        text=text,
        page_numbers=page_box.get(),
        authors=author_box.get(),
        book_title=book_box.get(),
        key1=key1_box.get(),
        key2=key2_box.get(),
    )
    session.add(citation)
    session.commit()
    # Clear the input boxes
    text_box.delete(0, tk.END)
    page_box.delete(0, tk.END)
    # author_box.delete(0, tk.END)      # Leave as they prob. will be used next again
    # book_box.delete(0, tk.END)
    key1_box.delete(0, tk.END)
    key2_box.delete(0, tk.END)

    populate_author_listbox()           # Updates if we just submitted a new author

def insert_text(box, text):
    box.delete(0, tk.END)
    box.insert(0, text)

def insert_text_from_listbox(box, listbox):
    '''Puts selected text from a listbox in a textbox'''
    
    if not listbox.curselection():
        return
    text = listbox.get(listbox.curselection())
    insert_text(box, text)
    
    if box == author_box:               # Trigger update populate_book_listbox
        populate_book_listbox(author=text)

def populate_author_listbox():
    '''Finds authors already in database and fills listbox'''
    author_listbox.delete(0, tk.END)
    citations = session.query(Citation).all()
    authors = sorted(list(set(citation.authors for citation in citations)))
    
    for author in authors:
        author_listbox.insert(tk.END, author)

def populate_book_listbox(author=None):
    '''Finds books by selected authors already in database and fills listbox'''
    book_listbox.delete(0, tk.END)
    citations = session.query(Citation).all()
    if author:
        # Filter books by author
        books = (session
                 .query(Citation.book_title)
                 .filter(Citation.authors == author)
                 .distinct()
                 .all()
                 )
        books = [b[0] for b in books]
    else:
        books = sorted(list(set(citation.book_title for citation in citations)))

    for book in books:
        book_listbox.insert(tk.END, book)
    
    if author:
        insert_text(book_box, books[0])

# Create a button to submit the citation information
submit_button = tk.Button(root, text="Submit", command=submit_citation)
submit_button.grid(row=6, column=1, padx=5, pady=5)

author_listbox = tk.Listbox(root, width=15, height=5)
author_listbox.grid(row=2, column=2)
book_listbox = tk.Listbox(root, width=15, height=5)
book_listbox.grid(row=3, column=2)

populate_author_listbox()
populate_book_listbox()


# User input logic
author_listbox.bind("<<ListboxSelect>>", lambda x: insert_text_from_listbox(author_box, author_listbox))
book_listbox.bind("<<ListboxSelect>>", lambda x: insert_text_from_listbox(book_box, book_listbox))
root.bind('<Return>', lambda x: submit_citation())


# TODO: 
'''
Gör combobox för keywords. Plockar alla keywords i databasen
Lägg till year och låt den fungera likadant med boxarna, (liten listbox dock)
Datestamp automatiskt, sjukt smidigt för att filtrera sen
'''

root.mainloop()

