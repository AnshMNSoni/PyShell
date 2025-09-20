from tkinter import *
import random
from tkinter import messagebox

THEME_COLOR = "#375362"
FONT=('Courier', 18, 'bold')

class GameUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('Rock Paper Scissor Game')
        self.window.config(bg=THEME_COLOR, highlightthickness=0, padx=40, pady=40)
        
        # Match Label:
        self.userscore = Label(text='Match', font=FONT, bg=THEME_COLOR, fg='white', highlightthickness=0)
        self.userscore.grid(row=0, column=2)
        
        
        # User Score:
        self.user_score = 0
        self.userscore = Label(text='Score :: 0', font=FONT, bg=THEME_COLOR, fg='white', highlightthickness=0)
        self.userscore.grid(row=0, column=1)
        
        # Computer Score:
        self.computer_score = 0
        self.computerscore = Label(text='Score :: 0', font=FONT, bg=THEME_COLOR, fg='white', highlightthickness=0)
        self.computerscore.grid(row=0, column=3)
        
        # Rock Button:
        self.img_rock = PhotoImage(file='game/Rock-Paper-Scissor/Rock.png')
        self.rock_button = Button(image=self.img_rock,bg=THEME_COLOR, highlightthickness=0, command=self.rock_pressed)
        self.rock_button.grid(row=1, column=0, pady=20)
        self.rock_button.config(bg=THEME_COLOR, highlightthickness=0)
        
        # Paper Button:
        self.img_paper = PhotoImage(file='game/Rock-Paper-Scissor/Paper.png')
        self.paper_button = Button(image=self.img_paper,bg=THEME_COLOR, highlightthickness=0, command=self.paper_pressed)
        self.paper_button.grid(row=2, column=0)
        self.paper_button.config(bg=THEME_COLOR, highlightthickness=0)
        
        # Scissors Button:
        self.img_scissor = PhotoImage(file='game/Rock-Paper-Scissor/Scissors.png')
        self.scissor_button = Button(image=self.img_scissor,bg=THEME_COLOR, highlightthickness=0, command=self.scissor_pressed)
        self.scissor_button.grid(row=3, column=0, pady=20)
        self.scissor_button.config(bg=THEME_COLOR, highlightthickness=0)
        
        # End Button:
        self.end_button = Button(text='End Game', command=self.End, fg='white', bg=THEME_COLOR, highlightthickness=0, font=FONT)
        self.end_button.grid(row=4, column=0)
        
        # User Label:
        self.user_label = Label(text='User', bg=THEME_COLOR, fg='white', highlightthickness=0, font=FONT)
        self.user_label.grid(row=4, column=1, padx=20) 
        
        # User Canvas:
        self.user_canvas = Canvas(height=240, width=240)
        self.user = self.user_canvas.create_image(120, 120, image=None)
        self.user_canvas.config(bg='grey', highlightthickness=0)
        self.user_canvas.grid(row=1, column=1, rowspan=3, padx=40)
        
        
        # Computer Label:
        self.user_label = Label(text='Computer', bg=THEME_COLOR, fg='white', highlightthickness=0, font=FONT)
        self.user_label.grid(row=4, column=3, padx=20)
        
        # Computer Canvas:
        self.computer_canvas = Canvas(width=240, height=240)
        self.computer = self.computer_canvas.create_image(120, 120, image=None)
        self.computer_canvas.config(bg='grey', highlightthickness=0)
        self.computer_canvas.grid(row=1, column=3, rowspan=3, padx=20)
        
        # Getting Random from Rock-Paper-Scissors:
        self.img_Big_Rock = PhotoImage(file='game/Rock-Paper-Scissor/Big_Rock.png')
        self.img_Big_Paper = PhotoImage(file='game/Rock-Paper-Scissor/Big_Paper.png')
        self.img_Big_Scissor = PhotoImage(file='game/Rock-Paper-Scissor/Big_Scissors.png')
        
        self.computer_image = [self.img_Big_Rock, self.img_Big_Paper, self.img_Big_Scissor]
        
        # Interactive to User :: Win / Lose / Tie
        self.result = Label(text=None, bg=THEME_COLOR , fg=THEME_COLOR, font=('Courier', 20, 'italic'))
        self.result.grid(row=2, column=2)
        
        self.window.mainloop()
        
        
    def rock_pressed(self):
        self.change_background()
        self.user_canvas.itemconfig(self.user, image=self.img_Big_Rock)
        self.computer_Big_img()
        self.game_logic(0)
        
    def paper_pressed(self):
        self.change_background()
        self.user_canvas.itemconfig(self.user, image=self.img_Big_Paper)
        self.computer_Big_img()
        self.game_logic(1)
        
    def scissor_pressed(self):
        self.change_background()
        self.user_canvas.itemconfig(self.user, image=self.img_Big_Scissor)
        self.computer_Big_img()
        self.game_logic(2)
        
    def computer_Big_img(self):
        self.random_int = random.randint(0, 2)
        self.random_img = self.computer_image[self.random_int]
        self.computer_canvas.itemconfig(self.computer, image=self.random_img)
        
    def change_background(self):
        self.user_canvas.config(bg = THEME_COLOR)
        self.computer_canvas.config(bg = THEME_COLOR)
        
    def game_logic(self, num):
        if (num == 0):
            if (self.random_int == 0):
                self.Tie()
            elif (self.random_int == 1):
                self.Lose()
            elif(self.random_int == 2):
                self.Win()
        
        elif (num == 1):
            if (self.random_int == 0):
                self.Win()
            elif (self.random_int == 1):
                self.Tie()
            elif(self.random_int == 2):
                self.Lose()
        
        elif (num == 2):
            if (self.random_int == 0):
                self.Lose()
            elif (self.random_int == 1):
                self.Win()
            elif(self.random_int == 2):
                self.Tie()
        
    def Win(self):
        self.user_score += 1
        self.userscore['text'] = f"Score :: {self.user_score}"
        
        self.result.config(text='Win', bg='green', fg='white')
        
        
    def Lose(self):
        self.computer_score += 1
        self.computerscore['text'] = f"Score :: {self.computer_score}"
        
        self.result.config(text='Lose', bg='red', fg='white')
        
    def Tie(self):
        self.result.config(text='Tie', bg='yellow', fg='black')
        
        
    def End(self):
        is_yes= messagebox.askyesno(message=f"Your Score :: {self.user_score} \n\nWant to play again?")
        
        if is_yes:
            # Reset score:
            self.user_score = 0
            self.userscore['text'] = f"Score :: {self.user_score}"
            
            self.computer_score = 0
            self.computerscore['text'] = f"Score :: {self.computer_score}"
            
            # Reset canvases:
            self.img_grey = PhotoImage(file='game/Rock-Paper-Scissor/grey.png')
            self.user_canvas.itemconfig(self.user, image=self.img_grey)
            self.computer_canvas.itemconfig(self.computer, image=self.img_grey)
            
            # Reset Result Label:
            self.result.config(text=None, bg=THEME_COLOR, fg=THEME_COLOR)
            
        else:
            self.window.quit()

        
GameUI()