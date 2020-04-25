import sys
import menu

if __name__ == "__main__":
    _menu = menu.Menu()
    
    try:
        _menu.start()
    except Exception as err_msg:
        print(f'Catching exception: {err_msg}')
        _menu.quit()
