# gawker-archive

This is a file I wrote for some friends who used to work at Gawker to scrape their post archives into a text format. 

## OS X Installation Instructions:

1) Open a Terminal (Press Command-Space and type "Terminal")

2) Copy and paste the following commands

```
mkdir gawker
cd gawker
git clone --recursive https://github.com/Srol/gawker-archive
sudo easy_install pip
pip install -r requirements.txt
```

3) Run the script
```
python gawker.py --user your_username_here
```

Enjoy!

