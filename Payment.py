import os
import sys

import webview

from JavascriptApi import JavascriptApi

if __name__ == '__main__':
    os.system('coffee --compile --output ./html/js/ ./html/coffee/')
    api = JavascriptApi()
    main_screen = webview.create_window('DATA LEARNING CENTER',
                                        'html/login.html', width=500, height=600, js_api=api, min_size=(500, 600),
                                        resizable=False)
    api.set_main_screen(main_screen)
    if sys.platform.startswith('linux'):
        webview.start(gui="qt")
    else:
        webview.start(gui="cef")
