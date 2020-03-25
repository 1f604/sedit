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
  - [If you must open an untrusted file, open it inside a VM](#if-you-must-open-an-untrusted-file-open-it-inside-a-vm)
  - [Choice of libraries](#choice-of-libraries)
  - [Usability](#usability)
  - [Simplicity](#simplicity)
  - [Security](#security)
  - [Availability](#availability)
- [Keyboard shortcuts:](#keyboard-shortcuts)
- [Please be aware that the undo function is somewhat buggy so don't count on being able to undo any changes you make to the file.](#please-be-aware-that-the-undo-function-is-somewhat-buggy-so-dont-count-on-being-able-to-undo-any-changes-you-make-to-the-file)

# sedit - automatically encrypting text editor

With this program, you can:

1. Create a new sedit-encrypted file.
2. Open an existing sedit-encrypted file, modify it, and save it.

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

## If you must open an untrusted file, open it inside a VM

Do not open untrusted files unless you absolutely have to. If you do have to open an untrusted file, then at least open it inside a VM. I say this because there have been well known vulnerabilities in the past, in many programs, where opening an untrusted file would get you pwned:

- CVE-2010-2547 - Use-after-free in GPG certificate parsing allows code execution.
- CVE-2014-8485 - Buffer overflow in GNU binutils file parsing potentially allows code execution.
- CVE-2019-9535 - Printing attacker controlled input to iTerm2 allows code execution. 
- CVE-2019-12735 - Modeline sandbox escape in Vim allows arbitrary execution of OS commands. 

The list goes on. It's not just complex file formats like PDFs that you have to worry about. Simply opening a file in `vim` (CVE-2019-12735), running `strings` on the file (CVE-2014-8485), or even `cat`ing the file to your terminal (CVE-2019-9535), can get you pwned. There are multiple points in this program where opening an untrusted file could get you pwned. For example, a malicious file could exploit a bug in pynacl's decryption routines, or in the Python UTF-8 decoder. If you open such a file inside a VM, the attacker would have to be packing along a VM escape in order to own you, which is much less likely, though it does happen (see list of Xen advisories). 

Note that if you have online cloud backups, then you should consider all files stored there to be permanently untrusted, because you cannot trust cloud vendors to tell you when they've been hacked. It would be trivial for a hacker or an unscrupulous employee to modify one of your files. Opening such a file with an insecure application like gpg would be risky, given gpg's track record. If you use the multi-layered encryption method in reverse, where you decrypt one layer in one VM, then you pass the result to another VM to decrypt the next layer, and so on, then your risk would be significantly reduced, as the attacker would have to pack a VM escape in addition to compromising gpg or openssl.

Note that just because you download a file from a reputable website, such as microsoft.com, doesn't necessarily mean that the file is safe. See the recent 2020 Microsoft subdomain hijackings, where any attacker could take control over a subdomain of microsoft.com, for example https://portal.ds.microsoft.com

This is why you must always verify file signatures no matter where you're downloading the file from. 

## Choice of libraries

tkinter was used because it is still the most mature, stable, and widely available python GUI library/framework as of 2020. The coding style is rather archaic, but that doesn't matter for a small project such as this one. I tried PySide2 and couldn't get it to run on my machine. 

pynacl was used because it has an easy to use, misuse-resistant API, and has been around for a while (for what it's worth, it had a security audit). It's pretty hard to mess up file encryption anyway (famous last words?). 

## Usability

"It is a profoundly erroneous truism, repeated by all copy-books and by eminent people when they are making speeches, that we should cultivate the habit of thinking of what we are doing. The precise opposite is the case. Civilization advances by extending the number of important operations which we can perform without thinking about them. Operations of thought are like cavalry charges in a battle — they are strictly limited in number, they require fresh horses, and must only be made at decisive moments." - Alfred North Whitehead

**If a program is too hard to use securely, then users will use it insecurely.** Therefore a goal in designing a tool should be to make it as easy as possible to use securely. 

Users are humans, and humans make mistakes sometimes. We should aim to reduce the security impact of these mistakes, for example downgrading a fatal mistake to a merely painful one, or ideally eliminating the possibility of making such mistakes altogether (e.g the use of memory-safe languages has eliminated the possibility of writing memory corruption bugs) - see [hierarchy of hazard controls](https://en.wikipedia.org/wiki/Hierarchy_of_hazard_controls). 

By construction, the tools I have provided do not allow you to change the password of a file once you have created it. This means **it's impossible for a user to accidentally change the password of an existing file**. I consider this to be a good thing. If they want to change the password, then they have to create a new file with the new password and copy over the contents from the old file, then delete the old file. In future I may add a script to make it possible to change the password. 

If you want a secure way to generate a secure password, I suggest using my [xkcd password generator](https://github.com/1f604/xkcdpwd). Of course, you must use a different password for everything, so you need to store your passwords somewhere - which is the original use case for this program. 

## Simplicity

It is vitally important for a program to be easily auditable. Keeping it as simple and modular as possible helps achieve this goal. Unneeded functionality should be removed so that they don't present unnecessary attack surface in addition to adding unnecessary complexity. 

This is one of the primary motivations for choosing Python: to keep the number of lines of code to a minimum, as well as to make the program as easy to read and understand as possible. Unfortunately this increases the number of entities that you need to trust (now you have to trust Python developers, tkinter developers, pynacl developers, etc.), which is a bad thing. In any case, you should be running this program inside an isolated VM with no network access, so the fact that this is written in Python rather than C should not make a significant difference to security. 

## Security

Information security usually refers to confidentiality and integrity. Availability is generally regarded as a reliability problem. 

Ordinary people: "I don't care whether it's secure or not, as long as it works."  
Security people: "I don't care whether it works or not, as long as it's secure."  

You have to make the call - do you prefer your data to be lost, or leaked? Which would be more damaging to you? This has implications for what technologies and strategies you should choose. Not all data needs the same level of security. 

There are 2 main threats to information security for most people:

1. Hacking (e.g ransomware, credential stealers, and RATs). Encryption won't protect you against this. 
2. Physical theft and cloud storage leaks. Encryption will protect you against those. 

If someone physically steals your computer, or your hard drives, encryption will ensure that he cannot read your files. Likewise if your cloud backup gets leaked, encryption will ensure that your files cannot be read by anyone without the password. There are also lots of programs that scan all the files on your computer and upload them to some remote server somewhere - Windows, Chrome, and all antiviruses do this. If you are concerned about your data getting sent to unaccountable entities, then encrypting your files will protect against this threat. Note however that these "nosy" programs could also look through other processes' memory (e.g. via `ptrace` or `ReadProcessMemory`), and encryption will not protect against that. I mean, on most mainstream operating systems, any program can read the contents of your clipboard at any time! It's really impossible to have any privacy when your OS is not designed for that. 

However, if you get hacked by opening some email attachment, or visiting a website, or downloading some backdoored software either manually or via automatic update (ASUS Live Update Utility, Gentoo, Linux Mint, Wechat, Didi, Railway 12306, China Unicom Mobile Office, Audacity, Classic Shell, CCleaner, Transmission, Handbrake, rsync, ProFTPD, etc.), then encryption is useless against it. If someone has owned up your computer, he can install a RAT, keylogger, ransomware, and whatever else he wants, and literally see everything that you're doing. As an application developer, there's nothing I can do to protect you against that. Do not be under the illusion that you can just install some application to protect yourself against this type of threat. **Antivirus software is absurdly dangerous.** Never install them. Because they scan (read: parse and run) every file on your computer, they have a huge, unsecurable attack surface (see: https://bugs.chromium.org/p/project-zero/issues/detail?id=1252&desc=5 Emphasis: "**Any filesystem activity, including receiving an email or browsing the web is enough to trigger this vulnerability.**"). Did you know that Avast antivirus included an unsandboxed Javascript interpreter that ran with system privileges? Not to mention they're also completely useless, as it's trivial for a malware author to keep modifying his creation until the likes of VirusTotal says that it's clean. You cannot deal with these kinds of threats at an application level. The only way to deal with them is at the OS or physical level. In short: you either airgap your computer (ridiculously expensive, only 3 letter agencies can afford to do this properly) or you use something like Qubes. To airgap properly, you need to figure out how to securely transfer information between your airgapped computer and non-airgapped computers. You can't use USB, as due to the complexity of the USB protocol there does not exist any secure USB stacks - if you plug a USB into a compromised machine, then the USB becomes compromised, and any future machines that you plug that USB into also become compromised (see stuxnet). On the other hand, if you use Qubes (or a similar solution), then you're relying on the security of Xen (which we already know is not very secure). Since all your VMs run on the same machine, you also open yourself up to hardware data leakages like meltdown (see QSB #37). In short, proper airgapping is the most secure but infeasible for ordinary people, so you have to use the less secure (but more practical) alternatives such as Qubes. 

If you are really worried about physical theft or your cloud backup getting leaked I would recommend using multiple layers of encryption, like using gpg and openssl on top of pynacl. This is to protect against the case where pynacl is compromised (for example, PyPi is compromised, or one of the pynacl developers get compromised). The attacker would then have to also compromise both gpg and openssl. The more layers of encryption the better, as it means the attacker has to compromise more entities in order to get to your data. If you do this, it's imperative that:

1. you use different passwords for each layer, because if there really is a backdoor in one of the encryption programs, then it can reveal the password, in which case decrypting the inner layers becomes trivial. 
2. you encrypt each layer on a separate machine (physical or virtual), because if one program is compromised, it can easily seek out and compromise other programs. If using Qubes, you'd encrypt a file in one HVM, then transfer the file to another HVM to be encrypted again. With physical machines this becomes impractical, because you can't use USB. 

You will also need to make sure that your password and keys, as well as the plaintext, aren't stored anywhere. First, you need to make sure that content from your RAM is never written to persistent storage, such as the swap file. So you will need to disable swap, for starters. You also need to disable hibernation, as that writes the entire contents of your RAM to disk (although Microsoft Bitlocker is written with this specific threat in mind, so with Bitlocker on Windows it's okay to hibernate). Once you are certain that sensitive information is never written to persistent storage, then you need to ensure that you turn off your computer whenever you're going to leave it unattended (as in, proper shut down, never sleep), making sure that the RAM is depowered. There is a thing called a "cold boot attack" whereby an attacker can retrieve the contents of your RAM for a few seconds or minutes after it was depowered, so to be really safe you should wait for a few minutes after your RAM has been depowered before leaving it unattended. 

## Availability

Everyone loves to talk about bitrot. In theory, as circuits have gotten smaller and less power-hungry, they have become more vulnerable to radiation as now less energy is required to flip a bit. Also, as the size of storage and RAM has grown (and files), so has the probability of a random bit being flipped somewhere in RAM or on disk. A single bit flip on an encrypted file is **catastrophic**, as it means the entire contents of that file are lost, since decryption will fail if even a single bit anywhere in the file is flipped (you can mitigate this to some extent by encrypting your file in chunks. When a bit is flipped you then only lose the chunk where the bit flipped, rather than everything, though this is still bad). It is therefore absolutely **imperative** to protect encrypted files against bitflips. To protect against bitrot, the best solution is ECC. Tools such as PAR2 or WinRAR allow you to do this. 

In reality, you're very, very unlikely to ever see a bit flip on your hard disk, since they come with their own ECC. Therefore, I have not bothered with adding ECC to the file. You're much more likely to see burst errors: entire failed sectors on hard drives, or burst errors due to bad links. File corruption due to file system bugs are common, this can cause an entire 64kb chunk of data to be corrupted, though these errors usually happen during filesystem operations such as copy or "scrub". 

The 2 most common classes of data corruption errors occur during:

1. Data copying (on disk, over USB, or over the network)
2. Data storage (sitting on disk for long periods of time)

Errors that occur during data copying can happen through many possible mechanisms. Copying a file involves moving it through RAM, and since most consumer grade machines don't have ECC RAM, an error while copying gigabytes is likely. Also, receiving data over the network involves the data moving through the network card. Again, TCP can catch some bit errors, but its checksum is weak and should not be relied upon. You really need end-to-end checksums at the application layer. Strong checksums at the file level will catch any errors that happened during a file copy - once you have copied over the file, you simply verify its checksum, and that's job done. This program uses pynacl's default encryption mode, which is an AEAD - it includes a MAC, which achieves both authentication and integrity. A checksum/hash achieves only integrity. So if you have a MAC then you do not need a checksum/hash. To mitigate against file corruption when saving, which is where you write a file to disk that cannot be decrypted, this program first writes to a temporary file, then checks that the temporary file can be decrypted, before deleting the original and replacing it with the temporary file. 

Errors that occur during data storage, again, usually occurs as large continuous runs (hundreds) of bytes being corrupted, or entire sectors failing. To protect against random runs of bytes being corrupted (let's say a run of a few hundred bytes), you should have two copies of the same file. If your file is small, as text files generally are, then it's fairly unlikely for both copies to be corrupted, let alone corrupted in the same place. Also, since each file must occupy at least one OS block (so a 1 byte file on an OS with 4kb block size would occupy an entire 4kb block all by itself, the rest of the block is just wasted bytes), and each OS block consists of at least one disk sector, this means every file is stored on a different sector - a sector cannot contain multiple files. This would then protect against a random sector failing. So what this program does is it makes a backup copy of your file every time you save it, and checks that the backup copy is bit-for-bit identical to the original. 

There are other hard drive failure modes however which will wipe out multiple sectors at a time. To protect against these failures, you could have multiple partitions on your disk that are as far away from each other as possible, and keep one copy on each partition. But the most reliable way to defend against disk failures is obviously to store your file on multiple hard drives, as well as on the cloud. 

So here are the guidelines:

1. Make sure to check checksums whenever you copy or send a file, whether over the network or across disks. If you use this program, you can just try to open the file at the destination. If it opens then it was not corrupted during copying. 
2. Make sure you keep each file on multiple hard disks, at least 3, preferably each of different brand and manufacture date. 
3. Make sure you keep multiple copies of each file on each hard disk. This will protect against some file system bugs. 
4. Make sure to keep cloud backups with multiple cloud vendors. Cloud vendors have a high replication factor across multiple geographic regions. They take data loss seriously (so I don't think having multiple copies of the same file on your cloud account would make a difference). It's more important to use a different email account for each vendor, to prevent cases like Yahoo 2013 where every single Yahoo account (all 3 billion of them) got hacked. If you use one email address for all your cloud accounts then you have a single point of failure - if that one email account gets hacked then you lose all your backups, though if your email gets hacked then you likely have bigger problems than just losing your backups. 

If your file gets corrupted while it's open in the text editor, there is no sane way to detect that. You cannot sanely implement ECC memory in software. Even worse, if the program code gets corrupted while running, there's no way to detect that. I mean, you could keep a hash of the program code and check against it every once in a while. As for the contents, you cannot possibly know if a change was due to user action or due to a random bitflip. To protect against in-memory corruption, you could periodically check that the code you're running hasn't been corrupted. However, this is problematic, because the code and data caches are typically stored separately. That is, modern CPUs have a separate cache for instructions that are to be executed, vs data that is to be read (see: iCache, dCache, iTLB, dTLB). What this means that your program code is copied into two caches, one is used when the CPU executes your code, and the other one is used when the CPU reads your code. If the code in the iCache is corrupted, but the code in the dCache isn't, then you won't be able to notice when your code has silently been corrupted in memory. ECC RAM won't help against this, because the caches are in the CPU itself. You could however keep 2 copies of the program running, and check them against each other for every single operation. Even better would be to have multiple computers all run the same program and check their result against each other - this is used in the Saturn V rocket for example. To do this, you need 3 copies of the program each running on a separate CPU. Based on the 2009 study by Google, I would estimate that you have to have some really bad RAM in order to be affected by memory errors...but the probability of a DIMM being bad is not negligible. It might be something like 10-20%. So it is important to check your memory. If you're worried about this, get a computer that supports ECC RAM. This problem cannot be sensibly solved at the software level. 

# Keyboard shortcuts:

- Ctrl-s to save file (file will be automatically encrypted with your master password when saved - plaintext will be deleted - gone -  once you close the editor). Cool thing to notice is that every time you save, a new IV will be randomly generated so the ciphertext will be completely different to before (even if the plaintext is exactly the same)! Pretty cool imo. 
- Ctrl-w to close editor 
- Ctrl-a to select all
- Ctrl-l to select current line 
- Ctrl-f to enter search mode and search text
- Esc to exit search mode

Substitute Ctrl for Cmd if you're using a Mac keyboard. 

# Please be aware that the undo function is somewhat buggy so don't count on being able to undo any changes you make to the file. 
