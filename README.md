#Rar/Zip Password Cracker in python.

I had to bruteforce a rar file in a ctf so wrote some ad-hoc code in python. 
Works in Linux/Windows.


```python```

`python bruteforce.py -f filetocrack.rar -c charset -s minsizeofpassword -e maxsizeofpassword -t usethreadsornot`

`python bruteforce.py -f RARFILE.rar -c abcdefghijklmnopqrst0123 -e 6`

`python bruteforce.py -f ZIPFILE.zip -c charset -s 1 -e 6 -t 0`

