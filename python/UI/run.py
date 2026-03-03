'''
File that is used for running all UI elements within the app

MAY BE UNNECESSARY ONCE MERGED WITH REST OF APPLICATION
'''

import flet as ft

from pages.homepage import main

ft.run(main, assets_dir='assets')