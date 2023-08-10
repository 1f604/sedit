Table of contents:

- [sedit - automatically encrypting text editor](#sedit---automatically-encrypting-text-editor)
- [Dependencies](#dependencies)
- [How to use](#how-to-use)
  - [Create a new file](#create-a-new-file)
  - [Open an existing file](#open-an-existing-file)
- [Installation on Unixy systems](#installation-on-unixy-systems)
- [Notes](#notes)
  - [Relationship to Dropass](#relationship-to-dropass)
  - [Code organization](#code-organization)
- [Keyboard shortcuts:](#keyboard-shortcuts)

# sedit - automatically encrypting text editor

With this program, you can:

1. Create a new sedit-encrypted file.
2. Open an existing sedit-encrypted file, modify it, and save it.

Note: For general file encryption use cases (where you would have previously used `gpg`), it is now recommended that you use [age](https://github.com/FiloSottile/age). 

# Dependencies

1. python 3+
2. pynacl 1.3.0 (you can install this with pip using `pip3 install pynacl`)
3. tkinter (you may have to install this. On fedora you can use `sudo dnf install python3-tkinter`)

# How to use

There are 2 utilities provided: `screate.py` and `sopen.py`. These are used for creating and opening files respectively. In particular, `screate.py` simply creates a file. You need to then run `sopen.py` to open the file. 

This text editor assumes that you use UTF-8 encoding. 

## Create a new file

```bash
$ python3 screate.py filename
```

This creates a new file named `filename` in the current directory (where `screate.py` is located). 

If the file was successfully created, a message will be printed. You can then run:

```
$ python3 sopen.py filename
``` 

to open the file. 

## Open an existing file

```bash
$ python sopen.py filename.salsa20
```

If the file exists then this will open it. Otherwise it will fail with an error. 

# Installation on Unixy systems

The scripts can be used as-is out of the box, but for convenience you can add some scripts to your `/usr/local/bin` directory (Linux/OSX only) so that you don't have to type the full path of the script every time. 

Save this to a file called `screate` in your `/usr/local/bin` directory:

```
#!/bin/bash
python3 /path/to/screate.py "$@" # make sure to change this path to where you're storing sedit
```

Save this to a file called `sedit` in your `/usr/local/bin` directory:

```
#!/bin/bash
python3 /path/to/sopen.py "$@"  # make sure to change this path to where you're storing sedit
```

Then run `sudo chmod +x /usr/local/bin/screate /usr/local/bin/sedit`. Now you can use the commands `screate` and `sedit` anywhere. 

This means you can simply type `sedit filename` and it will just work, regardless of your current working directory. 

# Notes

## Relationship to Dropass

This program is based on and supercedes [Dropass](https://github.com/1f604/dropass). The code has been changed and the workflow has been simplified to make it more user-friendly. Search functionality has been added. 

Some minor "quality of life" improvements have been made: Mac users can now use the Cmd key instead of Ctrl, and an annoying bug has been fixed where clicking past half of the whitespace at the end of a line would set the cursor to the start of the next line. 

## Code organization

I know it's not great, I'm still working on it. I wrote dropass 2 years ago and I haven't touched it until now. When I looked at it again, the most annoying thing that jumped out at me was that I couldn't easily tell which variables were global and which weren't, which is what has led to the current class-based design, with all the state encapsulated within the class. It's quite likely that I will revisit this code again some years later and "refactor" it once again. 

# Keyboard shortcuts:

- Ctrl-s to save file (file will be automatically encrypted with your master password when saved - plaintext will be deleted - gone -  once you close the editor). Cool thing to notice is that every time you save, a new IV will be randomly generated so the ciphertext will be completely different to before (even if the plaintext is exactly the same)! Pretty cool imo. 
- Ctrl-w to close editor 
- Ctrl-a to select all
- Ctrl-l to select current line 
- Ctrl-f to enter search mode and search text
- Esc to exit search mode

Substitute Ctrl for Cmd if you're using a Mac keyboard. 

Please report any bugs you find in Issues (ideally with steps to reproduce, and expected behavior). I check my emails every day and I am the active maintainer for this project.
