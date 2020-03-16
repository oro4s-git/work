"""ダンジョン探索ゲーム ver1（清書版）"""

import tkinter as tk
import csv
import random


class Model:

    HEIGHT =15
    WIDTH = 15
    CHARA_START_Y = 0
    CHARA_START_X = 0

    def __init__(self):
        # グリッドの定義
        self.grid = [[9]*Model.WIDTH for i in range(Model.HEIGHT)] # 初期化

        # csv で grid の下地を作成する
        #self.csvGrid()

        # 自動で grid を作成する
        self.newGridG2S()
        self.newGridDmy1()
        self.newGridDmy2()

        # キャラの位置定義
        self.chara = [Model.CHARA_START_Y,Model.CHARA_START_X] # Y軸, X軸

        # スタートとエンドを設定
        self.grid[self.chara[0]][self.chara[1]] = 1
        self.grid[Model.HEIGHT-1][Model.WIDTH-1] = 0

    def leftModel(self):
        if self.chara[1] > 0 and self.grid[self.chara[0]][self.chara[1]-1] != 9:
            self.grid[self.chara[0]][self.chara[1]] = 0
            self.chara[1] -= 1
            self.grid[self.chara[0]][self.chara[1]] = 1

    def rightModel(self):
        if self.chara[1] < Model.WIDTH-1 and self.grid[self.chara[0]][self.chara[1]+1] != 9:
            self.grid[self.chara[0]][self.chara[1]] = 0
            self.chara[1] += 1
            self.grid[self.chara[0]][self.chara[1]] = 1

    def upModel(self):
        if self.chara[0] > 0 and self.grid[self.chara[0]-1][self.chara[1]] != 9:
            self.grid[self.chara[0]][self.chara[1]] = 0
            self.chara[0] -= 1
            self.grid[self.chara[0]][self.chara[1]] = 1

    def downModel(self):
        if self.chara[0] < Model.HEIGHT-1 and self.grid[self.chara[0]+1][self.chara[1]] != 9:
            self.grid[self.chara[0]][self.chara[1]] = 0
            self.chara[0] += 1
            self.grid[self.chara[0]][self.chara[1]] = 1

    # csvファイルをもとに、gridを作成する
    def csvGrid(self):
        # csv ファイルから grid 情報を読み込む
        with open("data1.csv", "r", encoding="utf-8") as f:
            rd = csv.reader(f)
            i = 0
            for row in rd :
                j = 0
                for col in row:
                    self.grid[i][j] = int(col)
                    j+=1
                i+=1

    # 正規ルート作成
    def newGridG2S(self):
        # ゴールから走査
        chk_y = self.HEIGHT-1
        chk_x = self.WIDTH-1
        while True :
            r = random.randint(0, 1)

            if r>0 :
                chk_x = chk_x-1 if chk_x>0 else 0
            else :
                chk_y = chk_y-1 if chk_y>0 else 0
            self.grid[chk_y][chk_x] = 0

            #スタートにたどり着いたら終わり
            if chk_y == 0 and chk_x == 0 :
                break

    # ダミールート１
    def newGridDmy1(self):
        end_y2 = int((Model.HEIGHT/2)+random.randint(-2, 2))
        end_x2 = int((Model.WIDTH/2)+random.randint(-2, 2))
        end_y3 = int((Model.HEIGHT/2)+random.randint(-2, 2))
        end_x3 = int((Model.WIDTH/2)+random.randint(-2, 2))
        while True :
            ry2 = random.randint(0, 1)
            rx2 = random.randint(0, 1)
            ry3 = random.randint(0, 1)
            rx3 = random.randint(0, 1)

            # 斜めに作られるのを回避
            rx2 = 0 if (rx2+ry2==2) else rx2
            rx3 = 0 if (rx3+ry3==2) else rx3

            chk_y2 = end_y2 + ry2
            chk_x2 = end_x2 - rx2
            chk_y3 = end_y3 - ry3
            chk_x3 = end_x3 + rx3

            end_y2 = chk_y2 if chk_y2<=Model.HEIGHT-1 else end_y2
            end_x2 = chk_x2 if 0<=chk_x2 else end_x2
            end_y3 = chk_y3 if 0<=chk_y3 else end_y3
            end_x3 = chk_x3 if chk_x3<=Model.WIDTH-1 else end_x3

            self.grid[end_y2][end_x2] = 0
            self.grid[end_y3][end_x3] = 0

            # すべて隅にたどり着いたら終わり
            if ((end_y2 == Model.HEIGHT-1 and end_x2 == 0) and
                (end_y3 == 0 and end_x3 == Model.WIDTH-1)) :
                break

    # ダミールート２
    def newGridDmy2(self):
        for cnt in range(10) :
            ry = random.randint(0,Model.HEIGHT-1)
            rx = random.randint(0,Model.WIDTH-1)
            while True :
                if random.randint(0, 1) > 0 :
                    ry -= 1
                else :
                    rx -= 1

                if self.grid[ry][rx] == 0 :
                    break
                else :
                    ry = ry if ry>0 else 0
                    rx = rx if rx>0 else 0
                    self.grid[ry][rx] = 0


class View:

    def __init__(self, master, model, controller):
        self.master = master
        self.model = model
        self.controller = controller

        self.canvas = tk.Canvas(self.master, width=600, height=600, bg="black")
        self.canvas.pack()

        # grid の表示
        for i in range(Model.HEIGHT):
            for j in range(Model.WIDTH):
                x = 50+30*j
                y = 50+30*i
                if self.model.grid[i][j] == 1:
                    fill_ = "red"
                elif self.model.grid[i][j] == 9:
                    fill_ = "black"
                elif i == Model.HEIGHT-1 and j == Model.WIDTH-1 :
                    fill_ = "yellow"
                else :
                    fill_ = "white"

                self.canvas.create_rectangle(x,
                                        y,
                                        x+30,
                                        y+30,
                                        fill=fill_,
                                        outline="black",
                                        tag="map")

    def update(self):
        self.canvas.delete("map")

        if self.model.chara[0] == Model.HEIGHT-1 and self.model.chara[1] == Model.WIDTH-1 :
            self.canvas.create_text(280,
                                    300,
                                    text="GOAL!!",
                                    font=("Helverica", 100, "bold"),
                                    fill="yellow",
                                    tag="goal")

        else :
            for i in range(Model.HEIGHT):
                for j in range(Model.WIDTH):
                    x = 50+30*j
                    y = 50+30*i
                    if self.model.grid[i][j] == 1:
                        fill_ = "red"
                    elif self.model.grid[i][j] == 9:
                        fill_ = "black"
                    elif i == Model.HEIGHT-1 and j == Model.WIDTH-1 :
                        fill_ = "yellow"
                    else :
                        fill_ = "white"

                    self.canvas.create_rectangle(x,
                                            y,
                                            x+30,
                                            y+30,
                                            fill=fill_,
                                            outline="black",
                                            tag="map")


class Controller:

    def __init__(self, master, model):
        self.master = master
        self.model = model

        self.master.bind("<Left>", self.leftController)
        self.master.bind("<Right>", self.rightController)
        self.master.bind("<Down>", self.downController)
        self.master.bind("<Up>", self.upController)

    def leftController(self, event):
        self.model.leftModel()
        self.view.update()

    def rightController(self, event):
        self.model.rightModel()
        self.view.update()

    def downController(self, event):
        self.model.downModel()
        self.view.update()

    def upController(self, event):
        self.model.upModel()
        self.view.update()


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        master.geometry("550x600")
        master.title("Danjon")

        self.model = Model()
        self.controller = Controller(master, self.model)
        self.view = View(master, self.model, self.controller)

        self.controller.view = self.view


def main():
    win = tk.Tk()
    master = win
    app = Application(master)
    app.mainloop()

if __name__ == "__main__" :
    main()
