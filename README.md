# Honeypots


## SSH honeypot script

Goal is to deploy a simple SSH honeypot to catch hackers and bots

### Deploy 

1. Generate a pair of ssh key 

``
ssh-keygen -t rsa -f server_key
``


2. Edit the variable HOST_KEY_PATH = 'server_key' with the path of your new server_key



3. Launch the script in background

```
nohup python3 main.py > /dev/null 2>&1 &
```

4. Sanetise the ouptut 

```
pyton3 data-correlation.py
```


## Web honeypot

Goal is to emulate a fake login page with Flask , nothing is behind this webserver.

### Prerequistes

- flask 
- python3

### Deploy 

1. Run the script 

```
python3 /web-honeypot/main.py
```

2. Observe attack pattern in all_requests.txt files output


