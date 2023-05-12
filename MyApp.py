from CoreOOP import *
import sys

def main():
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = My_UI()
    window.show()
    with loop:
        sys.exit(loop.run_forever())
if __name__ == "__main__":
    main()

