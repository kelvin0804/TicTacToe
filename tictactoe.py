import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe vs AI")
        
        # 玩家使用X，AI使用O
        self.HUMAN = "X"
        self.AI = "O"
        self.current_player = self.HUMAN
        
        # 创建游戏板
        self.board = {}
        self.buttons = {}
        
        # 创建3x3的按钮网格
        for i in range(3):
            for j in range(3):
                self.board[(i, j)] = ""
                self.buttons[(i, j)] = tk.Button(
                    self.window,
                    text="",
                    font=('Arial', 20),
                    width=5,
                    height=2,
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                self.buttons[(i, j)].grid(row=i, column=j)
        
        # 重新开始按钮
        restart_button = tk.Button(
            self.window,
            text="重新开始",
            font=('Arial', 12),
            command=self.restart_game
        )
        restart_button.grid(row=3, column=1)

    def button_click(self, row, col):
        # 人类玩家回合
        if self.board[(row, col)] == "" and self.current_player == self.HUMAN:
            self.make_move(row, col)
            
            if not (self.check_winner() or self.is_board_full()):
                # AI回合
                self.current_player = self.AI
                self.window.after(500, self.ai_move)  # 延迟500ms再行动

    def make_move(self, row, col):
        self.board[(row, col)] = self.current_player
        self.buttons[(row, col)].config(text=self.current_player)
        
        if self.check_winner():
            winner = "你" if self.current_player == self.HUMAN else "AI"
            messagebox.showinfo("游戏结束", f"{winner}获胜！")
            self.restart_game()
        elif self.is_board_full():
            messagebox.showinfo("游戏结束", "平局！")
            self.restart_game()
        else:
            self.current_player = self.AI if self.current_player == self.HUMAN else self.HUMAN

    def ai_move(self):
        move = self.get_best_move()
        if move:
            self.make_move(move[0], move[1])

    def get_best_move(self):
        # 1. 检查AI是否能赢
        for i in range(3):
            for j in range(3):
                if self.board[(i, j)] == "":
                    self.board[(i, j)] = self.AI
                    if self.check_winner():
                        self.board[(i, j)] = ""
                        return (i, j)
                    self.board[(i, j)] = ""

        # 2. 阻止玩家赢
        for i in range(3):
            for j in range(3):
                if self.board[(i, j)] == "":
                    self.board[(i, j)] = self.HUMAN
                    if self.check_winner():
                        self.board[(i, j)] = ""
                        return (i, j)
                    self.board[(i, j)] = ""

        # 3. 选择中心
        if self.board[(1, 1)] == "":
            return (1, 1)

        # 4. 选择角落
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if self.board[corner] == ""]
        if available_corners:
            return random.choice(available_corners)

        # 5. 选择边
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_edges = [edge for edge in edges if self.board[edge] == ""]
        if available_edges:
            return random.choice(available_edges)

        return None

    def check_winner(self):
        # 检查行
        for i in range(3):
            if self.board[(i, 0)] == self.board[(i, 1)] == self.board[(i, 2)] != "":
                return True
        
        # 检查列
        for j in range(3):
            if self.board[(0, j)] == self.board[(1, j)] == self.board[(2, j)] != "":
                return True
        
        # 检查对角线
        if self.board[(0, 0)] == self.board[(1, 1)] == self.board[(2, 2)] != "":
            return True
        if self.board[(0, 2)] == self.board[(1, 1)] == self.board[(2, 0)] != "":
            return True
        
        return False

    def is_board_full(self):
        return all(self.board[key] != "" for key in self.board)

    def restart_game(self):
        self.current_player = self.HUMAN
        for key in self.board:
            self.board[key] = ""
            self.buttons[key].config(text="")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run() 