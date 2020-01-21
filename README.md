# Cookie sharing example

## Installation

Before this, make sure a redis-server already running on 127.0.0.1:6379

```
sudo apt python3-pip
pip3 install flask redis --user
```

## Usage

```
python3 app.py &
python3 shared.py &
# running
```

1. access `localhost:6969`
2. try to click `restricted page` (for proof if user hasn't login)
3. input username `kuda` & password `kuda`
4. click login

## Proof on cookie sharing

1. run both `app.py` and `shared.py`
2. access `localhost:3002` to ensure you aren't logged in
3. access `locahost:3001` to login
4. after logged in, try to access `localhost:3002` again
5. the page should return "SUKSES LOGIN!"