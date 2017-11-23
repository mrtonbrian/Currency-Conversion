from Tkinter import *
from requests import *
import json
from tkMessageBox import *
import clipboard
import sys
class converter:
    def __init__(self,master):
        #All Options For Dropdown Currency Menu
        options = [
            "USD (US Dollar)",
            "EUR (Euro)",
            "BGN (Bulgarian Lev)",
            "BRL (Brazilian Real)",
            "CAD (Canadian Dollar)",
            "CHF (Swiss Franc)",
            "CNY (Chinese Yuan)",
            "CZK (Czech Koruna)",
            "DKK (Danish Krone)",
            "GBP (British Pound)",
            "HKD (Hong Kong Dollar)",
            "HRK (Croatian Kuna)",
            "HUF (Hungarian Forint)",
            "IDR (Indonesian Rupiah)",
            "ILS (Israeli New Shekel)",
            "INR (Indian Rupee)",
            "JPY (Japanese Yen)",
            "KRW (South Korean Won)",
            "MXN (Mexican Peso)",
            "MYR (Malaysian Ringgit)",
            "NOK (Norwegian Krone)",
            "NZD (New Zealand Dollar",
            "PHP (Phillipine Peso)",
            "PLN (Polish Zloty)",
            "RON (Romanian Leu)",
            "RUB (Russian Ruble)",
            "SEK (Swedish Krona)",
            "SGD (Sudanese Pound)",
            "THB (Thai Baht)",
            "TRY (Turkish Lira)",
            "ZAR (South African Rand)"
        ]
        self.master = master
        self.frame = Frame(self.master)
        #Creates The Leftmost Textbox
        self.left_entry = Entry(master)
        self.left_entry.grid(row=0)
        #Creates a Variable that Will Store Dropdown Selection
        self.variablel = StringVar(master)
        #Sets Default Option To USD
        self.variablel.set(options[0])
        #Creates Option Menu (Dropdown)
        self.choose_left = apply(OptionMenu,(master,self.variablel)+tuple(options))
        self.choose_left.grid(row=0,column = 1)
        #Added For Spacing
        Label(text = "     ").grid(row=0,column=2)
        #Flips Data (Left Data To Right, Vice Versa)
        self.switch_button = Button(master,text="Switch Data",command = self.switch).grid(row=0,column=3)
        #Conversion Button
        self.convert = Button(master,text = "Convert",command = self.convert_money).grid(row=0,column = 4)
        #Spacing
        Label(text="     ").grid(row=0, column=5)
        self.variable_r = StringVar(master)
        self.variable_r.set(options[1])
        self.choose_right = apply(OptionMenu,(master,self.variable_r)+tuple(options))
        self.choose_right.grid(row=0,column = 6)
        self.right_entry = Entry(master,state=DISABLED)
        self.right_entry.grid(row=0,column=7)
        #Copying to Clipboard
        self.copy_butt = Button(master,text = "Copy Converted Amount", command = self.copy_to_clip)
        self.copy_butt.grid(row=1,column= 3)
    # Copying To Clipboard Function
    def copy_to_clip(self):
        #Checks To See If Entry Is Empty
        if not len(self.right_entry.get()) == 0:
            #Gets Entry Data / Copies It
            clipboard.copy(self.right_entry.get())
        else:
            #Shows Error Message
            showerror("Empty String","Cannot Copy Empty String!")
    #Function To Switch Data
    def switch(self):
        #Storing Current Data
        self.right_entry.config(state=NORMAL)
        left_amount = self.left_entry.get()
        right_amount = self.right_entry.get()
        left_curr = self.variablel.get()
        right_curr = self.variable_r.get()
        #Switching Data To Other Side
        self.variable_r.set(left_curr)
        self.variablel.set(right_curr)
        self.left_entry.delete(0,END)
        self.right_entry.delete(0,END)
        self.left_entry.insert(0,right_amount)
        self.right_entry.insert(0,left_amount)
        self.right_entry.config(state=DISABLED)
    #Conversion Function
    def convert_money(self):
        #Checks To See If Both Currencies Are Same; If So: Show Error Message
        if not self.variable_r.get() == self.variablel.get():
            #Checks To See if Input Is Empty; If it is, show Error Message
            if not len(self.left_entry.get()) == 0:
                #Changes Base Url
                self.right_entry.config(state=NORMAL)
                base_url = "https://api.fixer.io/latest?base="
                left_chooser = self.variablel.get()
                base_url += str(left_chooser[0:3])
                #Get Request
                c = get(base_url)
                #Conversion
                c.json()
                #Load Json Into Json Lib
                result = json.loads(c.text)
                right_chooser = self.variable_r.get()
                #Finds the Rate For Selected End Currency
                exchange_rate = result['rates'][right_chooser[0:3]]
                #Insert Data Into Textbox
                self.right_entry.delete(0,END)
                start_money = self.left_entry.get()
                self.right_entry.insert(0,str(round(float(start_money)*float(exchange_rate),4)))
                self.right_entry.config(state=DISABLED)
            else:
                showerror("Empty Input","You Didn't Input Any Data!")
        else:
            showwarning("Same Currency","Just FYI \n Converting the Same Currency Is Redundant! \n Change The Currency")
#Shows Help Info
def help():
    showinfo("Help","First, Input Starting Amount Into Left Textbox \n \n Then, Click The Convert Button \n  \n If You Want To Switch The Two Sides' Data, Click The Switch Data Button \n \n If You Want To Copy The Output, Click The Copy Current Amount Button")
#Shows About Section
def about():
    showinfo("About This Program", "This Program Was Written By Brian Ton \n\nThis Program Uses fixer.io To Fetch Current Exchange Rates \n\nIf You Want To Contact Me, My Email Is mrtonbrian@gmail.com \n\n My GitHub is https://github.com/redder558")
#Exits Program
def exit_prog():
    sys.exit()
def main():
    root = Tk()
    c = converter(root)
    root.title("Currency Converter By: Brian Ton")
    menubar = Menu(root)
    #Help Menu Init
    menubar.add_command(label="Help", command=help)
    #About Menu Init
    menubar.add_command(label="About",command=about)
    menubar.add_command(label="Exit",command=exit_prog)
    root.config(menu=menubar)
    root.mainloop()
if __name__ == '__main__':
    main()