import sys
import os.path, getpass
import shutil
import filecmp
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

TEAL = '#008080'
BROWN = '#800000'
GREY = '#808080'

def goodmsg(msg):
    print(bcolors.OKGREEN + msg + bcolors.ENDC)

def badmsg(msg):
    print(bcolors.FAIL + msg + bcolors.ENDC)

def error_out(msg: str):
    badmsg("Error: " + msg)
    getpass.getpass("Press enter to exit.") # This is to capture the user's password if he enters it inadvertently.
    exit(1)

if sys.version_info[0] < 3:
    error_out("You must use Python 3")

from cryptotest import encrypt, decrypt

class WindowManager(object):
    def getSearchboxContents(self):
        return self.searchbox.get()

    def getTextboxContents(self):
        return self.text.get("1.0", "end-1c")

    def savefile(self, event=None):
        """
            When we save a file, we need to make sure it can be decrypted again.

            To this end, we first try to save it in a tmp file, once that succeeds,
            we then replace the original with the tmp file.
        """
        plaintext = self.getTextboxContents()
        self.curSavedFileContents = plaintext
        # We need to check that we can open the file again. If not, we need to re-save the file.
        # This loop exits once we've confirmed that we can decrypt the file we've just saved, or when we've tried 10 times.
        # To this end, we use a temporary file so that we don't lose the original.
        tempfilename = self.filename + ".tmp"
        success = False
        for i in range(10):
            # Since we immediately close the file, this should force a write to disk on save.
            with open(tempfilename, "wb") as f:
                f.write(encrypt(plaintext, self.password))
            # We then open the file to check if we can decrypt it.
            with open(tempfilename, "rb") as f:
                wholetext = f.read()
            try:
                if plaintext == decrypt(wholetext, self.password):
                    self.dirty = False
                    # We only change the window color after the file has been written to and closed successfully.
                    self.frame.configure(bg=TEAL)
                    goodmsg("Temp file saved successfully.")
                    success = True
                    break
            except Exception as e:
                badmsg(e)
                badmsg("Error encountered trying to decrypt/decode file, see above.")
                badmsg("This is attempt #" + str(i))
        if success:
            # successful, replace original file with tmp file.
            # we also update the backup copy, and check that they are bit-for-bit identical.
            os.remove(self.filename)
            os.rename(tempfilename, self.filename)
            goodmsg("Original successfully replaced by temp file.")
            backupfilename = self.filename+".backup"
            for _ in range(5):
                shutil.copy(self.filename, backupfilename)
                if not filecmp.cmp(self.filename, backupfilename):
                    badmsg("ERROR: backup file is not identical to original.")
                else:
                    goodmsg("Backup file successfully saved and checked.")
                    break
            else:
                badmsg("Warning: File was not backed up.")
        else:
            # failed, delete temporary file.
            os.remove(tempfilename)
            badmsg("ERROR: FILE NOT SAVED.")

    def checkUnsavedChanges(self, event=None):
        # check if saving
        # if not:
        if self.dirty:
            if messagebox.askyesno("Exit", "THERE ARE UNSAVED CHANGES! Do you want to quit the application?"):
                if messagebox.askokcancel("Exit", "THERE ARE UNSAVED CHANGES!! ARE YOU SURE you want to quit the application?"):
                    win = tk.Toplevel()
                    win.title('warning')
                    message = "This will delete stuff"
                    tk.Label(win, text=message).pack()
                    buttons = [
                        tk.Button(win, text='No!', command=win.destroy),
                        tk.Button(win, text='Delete', command=self.root.destroy),
                        tk.Button(win, text='Noo!', command=win.destroy),
                        tk.Button(win, text='Don\'t delete!!', command=win.destroy)
                    ]
                    random.shuffle(buttons)
                    for button in buttons:
                        button.pack()
        else:
            self.root.destroy()

    def ismodified(self, event):
        plaintext = self.getTextboxContents()
        if plaintext != self.curSavedFileContents:
            self.frame.configure(bg=BROWN)
            self.dirty = True
        else:
            self.frame.configure(bg=TEAL)
            self.dirty = False
        self.text.edit_modified(0)  # IMPORTANT - or <<Modified>> will not be called later.

    def on_focus_out(self, event):
        if event.widget == self.root:
            self.frame.configure(bg=GREY)

    def on_focus_in(self, event):
        if event.widget == self.root:
            if self.dirty:
                self.frame.configure(bg=BROWN)
            else:
                self.frame.configure(bg=TEAL)

    def focus_search(self, event):
        self.searchbox.focus()
        self.select_all_searchbox(event)

    def clear_highlights(self, event):
        self.in_search = False
        self.srch_idx = '1.0'
        self.text.tag_remove('found', '1.0', tk.END)
        self.text.tag_remove('found_cur', '1.0', tk.END)
        self.msglabel['text'] = ''

    def search_highlight(self, s):
        """
            Given a search string s, highlight all occurrances of it in the text.
        """
        self.text.tag_remove('found', '1.0', tk.END)
        if s:
            idx = '1.0'
            while 1:
                idx = self.text.search(s, idx, nocase=1, stopindex=tk.END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(s))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config('found', background='magenta') #firefox search highlight colors
            self.text.tag_raise("sel") # allow highlighted text to be seen over search highlights

    def find_next(self, needle):
        self.text.tag_remove('found_cur', '1.0', tk.END)
        idx = self.text.search(needle, self.srch_idx, nocase=1, stopindex=tk.END)
        if not idx:
            self.srch_idx = '1.0'
            self.msglabel['text'] = 'No more search results.'
            return
        self.msglabel['text'] = ''
        lastidx = '%s+%dc' % (idx, len(needle))
        self.srch_idx = lastidx
        self.text.tag_add('found_cur', idx, lastidx)
        self.text.tag_config('found_cur', foreground='red', background='green') #firefox search highlight colors
        self.text.tag_raise("sel") # allow highlighted text to be seen over search highlights
        self.text.see(idx) # scroll the textbox to where the found text is.

    def text_search(self, event):
        needle = self.getSearchboxContents()
        if not self.in_search:
            self.in_search = True
            self.search_highlight(needle)
        self.find_next(needle)

    # This is to move the cursor to the end of the line when you click on some empty space at the end of the line.
    # Default behavior is really annoying as it moves the cursor to the beginning of the next line if you click past half of the whitespace.
    def on_text_click(self, event):
        line = event.x
        column = event.y
        index = self.text.index("@%d,%d" % (event.x, event.y))
        self.text.mark_set("insert", index)

    # Select all the text in textbox
    def select_all(self, event):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        return 'break'

    # Select all the text in searchbox
    def select_all_searchbox(self, event):
        self.searchbox.select_range(0, tk.END)
        return 'break'

    # Select current line in textbox
    def select_line(self, event):
        tk.current_line = self.text.index(tk.INSERT)
        self.text.tag_add(tk.SEL, "insert linestart", "insert lineend+1c")
        return 'break'
        #after(interval, self._highlight_current_line)

    def __init__(self, root, filename, contents, password):
        # initialize "global" variables
        # These variables refer to the elements inside the UI
        # For example, self.text refers to the main text box, self.searchbox refers to the search box, and so on.
        self.root = root
        self.filename = filename
        self.curSavedFileContents = contents
        self.password = password
        self.dirty = False
        self.frame = tk.Frame(root, bg=TEAL)
        self.text = tkst.ScrolledText(
            master=self.frame,
            wrap='word',  # wrap text at full words only
            width=80,      # characters
            height=30,      # text lines
            bg='beige',        # background color of edit area
            undo=True
        )
        self.searchframe = tk.Frame(root)
        self.searchlabel = tk.Label(self.searchframe, text='Search text:')
        self.searchbox = tk.Entry(self.searchframe)
        saveframe = tk.Frame(root)
        self.msglabel = tk.Label(saveframe, text='')

        # initialize text editor window UI
        self.root.wm_title("sedit")
        self.frame.pack(fill='both', expand='yes')
        self.text.bind('<<Modified>>', self.ismodified)
        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)
        self.searchlabel.pack(side=tk.LEFT)
        self.searchbox.pack(side=tk.LEFT, expand=True, fill='both')
        self.msglabel.pack(side=tk.LEFT)
        self.searchframe.pack(fill=tk.X)
        button = tk.Button(saveframe, text="Save", command=self.savefile, padx=8, pady=8)
        button.pack(side=tk.RIGHT)
        saveframe.pack(fill=tk.X)
        # the padx/pady space will form a frame
        self.text.pack(fill='both', expand=True, padx=8, pady=8)
        self.text.insert('insert', contents)
        self.frame.configure(bg=TEAL)
        # On Mac, Command binds to the cmd key. On Windows it binds to the ctrl key.
        self.root.bind_all("<Command-w>", self.checkUnsavedChanges)
        self.root.bind_all("<Command-s>", self.savefile)
        self.text.bind("<Command-a>", self.select_all)
        self.text.bind("<Command-l>", self.select_line)
        self.in_search = False
        self.srch_idx = '1.0'
        self.text.bind("<Command-f>", self.focus_search)
        self.searchbox.bind("<Return>", self.text_search)
        self.root.bind("<Escape>", self.clear_highlights)
        self.searchbox.bind("<Command-a>", self.select_all_searchbox)
        self.root.bind("<Button-1>", self.on_text_click)
        self.root.protocol('WM_DELETE_WINDOW', self.checkUnsavedChanges)  # root is your root window





def openfile(filename: str, password: str):
    #1. Open file and try to decrypt it.
    with open(filename,"rb") as f:
        s = f.read()
    contents = decrypt(s,password) # An exception here is fine as we can terminate here no problems.

    #2. Main window setup
    root=tk.Tk()
    WindowManager(root, filename, contents, password)

    #3. main loop
    root.mainloop()





if __name__ == "__main__":
    if len(sys.argv) != 2:
        error_out("You must supply exactly one command line argument to open.py")

    filename = sys.argv[1]
    filename = os.path.abspath(filename) # just for insurance.

    # Check if file exists
    if not os.path.isfile(filename):
        error_out("File not found.")

    goodmsg("sedit: Found file "+filename+".")

    password = getpass.getpass("Enter the password to decrypt the file: ")

    # All these GUI imports take a while, so we only do it after the user enters the right password.
    # This is to allow the user to enter the password immediately after starting this program.
    import tkinter as tk
    from tkinter import messagebox
    import tkinter.scrolledtext as tkst

    openfile(filename, password)
