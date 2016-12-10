#!/usr/bin/python3
import getopt
import os
import platform
import subprocess
import sys
import tempfile


def usage():
    print("Usage: ", end="", flush=True)
    print(os.path.basename(sys.argv[0]) + " [-hkr] [-c COMPILER] [-l LINKER] [-t TEMPDIRECTORY] [-f FORMAT] INPUTFILE OUTPUTFILE")
    print("\t-h\t--help\t\t\tPrint this help.\n\t-k\t--keep-cfile\tDon't remove compiled file after successful linking.\n\t-r\t--autorun\t\tAutomatically run the program after successful linking.\n\t-c\t--compiler\t\tSelect alternative compiler. Defaults to nasm.\n\t-l\t--linker\t\tSelect alternative linker. Defaults to ld.\n\t-t\t--temp-dir\t\tChange where to save the object file if you wish to keep it.\n\t-f\t--format\t\tChange the target format. Defaults to ELF on Unix, Win32/64 on Windows and BIN on unrecognized OSes.")


def main(argv):
    asmFile = ''
    asmHandler = 'nasm'
    asmLinker = 'ld'
    tmpDir = tempfile.gettempdir()
    removeObjAfterCompilation = True
    outputFile = ''
    runAfterwards = False
    asmFormat = None
    if platform.os.name == 'posix':
        if platform.machine() == "x86_64":
            asmFormat = "elf64"
        else:
            asmFormat = "elf32"
    elif platform.os.name == 'nt':
        if platform.machine() == "x86_64":
            asmFormat = "win64"
        else:
            asmFormat = "win32"
    else:
        print("Warning: Couldn't recognize host OS. Make sure the format is correct.")
        asmFormat = "bin"


    try:
        opts, args = getopt.gnu_getopt(argv, "hkl:c:t:f:r",
                                       ["help", "keep-cfile", "linker=", "compiler=", "temp-dir=", "format=", "autorun"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-k", "--keep-cfile"):
            removeObjAfterCompilation = False
        elif o in ("-l", "--linker"):
            asmLinker = a
        elif o in ("-c", "--compiler"):
            asmHandler = a
        elif o in ("-t", "--temp-dir"):
            if os.path.isdir(a):
                tmpDir = a
            else:
                print("{0} is not a directory!".format(a))
                sys.exit(2)
        elif o in ("-r", "--autorun"):
            runAfterwards = True
        elif o in ("-f", "--format"):
            asmFormat = a
        else:
            assert False, "unhandled option"

    if len(args) != 2:
        print("Incorrect amount of arguments: " + str(args))
        usage()
    else:
        asmFile = args[0]
        outputFile = args[1]
        if os.path.isfile(asmFile):
            objectPath = os.path.abspath(tmpDir) + "/qasml-" + os.path.basename(outputFile) + ".o"
            # print("Compiling {0} with {1}, linking to {2} with {3}.".format(asmFile, asmHandler, outputFile, asmLinker))
            buildCommand = [asmHandler, asmFile, "-f", asmFormat, "-o", objectPath]
            print("Running: " + " ".join(buildCommand))

            if subprocess.call(buildCommand) != 0:
                print("\nSomething went wrong, you're on your own.")
                sys.exit(127)
            print("OK!")

            linkCommand = [asmLinker, objectPath, "-o", outputFile]
            print("Running: " + " ".join(linkCommand))
            if subprocess.call(linkCommand) != 0:
                print("\nSomething went wrong, you're on your own.")
                os.remove(objectPath)
                sys.exit(127)
            print("OK!")

            if removeObjAfterCompilation:
                print("Cleaning up " + objectPath)
                os.remove(objectPath)

            if runAfterwards:
                print("Running: " + outputFile)
                if subprocess.call([os.path.abspath(outputFile)]) != 0:
                    print("\nSomething appears to have gone wrong, don't care at this point.")

        else:
            print("{0} doesn't seem to exist.".format(asmFile))
            sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
