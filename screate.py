import os, sys, getpass
from cryptotest import encrypt

def getpassword() -> str:
    """
        This function has been manually tested.

        It successfully detects and exits when user enters a blank password,
        or when the user enters 2 passwords that don't match.
    """
    password1 = getpass.getpass("Enter a password: ")
    password2 = getpass.getpass("Enter the password again: ")
    if password1 != password2:
        print("Passwords do not match.")
        exit(1)
    if not password1:
        print("YOU MUST ENTER A PASSWORD!")
        exit(1)
    return password1

def createfile(filename: str) -> str:
    # create the file
    print("You will now be asked to enter a password for the new file.")
    try:
        password = getpassword()
    except Exception as e:
        print(e)
        exit(1)
    try:
        with open(filename, 'xb') as f:
            ciphertext = encrypt("You can write your stuff in this file.", password)
            f.write(ciphertext)
            print("File " + filename + " was successfully created.")
            print("You can open the file with the following command:")
            print("    python3 sopen.py " + filename)
    except Exception as e:
        print(e)
        print("An error occurred while creating the file. See above.")
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: screate.py filename")
        exit(0)
    fn = sys.argv[1]
    fn = os.path.abspath(fn) # just for insurance.
    createfile(fn)
