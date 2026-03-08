# pynter - entry point
# run:  python pynter.py

from pynter.main_window import MainWindowGUI


def main():
    app = MainWindowGUI()
    app.init()
    try:
        app.start_loop()
    except KeyboardInterrupt:
        pass  # user pressed ctrl+c, just quit
    finally:
        # finally runs even if theres an error, so pygame always gets cleaned up
        app.shutdown()


if __name__ == "__main__":
    main()
