# qasml.py
Python script for **Q**uickly **As**se**m**bling and **L**inking programs.

Simple script eliminating the need to manually run nasm and gcc/ld every time you want to rebuild your simple asm program.

# Usage
```
qasml.py [-hkr] [-c COMPILER] [-l LINKER] [-t TEMPDIRECTORY] [-f FORMAT] INPUTFILE OUTPUTFILE
-h	--help			Print this help.
-k	--keep-cfile	Don't remove compiled file after successful linking.
-r	--autorun		Automatically run the program after successful linking.
-c	--compiler		Select alternative compiler. Defaults to nasm.
-l	--linker		Select alternative linker. Defaults to ld.
-t	--temp-dir		Change where to save the object file if you wish to keep it.
-f	--format		Change the target format. Defaults to ELF on Unix, Win32/64 on Windows and BIN on unrecognized OSes.
```
