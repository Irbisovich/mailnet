import emailtools.client.emailrequests as requests
from tkinter.ttk import Progressbar
from tkinterweb import HtmlFrame
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import *
import json

from autologging import logged, TRACE, traced
import logging
import sys

root = Tk()
root.title("EMailNet")
root.geometry("800x600")

@logged
@traced
class Login:
    def __init__(self, master):
        self.configfile = open('config/config.json', 'w+')

        self.configfile.seek(0)
        if self.configfile.read().replace(' ', '') == '':
            self.configfile.write(json.dumps({}))
            self.configfile.flush()
            self.configfile.seek(0)

        self.configfile.seek(0)
        print(self.configfile.read())
        self.configfile.seek(0)
        self.config = json.loads(self.configfile.read())

        self.loginwindow = Toplevel(master)

        self.createlogwin()

    def update(self):
        self.config['email'], self.config['email_password'], self.config['crypto_password'] = self.login()

        self.configfile.seek(0)
        self.configfile.truncate()
        self.configfile.write(json.dumps(self.config))
        self.configfile.flush()

        try:
            for key in self.config:
                if self.config[key].replace(' ', '') == '':
                    raise Exception(f'{key.replace('_', ' ')[0].upper()}{key.replace('_', ' ')[1:-1].lower()}{key.replace('_', ' ')[-1].lower()} is empty.')

            if not '@' in self.config['email']:
                raise Exception('E-Mail is typed wrong.')

        except Exception as e:
            messagebox.showwarning('An error has occurred.', f'An error has occurred: {str(e)}\nTry again.')

        finally:
            self.loginwindow.destroy()

    def login(self):
        return [entry.get() for entry in self.entries]

    def createlogwin(self):
        self.entries, self.entriesdesc = [Entry(self.loginwindow), Entry(self.loginwindow), Entry(self.loginwindow)], [Label(self.loginwindow, text="E-Mail"), Label(self.loginwindow, text="E-Mail password"), Label(self.loginwindow, text="Crypto password")]

        for entrydesc in self.entriesdesc:
            self.entriesdesc[self.entriesdesc.index(entrydesc)].grid(column=0, row=self.entriesdesc.index(entrydesc), padx=5, pady=5)
            self.entries[self.entriesdesc.index(entrydesc)].grid(column=1, row=self.entriesdesc.index(entrydesc), padx=5, pady=5)

        Button(self.loginwindow, text='Login', command=self.update).grid(column=0, row=len(self.entriesdesc), sticky='nsew', padx=5, pady=5)

def updateresponse():
    responsetext.delete(1.0, END)
    responsetext.configure(state="normal")
    html = requests.get(email=json.loads(open('config/config.json').read())['email'], password=json.loads(open('config/config.json').read())['email_password'], to=goentry.get().split('/')[0], page=f'/{'/'.join(goentry.get().split('/')[1:])}', progbar=waitbar).split('\r\n\r\n')[-1]
    responsetext.insert(INSERT,
                        html
    )
    html_frame.load_html(html)
    responsetext.configure(state="disabled")

menu = Menu(root)
menu.add_command(label='Login', command=lambda x=None: Login(root))
menu.add_command(label='Save')
menu.add_command(label='About')
menu.add_command(label='Help')

gobtn = Button(root, text='Go', command=updateresponse)
goentry = Entry(root)
waitbar = Progressbar(root, length=100)
responsetext = scrolledtext.ScrolledText(root, state="disabled")
html_frame = HtmlFrame(root)

gobtn.place(relwidth=0.1, relheight=0.04, relx=0.9, rely=0)
goentry.place(relwidth=0.9, relheight=0.04, relx=0, rely=0)
waitbar.place(relwidth=1, relheight=0.03, relx=0, rely=0.04)
responsetext.place(relwidth=0.1, relheight=0.93, relx=0.9, rely=0.07)
html_frame.place(relwidth=0.9, relheight=0.93, relx=0, rely=0.07)
html_frame.load_html('<h1>Hello! Go to %%% insert your page %%% page</h1>')

logging.basicConfig(level=TRACE, stream=sys.stderr, format="%(levelname)s: %(filename)s (%(lineno)d): %(name)s.%(funcName)s - %(message)s")

root.config(menu=menu)
root.mainloop()
