# Pynter - entry point
# Run:  python pynter.py

from pynter.main_window import MainWindowGUI


def main():
    app = MainWindowGUI()
    app.init()
    try:
        app.start_loop()
    except KeyboardInterrupt:
        pass  # user pressed Ctrl+C, just quit
    finally:
        app.shutdown()  # clean up pygame


if __name__ == "__main__":
    main()
