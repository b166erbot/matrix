from contextlib import suppress

from src.matrix import main


if __name__ == '__main__':
    with suppress((KeyboardInterrupt, EOFError)):
        main()
