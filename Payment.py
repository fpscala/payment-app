import os

import webview

from JavascriptApi import JavascriptApi


def load_js(window, path):
    with open(path, mode="r", encoding="utf-8") as f:
        window.evaluate_js(f.read())


if __name__ == '__main__':
    os.system('coffee --compile --output ./html/js/ ./html/coffee/')
    api = JavascriptApi()
    main_screen = webview.create_window('DATA LEARNING CENTER',
                                        'html/login.html', width=500, height=600, js_api=api, min_size=(500, 600),
                                        resizable=False)
    jsList = ['html/js/jquery.min.js',
      'html/js/knockout-min.js',
      'html/js/knockout.mapping-latest.js',
      'html/js/bootstrap-select.min.js',
      'html/js/moment.min.js',
      'html/js/toastr.min.js',
      'html/js/index.js']
    # for path in jsList:
    load_js(main_screen, 'html/js/jquery.min.js')
    api.set_main_screen(main_screen)
    webview.start(gui="qt")
