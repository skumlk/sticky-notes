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
    packages=['app', 'app.bin', 'app.shared'],
    include_package_data = True,
    package_data = {
        '' : ['*.png'],
    },
    entry_points = {
        'gui_scripts' : ['StickyNotes = app.main:main']
    },
    data_files = [
        ('share/applications/', ['StickyNoteApp.desktop'])
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)