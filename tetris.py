import tkinter as tk
from tkinter import font
# import winsound as ws

import numpy as np




class Application(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        master.title("TETRIS")
        master.geometry("600x600")

        self.canvas = tk.Canvas(master, width=580, height=580)
        self.canvas.place(x=20, y=20)

        self.x = 4
        self.y = 0

        self.save_x = 0
        self.save_y = 0
        self.save_tetrimino = 0
        self.save_block_kind = 0
        self.save_next_color = 0
        self.save_rot_kind = 0
        self.shaffle_True = True

        self.turn_end_point = False
        self.type = "down"

        self.line_point = np.array([])
        self.change_check = 0

        self.count_mino = 0
        self.count_mino_array = np.array([1,0,2,6,4,5,3])
        
        self.block_size = 25
        self.stage_height = 20
        self.stage_width = 10

        self.tetri_mino = np.zeros((4, 2))
        self.block_color = "yellow"
        self.block_kind = 1
        self.rot_kind = 0
        self.rot_click = True

        self.btn_width = 10
        self.btn_height = 10
        self.btn_ok = True

        self.block_color_array = np.where(np.zeros((self.stage_height, self.stage_width))==0,\
            "gray95", "None")
        self.save_block_color_array = self.block_color_array.copy()
        self.stage_array = np.zeros((self.stage_height, self.stage_width))
        self.save_stage_array = np.zeros((self.stage_height, self.stage_width))

        self.game_continue = 0
        self.nextCanvas()
        self.makeStage()
        self.keyInput()
        self.startBtn()
        
        


    """ 
    def Movebutton(self):
        self.btnleft = tk.Button(self.master, text="left", command=self.leftMove, width=self.btn_width, height=self.btn_height)
        self.btnright = tk.Button(self.master, text="Right", command=self.rightMove, width=self.btn_width, height=self.btn_height)
        self.btndown = tk.Button(self.master, text="Down", command=self.downMove, width=self.btn_width, height=int(self.btn_height/2))
        self.btnrot = tk.Button(self.master, text="rot", command=self.rotMove, width=self.btn_width, height=int(self.btn_height/2))
        self.btnleft.place(x=300, y=325)
        self.btnrot.place(x=400, y=320)
        self.btnright.place(x=500, y=325)
        self.btndown.place(x=400, y = 410)
    """

    def nextCanvas(self):
        for i in range(4):
            for j in range(4):
                self.canvas.create_rectangle((i+13)*self.block_size, (j+5)*self.block_size, (i+14)*self.block_size, \
                    (j+6)*self.block_size, fill="gray", outline="gray95")
        font_next_canvas = font.Font(size=10, weight='bold')
        self.label_next = tk.Label(self.master, text="NEXT TETRIMINO", fg="red", bg="white", font=font_next_canvas)
        self.label_next.place(x=337, y=120)


    def makeNextBlock(self):
        self.save_x = self.x
        self.save_y = self.y
        self.save_tetrimino = self.tetri_mino
        self.save_block_kind = self.block_kind
        self.save_rot_kind = self.rot_kind
        self.save_next_color = self.block_color
        
        self.rot_kind = 0

        if self.shaffle_True:
            if self.count_mino == 6:
                    self.shaffleBlockArray()
                    self.shaffle_True = False
                    self.block_kind = self.count_mino_array[0]
            else:
                self.block_kind  = self.count_mino_array[self.count_mino+1]

            if self.block_kind == 0 or self.block_kind == 2:
                self.x = 15
                self.y = 7
            elif self.block_kind == 3 or self.block_kind == 5 or self.block_kind ==6:
                self.x = 14
                self.y = 7
            elif self.block_kind == 4:
                self.x = 14
                self.y = 8
            else:
                self.x = 15
                self.y = 6
            
            self.makeTetrimino()

            self.canvas.delete("next")

            for i in range(4):
                self.canvas.create_rectangle(self.tetri_mino[i][0]*self.block_size, self.tetri_mino[i][1]*self.block_size, \
                    (self.tetri_mino[i][0]+1)*self.block_size, (self.tetri_mino[i][1]+1)*self.block_size, \
                        fill=self.block_color, tag="next")
        
        self.x = self.save_x
        self.y = self.save_y
        self.tetri_mino = self.save_tetrimino
        self.block_kind = self.save_block_kind
        self.block_color = self.save_next_color
        self.rot_kind = self.save_rot_kind
    

    def startBtn(self):
        font_st = font.Font(family='Helvetica', size=50, weight='bold')
        self.start_btn = tk.Button(self.master, text="start", font=font_st, command=self.gameStart)
        self.start_btn.place(x=200, y=200)


    def gameStart(self):
        self.start_btn.place_forget()
        self.oneGame()
        

    def keyInput(self):
        self.button1 = self.master.bind('<Left>', self.leftMove)
        self.button2 = self.master.bind('<Right>', self.rightMove)
        self.button3 = self.master.bind('<Down>', self.downMove)
        self.button4 = self.master.bind('<space>', self.rotMove)

    
    def unkeyInput(self):
        self.master.unbind('<Left>', self.button1)
        self.master.unbind('<Right>', self.button2)
        self.master.unbind('<Down>', self.button3)
        self.master.unbind('<space>', self.button4)


    def leftMove(self, event):
        if self.btn_ok:
            self.btn_ok = False
            self.master.after_cancel(self.nextid)
            self.type = "left"
            self.y -= 1
            self.x -= 1
            self.oneGame()
        
        
    def rightMove(self, event):
        if self.btn_ok:
            self.master.after_cancel(self.nextid)
            self.btn_ok = False
            #self.master.after(50)
            self.type="right"
            self.y -= 1
            self.x += 1
            self.oneGame()


    def downMove(self, event):
        if self.btn_ok:
            self.btn_ok = False
            self.master.after_cancel(self.nextid)
            self.type="down"
            self.oneGame()


    def rotMove(self, event):
        if self.btn_ok:
            self.btn_ok = False
            # self.y
            self.master.after_cancel(self.nextid)
            #self.master.after(50)
            self.type="rot"
            if self.rot_kind == 3:
                self.rot_kind = 0
            else:
                self.rot_kind += 1
            self.oneGame()


    def makeStage(self):
        for i in range(self.stage_width):
            for j in range(self.stage_height):
                self.canvas.create_rectangle(i*self.block_size, j*self.block_size, \
                    (i+1)*self.block_size, (j+1)*self.block_size, fill="gray", outline="gray95")


    def makeTetrimino(self):
        if self.block_kind == 0:
            if self.rot_kind == 0:
                self.O_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y+1],
                    [self.x, self.y+1],
                    [self.x+1, self.y]
                ])
            elif self.rot_kind == 1:
                self.O_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y+1],
                    [self.x, self.y+1],
                    [self.x+1, self.y]
                ])
            elif self.rot_kind == 2:
                self.O_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y+1],
                    [self.x, self.y+1],
                    [self.x+1, self.y]
                ])
            else:
                self.O_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y+1],
                    [self.x, self.y+1],
                    [self.x+1, self.y]
                ])    
            self.tetri_mino = self.O_tetri_mino
            self.block_color = "yellow"

        elif self.block_kind == 1:
            if self.rot_kind == 0:
                self.I_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x, self.y+1],
                    [self.x, self.y+2]
                ])
            elif self.rot_kind == 1:
                self.I_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x+1, self.y],
                    [self.x-2, self.y]
                ])
            elif self.rot_kind == 2:
                self.I_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x, self.y-2],
                    [self.x, self.y+1]
                ])
            else:
                self.I_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x-1, self.y],
                    [self.x+2, self.y]
                ])
            self.tetri_mino = self.I_tetri_mino
            self.block_color = "cyan"
        
        elif self.block_kind == 2:
            if self.rot_kind == 0:
                self.L_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x, self.y+1],
                    [self.x+1, self.y+1]
                ])
            elif self.rot_kind == 1:
                self.L_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x-1, self.y],
                    [self.x-1, self.y+1]
                ])
            elif self.rot_kind == 2:
                self.L_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x-1, self.y-1],
                    [self.x, self.y+1]
                ])
            else:
                self.L_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x+1, self.y],
                    [self.x+1, self.y-1]
                ])
            self.tetri_mino = self.L_tetri_mino
            self.block_color = "orange"

        elif self.block_kind == 3:
            if self.rot_kind == 0:
                self.S_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x, self.y+1],
                    [self.x-1, self.y+1]
                ])
            elif self.rot_kind == 1:
                self.S_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x-1, self.y-1],
                    [self.x, self.y+1]
                ])
            elif self.rot_kind == 2:
                self.S_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x, self.y-1],
                    [self.x+1, self.y-1]
                ])
            else:
                self.S_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x+1, self.y],
                    [self.x+1, self.y+1]
                ])
            self.tetri_mino = self.S_tetri_mino
            self.block_color = "green"

        elif self.block_kind == 4:
            if self.rot_kind == 0:
                self.T_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x-1, self.y],
                    [self.x+1, self.y]
                ])
            elif self.rot_kind == 1:
                self.T_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x, self.y-1],
                    [self.x, self.y+1]
                ])
            elif self.rot_kind == 2:
                self.T_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y+1],
                    [self.x-1, self.y],
                    [self.x+1, self.y]
                ])
            else:
                self.T_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x, self.y-1],
                    [self.x, self.y+1]
                ])
            self.tetri_mino = self.T_tetri_mino
            self.block_color = "pink"
            
        elif self.block_kind == 5:
            if self.rot_kind == 0:
                self.Z_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x, self.y+1],
                    [self.x+1, self.y+1]
                ])
            elif self.rot_kind == 1:
                self.Z_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x-1, self.y],
                    [self.x-1, self.y+1]
                ])
            elif self.rot_kind == 2:
                self.Z_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x, self.y-1],
                    [self.x-1, self.y-1]
                ])
            else:
                self.Z_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x, self.y+1],
                    [self.x+1, self.y-1]
                ])
            self.tetri_mino = self.Z_tetri_mino
            self.block_color = "red"

        elif self.block_kind == 6:
            if self.rot_kind == 0:
                self.J_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x, self.y+1],
                    [self.x-1, self.y+1]
                ])
            elif self.rot_kind == 1:
                self.J_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x+1, self.y],
                    [self.x-1, self.y],
                    [self.x-1, self.y-1]
                ])
            elif self.rot_kind == 2:
                self.J_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x, self.y-1],
                    [self.x+1, self.y-1],
                    [self.x, self.y+1]
                ])
            else:
                self.J_tetri_mino = np.array([
                    [self.x, self.y],
                    [self.x-1, self.y],
                    [self.x+1, self.y],
                    [self.x+1, self.y+1]
                ])
            self.tetri_mino = self.J_tetri_mino
            self.block_color = "blue"


    def shaffleBlockArray(self):
        x = np.array([0, 1, 2, 3, 4, 5, 6])
        self.count_mino_array = np.random.permutation(x)


    def addBlockKind(self):
        if self.count_mino == 6:
                self.count_mino = 0
        else:
            self.count_mino += 1
        self.block_kind = self.count_mino_array[self.count_mino]


    def judgeBoundary(self):
        while not np.all(self.tetri_mino.T[0] >= 0):
            self.x += 1
            self.makeTetrimino()
        while not np.all(self.tetri_mino.T[0] <= 9):
            self.x -= 1
            self.makeTetrimino()
        while not np.all(self.tetri_mino.T[1] >= 0):
            self.y += 1
            self.makeTetrimino()
        while not np.all(self.tetri_mino.T[1] <= 19):
            self.y -= 1
            self.makeTetrimino()
            if self.rot_kind != "rot":
                self.turn_end_point = True


    def setArray(self):
        self.stage_array = self.save_stage_array.copy()
        self.block_color_array = self.save_block_color_array.copy()
        for k in range(self.tetri_mino.shape[0]):
            self.stage_array[self.tetri_mino[k][1]][self.tetri_mino[k][0]] += 1
            self.block_color_array[self.tetri_mino[k][1]][self.tetri_mino[k][0]] = self.block_color


    def judgementTwo(self):
        while not np.all(self.stage_array < 2):
            if self.type == "left":
                self.x += 1
            elif self.type == "right":
                self.x -= 1
            elif self.type == "rot":
                self.rot_kind -= 1
            else:
                self.y -= 1
                self.turn_end_point = True
            self.makeTetrimino()
            self.setArray()
        self.type = "down"
        

    def saveArray(self):
        self.save_stage_array = self.stage_array.copy()
        self.save_block_color_array = self.block_color_array.copy()


    def setBlock(self):
        self.canvas.delete("id")

        if self.turn_end_point:
            tag_name = "ovg"
        else:
            tag_name = "id"
        for k in range(self.tetri_mino.shape[0]):
            self.canvas.create_rectangle(self.tetri_mino[k][0]*self.block_size, self.tetri_mino[k][1]*self.block_size, \
                (self.tetri_mino[k][0]+1)*self.block_size, (self.tetri_mino[k][1]+1)*self.block_size, \
                    fill=self.block_color, tag=tag_name)


    def judgeline(self):
        line_call = False
        for k in range(self.stage_array.shape[0]):
            if np.all(self.stage_array[k] == 1):
                line_call = True
                self.changeLine(k)
                self.line_point = np.append(self.line_point, k).astype("int64")
        if line_call:
            self.delLineblack()
        self.canvas.delete("ovg")
        for i in range(self.stage_array.shape[1]):
            for j in range(self.stage_array.shape[0]):
                if self.stage_array[j][i] == 1:
                    self.canvas.create_rectangle(i*25, j*25, (i+1)*25, (j+1)*25, fill=self.block_color_array[j][i], tag="ovg")
        self.saveArray()

    
    def delLineblack(self):
        #color1 = "black"
        color =  "black"
        for j in self.line_point:
            for i in range(self.stage_width):
                self.canvas.create_rectangle(i*25, j*25, (i+1)*25, (j+1)*25, fill=color, tag="del")
        # ws.Beep(770, 50)
        
        if self.change_check == 4:
            self.canvas.delete("del")
            self.change_check = 0
            self.line_point = np.array([])
        else:
            self.master.after(30, self.delLineWhite)


    def delLineWhite(self):
        color =  "white"
        for j in self.line_point:
            for i in range(self.stage_width):
                self.canvas.create_rectangle(i*25, j*25, (i+1)*25, (j+1)*25, fill=color, tag="del")
        # ws.Beep(200, 40)
        self.change_check += 1
        self.master.after(30, self.delLineblack)

        
    def changeLine(self, k):
        temp_stage_array = np.delete(self.stage_array, k, 0)
        temp_color_array = np.delete(self.block_color_array, k, 0)
        zeros_stage_array = np.zeros(self.stage_width).reshape(1, self.stage_width)
        zeros_color_array = np.where(np.zeros((1, self.stage_width))==0, "gray95", "None") 
        self.stage_array = np.append(zeros_stage_array, temp_stage_array, axis=0)
        self.block_color_array = np.append(zeros_color_array, temp_color_array, axis=0)


    def judgeGameOver(self):
        for i in range(4):
            for j in range(self.stage_width):
                if self.stage_array[i][j] == 2:
                    self.master.after_cancel(self.nextid)
                    self.game_continue = 1
                    break
            else:
                continue
            break

    
    def judgeNextTurn(self):
        if self.turn_end_point:
            self.saveArray()
            self.judgeline()
            self.x = 4
            self.y = 0
            self.turn_end_point = False
            self.shaffle_True = True
            self.rot_kind = 0
            self.addBlockKind()
        else:
            self.y += 1
        self.btn_ok = True
        self.nextid = self.master.after(250, self.oneGame)


    def oneGame(self):
        self.makeTetrimino()
        self.makeNextBlock()
        self.judgeBoundary()
        self.setArray()
        self.judgeGameOver()
        if self.game_continue == 0:
            self.judgementTwo()
            self.setBlock()
            self.judgeNextTurn()
        else:
            self.judgementTwo()
            self.setBlock()
            self.reStartButton()
            self.endGame()


    def reStartButton(self):
        font_rs = font.Font(family='Helvetica', size=30, weight='bold')
        self.rs_btn = tk.Button(self.master, text="restart", font=font_rs, command=self.reStart)
        self.rs_btn.place(x=230, y=350)


    def endGame(self):
        font1 = font.Font(family='Helvetica', size=50, weight='bold')
        self.label = tk.Label(self.master, text="GAME OVER", fg="red", bg="black", font=font1)
        self.label.place(x=100, y=240)
        # ws.Beep(600, 50)
        self.endid = self.after(300, self.delText)

    
    def delText(self):   
        self.label.place_forget()
        # ws.Beep(200, 50)
        self.endid = self.after(300, self.endGame)

    
    def reStart(self):
        self.after_cancel(self.endid)
        self.unkeyInput()
        self.gameClear()

    
    def gameClear(self):
        pass




def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()