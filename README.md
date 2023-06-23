# Backdoor
A backdoor program written in Python that works in conjunction with a server program that allows the user to control a target machine. 
The backdoor uses Python's socket, time, subprocess, json, and os libraries. The backdoor program has functions that: send data & receive data, connect to a specific Kali Linux machine over a specific port number, upload & download files, and mimics a shell terminal for issuing commands to the target machine.
The server program uses Python's socket, json, and os libraries. The server program has functions that: send & receive data, upload & download files, and sends user commands to the backdoor program on a target computer.
