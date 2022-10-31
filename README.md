# Scripts for Rasptank
---
### Newest recommed
--- 
## Important
### 1.1 Cam 
The camera is right now not in use.

### 1.2 Setup
The Raspberry need a Setup. You will find a automatically Setup [here](https://github.com/adeept/Adeept_RaspTank).
(Download and run _setup.py_ on Raspberry; The Script is from _Adeept_) 

### 1.3 sys_info.py
_sys_info.py_ is for the Raspberry. 
To make it work, you need to install _psutil_. Run "pip3 install psutil" on Terminal on Raspberry. 

---

## How to use
### 2.1 Server and Client
The Servers are for the Raspberry and the Clients for your PC. 
You will find 2 different Servers:
+ Server V1 is compatible with:
    + Client V1
    + Client V2.1
+ Server V2 ist compatible with:
    + Client V2.2

You won't need all. 

### 2.2 Client
You have to put your Raspberrys IP-Addres in the Client script that you use. 
```
15. 【...】
16.  ip_addr = [your ip_addres]
17. 【...】
```
(always Line 16 )

### 2.3 Paths
For _Client_V2_2.py_ you need to write in the path of _bg.jpg_ in Line 334.
