Вот код с реализованной подсветкой синтаксиса для языков Python и C++:

#-- coding: windows-1251 --
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.font import Font, families
import subprocess
from tkinter.ttk import Combobox, Notebook
import sys
from PIL import Image, ImageTk
import os
import tempfile
import codecs
import threading
from tkinter import ttk
from tkinter import Tk
from tkinter import StringVar
from tkinter import TclError
import os.path
import shlex
import platform
import keyword
import re

file_path = ""

def toggle_theme():
    if editor.cget('background') == 'white':
        editor.config(background='black', foreground='white', insertbackground='white')
        code_output.config(background='black', foreground='white', insertbackground='white')
    else:
        editor.config(background='white', foreground='black', insertbackground='black')
        code_output.config(background='white', foreground='black', insertbackground='black')

def change_font(event):
    selected_font = font_var.get()
    font_tuple = (selected_font, 12)
    editor.config(font=font_tuple)
    code_output.config(font=font_tuple)
    
def change_text_color():
    color = askcolor()[1]
    if color:
        editor.config(fg=color)
        
def change_language(language):
    if language == "English":
        file_menu.entryconfig(0, label='Open')
        file_menu.entryconfig(1, label='Save') 
        file_menu.entryconfig(2, label='Save As')
        file_menu.entryconfig(3, label='Exit')
        menu_bar.entryconfig(1, label='Toggle Theme')
        text_bar.entryconfig(0, label='Change Text Color')
        run_bar.entryconfig(0, label='Run')
        clear_bar.entryconfig(0, label='Clear Terminal')
        clear_bar.entryconfig(1, label='Clear Command Line')
        help_menu.entryconfig(0, label='Help')
        help_menu.entryconfig(1, label='About Us')
        edit_menu.entryconfig(0, label='Paste')
    else:
        file_menu.entryconfig(0, label='Открыть')
        file_menu.entryconfig(1, label='Сохранить')
        file_menu.entryconfig(2, label='Сохранить как')
        file_menu.entryconfig(3, label='Выход')
        menu_bar.entryconfig(1, label='Переключить тему')
        text_bar.entryconfig(0, label='Изменить цвет текста')
        run_bar.entryconfig(0, label='Запустить')
        clear_bar.entryconfig(0, label='Очистить терминал')
        clear_bar.entryconfig(1, label='Очистить командную строку')
        help_menu.entryconfig(0, label='Справка')
        help_menu.entryconfig(1, label='О нас')
        edit_menu.entryconfig(0, label='Вставить')
        
def display_app_version(parent_widget, version_text):
    version_label = Label(parent_widget, text=version_text, anchor='se')
    version_label.pack(side='bottom', anchor='se', padx=5, pady=5)
    
def on_language_selected(event):
    selected_language = language_combobox.get()
    print(f'Выбранный язык программирования: {selected_language}')
    highlight_syntax()
    
def get_installed_languages():
    languages = []
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        languages.append("Python")
    except FileNotFoundError:
        pass
    try:
        subprocess.run(["java", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        languages.append("Java")
    except FileNotFoundError:
        pass
    try:
        subprocess.run(["g++", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        languages.append("C++")
    except FileNotFoundError:
        pass
    return languages

def open_file():
    global file_path
    path = askopenfilename(filetypes=[('Python Files', '*.py'), ('C++ Files', '*.cpp')])
    encodings = ['utf-8', 'utf-16', 'cp1251', 'cp1252']
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as file:
                code = file.read()
                editor.delete('1.0', END)
                editor.insert(INSERT, code)
                file_path = path
                highlight_syntax()
                break
        except UnicodeDecodeError:
            pass
            
def save_as():
    global file_path
    path = file_path if file_path != '' else asksaveasfilename(filetypes=[('Python Files', '*.py'), ('C++ Files', '*.cpp')])
    if path:
        with codecs.open(path, 'w', encoding='utf-8') as file:
            code = editor.get('1.0', END)
            file.write(code)
            file_path = path
            
def run():
    global file_path
    if not file_path:
        if file_path == '':
            save_as()
        if file_path:
            # Create a temporary file and write the content to it
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
                code = editor.get("1.0", END)
                temp.write(code)
            # Run the temporary file to get the result
            process = subprocess.Popen(["python", temp.name], text=True, stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
            output, error = process.communicate()
            # Output the result to the terminal
            code_output.config(state=NORMAL)
            code_output.insert(END, "\n" + output)  
            if error:
                code_output.insert(END, "\n" + error, "error")
                code_output.tag_configure("error", foreground="red")
            code_output.config(state=DISABLED)
            # Delete the temporary file
            os.remove(temp.name)
        save_as()
    
    if file_path:
        process = subprocess.Popen(["python", file_path], text=True,\
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        code_output.config(state=NORMAL)
        code_output.insert(END, "\n" + output)
        if error:
            code_output.insert(END, "\n" + error, "error")
            code_output.tag_configure("error", foreground="red")
        code_output.config(state=DISABLED)
        
def clear_terminal():
    code_output.config(state=NORMAL)
    code_output.delete('1.0', END)
    code_output.config(state=DISABLED)
    
def clear_command_line():
    editor.delete('1.0', END)
    
def highlight_syntax():
    code = editor.get("1.0", "end")
    languages = ["python", "cpp"]
    selected_language = language_combobox.get().lower()
    
    if selected_language in languages:
        highlighted_code = highlight(code, selected_language)
        editor.delete("1.0", END)
        editor.insert("1.0", highlighted_code)
        
def highlight(code, language):
    if language == "python":
        keywords = keyword.kwlist
        keyword_pattern = r'\b(' + r'|'.join(keywords) + r')\b'
        keyword_re = re.compile(keyword_pattern)
        
        strings_re = re.compile(r'(".*?")|(\'.*?\')')
        comments_re = re.compile(r'#.*$')
        
        highlighted_code = ""
        for line in code.split("\n"):
            line = comments_re.sub(r'\1', line)
            line = strings_re.sub(r'\2', line)
            line = keyword_re.sub(r'\1', line)
            
            highlighted_code += line + "\n"
            
        return highlighted_code
    
    elif language == "cpp":
        keywords = [
            "auto", "break", "case", "char", "const", 
            "continue", "default", "do", "double", "else", 
            "enum", "extern", "float", "for", "goto", 
            "if", "int", "long", "register", "return", 
            "short", "signed", "sizeof", "static", "struct", 
            "switch", "typedef", "union", "unsigned", "void", 
            "volatile", "while"
        ]
        
        keyword_pattern = r'\b(' + r'|'.join(keywords) + r')\b'
        keyword_re = re.compile(keyword_pattern)
        
        strings_re = re.compile(r'(".*?")|(\'.*?\')')
        comments_re = re.compile(r'//.*$')
        
        highlighted_code = ""
        for line in code.split("\n"):
            line = comments_re.sub(r'\1', line)
            line = strings_re.sub(r'\2', line)
            line = keyword_re.sub(r'\1', line)
            
            highlighted_code += line + "\n"
            
        return highlighted_code
        
def run():
    global file_path
    if file_path == '':
        save_as()
    if file_path:
        # Create a temporary file and write the content to it
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
            code = editor.get("1.0", END)
            temp.write(code)
        # Run the temporary file to get the result
        process = subprocess.Popen(["python", temp.name], text=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, error = process.communicate()
        # Output the result to the terminal
        code_output.config(state=NORMAL)
        code_output.insert(END, "\n" + output)
        if error:
            code_output.insert(END, "\n" + error, "error")
            code_output.tag_configure("error", foreground="red")
        code_output.config(state=DISABLED)
        # Delete the temporary file
        os.remove(temp.name)
        
compiler = Tk()
compiler.wm_title("LifeBoost")
# Разрешить или запретить изменение размера окна
compiler.resizable(False, False) 

iconpath = "icon.ico"
compiler.iconbitmap(iconpath)

def set_file_path(path):
    global file_path
    file_path = path
    
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=compiler.quit)

menu_bar.add_command(label='Toggle Theme', command=toggle_theme)
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Paste', command=paste_text)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

compiler.config(menu=menu_bar)

text_bar = Menu(menu_bar, tearoff=0)
text_bar.add_command(label='Change Text Color', command=change_text_color)
menu_bar.add_cascade(label='Text', menu=text_bar)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

clear_bar = Menu(menu_bar, tearoff=0)
clear_bar.add_command(label='Clear Terminal', command=clear_terminal)
clear_bar.add_command(label='Clear Command Line', command=clear_command_line)
menu_bar.add_cascade(label='Clear', menu=clear_bar)

language_menu = Menu(menu_bar, tearoff=0)
language_menu.add_command(label='English', command=lambda: change_language('English'))
language_menu.add_command(label='Русский', command=lambda: change_language('Russian'))
menu_bar.add_cascade(label='Language', menu=language_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label='Help', command=open_help_window)
help_menu.add_command(label='About Us', command=open_about_window)
menu_bar.add_cascade(label='Help', menu=help_menu)

compiler.config(menu=menu_bar)

language_choices = get_installed_languages()
language_combobox = Combobox(compiler, values=language_choices, state='readonly')
language_combobox.current(0)
language_combobox.bind('<<ComboboxSelected>>', on_language_selected)
language_combobox.pack(side='bottom', anchor='sw', padx=5, pady=5)

editor = Text()
editor.pack()

def switch_tab(event):
    selected_tab = notebook.index(notebook.select())
    if selected_tab == 0:
        terminal_label.config(text="Terminal")
    elif selected_tab == 1:
        terminal_label.config(text="Local")
        
def execute_command(event):
    selected_tab = notebook.index(notebook.select())
    if selected_tab == 0: # Terminal
        run() # Вызываем функцию run() при активации вкладки Terminal
    else:
        command = local_terminal.get("end-1c linestart", "end-1c")
        local_terminal.insert(END, "\n")
        def run_command():
            try:
                if sys.platform == "win32":
                    shell = True
                    text = True
                else:
                    shell = False
                    text = False
                # Разбиваем командную строку на аргументы с помощью shlex.split
                command_args = shlex.split(command)
                process = subprocess.Popen(
                    command_args,
                    cwd=os.path.dirname(file_path) if file_path else None,
                    shell=shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=text,
                )
                output, error = process.communicate()
                insert_protected_text(local_terminal, output)
                if error:
                    insert_protected_text(local_terminal, "Error: " + error, "error", foreground="red")
            except Exception as e:
                insert_protected_text(local_terminal, "Error: Возникла ошибка: {}\n".format(str(e)), "error", foreground="red")
        threading.Thread(target=run_command).start()
        local_terminal.mark_set("protect_mark", local_terminal.index("end-1c linestart"))
        
def insert_protected_text(widget, txt, tag=None, **kw):
    if tag is not None:
        widget.insert(END, txt, tag)
        widget.tag_configure(tag, kw)
    else:
        widget.insert(END, txt)
    widget.mark_set("protect_mark", local_terminal.index("end-1c linestart"))
        
def backspace(event):
    if local_terminal.compare("insert-1c", "<=", "protect_mark"):
        return "break"
        
def delete(event):
    if local_terminal.compare("insert", "<=", "protect_mark"):
        return "break"

notebook = ttk.Notebook(compiler)

code_output = Text(height=10)
local_terminal = Text(height=10)

notebook.add(code_output, text='Terminal')
notebook.add(local_terminal, text='Local')

notebook.bind('<<NotebookTabChanged>>', switch_tab)
notebook.pack()

insert_protected_text(local_terminal, 'Windows PowerShell\n\n(C) Корпорация Fixfrom (Fixfrom Corporation). Все права защищены.\n________________________________________________________________________________\n\n')
local_terminal.mark_set("protect_mark", local_terminal.index("end-1c linestart"))
local_terminal.bind("<Return>", execute_command)  
local_terminal.bind("<BackSpace>", backspace)
local_terminal.bind("<Delete>", delete)

terminal_label = Label(code_output, text="Terminal", bg="white", anchor='nw')
terminal_label.place(x=589, y=0)
code_output.configure(state=DISABLED)

def auto_complete_brackets(event):
    if event.char == '(':
        editor.insert(INSERT, ')')
        editor.mark_set(INSERT, editor.index(INSERT + '-1c'))
    elif event.char == '[':
        editor.insert(INSERT, ']')
        editor.mark_set(INSERT, editor.index(INSERT + '-1c'))
    elif event.char
