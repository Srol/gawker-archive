# gawker-archive

This is a file I wrote for some friends who used to work at Gawker to scrape their post archives into a text format. 

## OS X Installation Instructions:

1) Clone or download this repo
2) Unzip it.
3) Open a Terminal (Press Command-Space and type "Terminal"), and navigate to the repo. Assuming you downloaded and unzipped in the Downloads folder:
```
cd ~/Downloads/gawker-archive/master
```
4) Run the following command to download the pre-reqs. Your password will be required
```
sudo easy_install pip
```
5) Run this command to install the pre-eqs
```
pip install -r requirements.txt
```
6) Run the script
```
python gawker.py --user your_username_here
```
Enjoy!

