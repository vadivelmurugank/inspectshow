

# Main Routine

if __name__ == "__main__":
    import sys
    import inspectshow

    display = inspectshow.tree()

    if len(sys.argv) < 2:
        display()
        sys.exit()

    if ((len(sys.argv) > 2) and (sys.argv[2] == "help")):
        pydoc.help(sys.argv[1])
        sys.exit()

    display(sys.argv[1])

