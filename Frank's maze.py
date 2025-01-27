                        # Franks maze
#importy
                        
import tkinter as tk

#Hlavni menu

def Start_hry():
    print ("Bludiště začíná")
    
def otevri_nastaveni():
    print("Otevírání nastavení...")
    
def zavreni_hry():
    okno.destroy()
    
#rozliseni hlavniho menu
    
okno = tk.TK()
okno.title("Frank's maze")
okno.rozliseni("1000x1000")
    
    
    