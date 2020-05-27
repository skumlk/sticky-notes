# sticky-notes
Cross platform sticky notes application

# Compile
python3 setup.py --command-packages=stdeb.command bdist_deb

# Install
sudo dpkg -i ./deb_dist/python3-stickynotes_1.0-1_all.deb 