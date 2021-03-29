init:
    pip install -r requirements.txt

exe:
    pyinstaller -F -w -n Qix main.py

.PHONY: init exe.