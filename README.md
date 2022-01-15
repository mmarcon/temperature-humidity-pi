# How to make it work

Create a virtual environment and activate it

```
python3 -m venv .venv
source .venv/bin/activate
```


```shell
sudo apt install libgpiod2
sudo apt-get install python3-dev python3-pip
sudo python3 -m pip install --upgrade pip setuptools wheel
CFLAGS="-fcommon" pip3 install -r requirements.txt
```