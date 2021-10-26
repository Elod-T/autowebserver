# Automatically create a docker container from your existing website with SSL!

## Step 0:
Make sure you have [docker](https://docs.docker.com/get-docker/) and [python](https://www.python.org/downloads/) installed.

## Step 1:
Clone this repo.
```bash
git clone https://github.com/Elod044/autowebserver/
```

## Step 2:
Install the required packages!
```bash
pip install requirements.txt
```

## Step 3:
Put all of your html files inside the /html folder, and put your SSL certificate in the /ssl folder. If you don't have any the script will auto generate one for you!

## Step 4:
Run main.py with your desired flags!
```
python main.py -name test
```
Optional flags:
- -autostart, after the image was created it starts a container with it
- -export, after the image was created (and started) it exports the image to the main directory
```
python main.py -name test -autostart -export
```
