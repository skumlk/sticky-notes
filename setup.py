import os
from setuptools import setup, find_packages

setup(
    name = "StickyNotes",
    version = "1.0",
    author = "Sameera Kumarasingha",
    author_email = "sameerakumarasingha@gmail.com",
    description = "Sticky Notes",
    license = "BSD",
    url = "https://github.com/skumlk/sticky-notes",
    packages=['skstickynotes', 'skstickynotes.bin', 'skstickynotes.shared'],
    include_package_data = True,
    package_data = {
        'skstickynotes.img' : ['skstickynotes/img/*.png'],
    },
    entry_points = {
        'gui_scripts' : ['StickyNotes = skstickynotes.main:main']
    },
    data_files = [
         ('share/applications/', ['StickyNoteApp.desktop']),
        ('share/icons/hicolor/scalable/apps', ['icon.png']),#main icon
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)