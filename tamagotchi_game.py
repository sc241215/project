import tkinter as tk
from tkinter import simpledialog

class TamagotchiGame:
    def __init__(self, master):
        self.master = master
        self.master.title("がんばるっち育成ゲーム")
        
        # 初期設定
        self.hunger = 0  # エサの必要度
        self.happiness = 100  # 機嫌
        self.growth = 0  # 成長段階（0:卵、1:子供、2:大人、3:進化後）
        self.age = 0  # 年齢（0歳からスタート）
        self.alive = True  # 生死状態
        self.in_game = False  # ゲーム中かどうか
        self.color = "yellow"  # 初期キャラクターの色

        # 操作説明画面を表示
        self.show_instructions()

    def show_instructions(self):
        """操作説明画面を表示"""
        self.instructions_frame = tk.Frame(self.master)
        self.instructions_frame.pack(pady=20)

        instructions = """操作説明:
        1. ごはん: "ごはん"ボタンを押してエサを選びます。
        2. お風呂: "お風呂"ボタンを押して「がんばるっち」をきれいにします。
        3. 遊ぶ: "遊ぶ"ボタンで「がんばるっち」の機嫌を良くします。
        4. 寝かせる: "寝かせる"ボタンで「がんばるっち」の機嫌を回復します。
        
        「がんばるっち」を育てて、元気に成長させましょう!
        """
        
        instructions_label = tk.Label(self.instructions_frame, text=instructions, font=('Arial', 14), justify="left")
        instructions_label.pack()

        # ゲーム開始ボタン
        start_button = tk.Button(self.instructions_frame, text="ゲーム開始", command=self.start_game)
        start_button.pack()

    def start_game(self):
        """ゲーム開始"""
        self.instructions_frame.pack_forget()  # 操作説明を非表示にする

        # キャラクターの色を選択する
        self.choose_color()

        # ゲームの初期設定
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="lightblue")
        self.canvas.pack()

        # たまごっち（がんばるっち）の顔（卵からスタート）
        self.face = self.create_face()

        # ステータス表示
        self.status_text = self.canvas.create_text(10, 10, anchor="nw", text=self.get_status(), font=('Arial', 12), fill="black")

        # 機嫌ゲージ表示
        self.happiness_bar = self.canvas.create_rectangle(10, 40, 210, 60, fill="green")
        
        # 選択肢ボタン（ごはん、お風呂、遊ぶ、寝る）
        self.food_button = tk.Button(self.master, text="ごはん", command=self.select_food)
        self.food_button.pack(side="left")

        self.bath_button = tk.Button(self.master, text="お風呂", command=self.bath)
        self.bath_button.pack(side="left")

        self.play_button = tk.Button(self.master, text="遊ぶ", command=self.play)
        self.play_button.pack(side="left")

        self.sleep_button = tk.Button(self.master, text="寝かせる", command=self.sleep)
        self.sleep_button.pack(side="left")

        # ゲーム開始
        self.in_game = True
        self.update_game()

    def choose_color(self):
        """キャラクターの色を日本語で選択する"""
        color = simpledialog.askstring("色を選ぶ", "キャラクターの色を選んでください (例: 赤, 青, 緑, 黄色):")
        if color:
            # 入力された色を小文字に変換して、色名をチェック
            color = color.strip().lower()
            if color == "赤" or color == "あか":
                self.color = "red"
            elif color == "青" or color == "あお":
                self.color = "blue"
            elif color == "緑" or color == "みどり":
                self.color = "green"
            elif color == "黄色" or color == "きいろ":
                self.color = "yellow"
            else:
                self.color = "yellow"  # 無効な入力の場合、デフォルトは黄色
        else:
            self.color = "yellow"  # 入力が無かった場合、黄色をデフォルトにする

    def create_face(self):
        """顔の描画 (シンプルな顔)"""
        # 顔の輪郭（シンプルな丸型）
        self.face = self.canvas.create_oval(120, 120, 280, 280, fill=self.color, outline="black")

        # 目（シンプルで可愛いデザイン）
        self.left_eye = self.canvas.create_oval(160, 170, 190, 200, fill="white")
        self.right_eye = self.canvas.create_oval(210, 170, 240, 200, fill="white")
        self.left_pupil = self.canvas.create_oval(170, 180, 180, 190, fill="black")
        self.right_pupil = self.canvas.create_oval(220, 180, 230, 190, fill="black")

        # 口（シンプルで可愛い口）
        self.mouth = self.canvas.create_arc(170, 220, 230, 260, start=0, extent=-180, style=tk.ARC)

        return self.face

    def update_game(self):
        """時間経過で「がんばるっち」の状態を更新"""
        if self.in_game:
            # 幸せが減っていく
            self.happiness -= 0.1
            self.hunger += 0.05
            self.age += 0.01

            # 不機嫌レベルが40以下でゲームオーバー
            if self.happiness <= 40:
                self.in_game = False
                self.canvas.itemconfig(self.status_text, text="がんばるっちが死んでしまいました...")
                self.canvas.create_text(200, 200, text="ゲームオーバー", font=('Arial', 24), fill="red")
                self.show_restart_button()  # 再挑戦ボタンを表示
                return  # ゲーム終了

            # 機嫌ゲージの更新
            self.canvas.coords(self.happiness_bar, 10, 40, 10 + self.happiness * 2, 60)
            self.canvas.itemconfig(self.happiness_bar, fill="green" if self.happiness > 60 else ("yellow" if self.happiness > 30 else "red"))

            # 「がんばるっち」が進化する
            if self.age > 1 and self.growth == 0:
                self.growth = 1
                self.canvas.itemconfig(self.status_text, text=self.get_status())
                self.canvas.coords(self.face, 100, 100, 300, 300)  # 子供の大きさに変更
                self.update_face(1)  # 子供の顔に変更
            elif self.age > 5 and self.growth == 1:
                self.growth = 2
                self.canvas.itemconfig(self.status_text, text=self.get_status())
                self.canvas.coords(self.face, 80, 80, 320, 320)  # 大人の大きさに変更
                self.update_face(2)  # 大人の顔に変更
            elif self.age > 10 and self.growth == 2:
                self.growth = 3
                self.canvas.itemconfig(self.status_text, text=self.get_status())
                self.canvas.coords(self.face, 60, 60, 340, 340)  # 最終形態
                self.update_face(3)  # 最終進化の顔に変更

            # 1秒ごとに更新
            self.master.after(1000, self.update_game)

    def update_face(self, growth_stage):
        """成長段階に応じて顔を変更"""
        if growth_stage == 1:
            # 子供の顔に変更（目が大きく、口は笑顔）
            self.canvas.coords(self.left_eye, 160, 170, 190, 200)
            self.canvas.coords(self.right_eye, 210, 170, 240, 200)
            self.canvas.itemconfig(self.mouth, start=0, extent=-180)  # 笑顔
        elif growth_stage == 2:
            # 大人の顔に変更（目が少し小さく、口が普通）
            self.canvas.coords(self.left_eye, 170, 180, 200, 210)
            self.canvas.coords(self.right_eye, 210, 180, 240, 210)
            self.canvas.itemconfig(self.mouth, start=0, extent=0)  # 普通の口
        elif growth_stage == 3:
            # 進化後の顔に変更（目が鋭く、口が挑戦的）
            self.canvas.coords(self.left_eye, 160, 170, 190, 200)
            self.canvas.coords(self.right_eye, 210, 170, 240, 200)
            self.canvas.itemconfig(self.mouth, start=0, extent=180)  # 挑戦的な口

    def select_food(self):
        """ごはん選択肢を表示"""
        self.food_frame = tk.Frame(self.master)
        self.food_frame.pack(pady=20)

        self.tomato_button = tk.Button(self.food_frame, text="トマト", command=lambda: self.feed("トマト"))
        self.tomato_button.pack(side="left")

        self.burger_button = tk.Button(self.food_frame, text="ハンバーガー", command=lambda: self.feed("ハンバーガー"))
        self.burger_button.pack(side="left")

        self.onigiri_button = tk.Button(self.food_frame, text="おにぎり", command=lambda: self.feed("おにぎり"))
        self.onigiri_button.pack(side="left")

    def feed(self, food):
        """エサを与える"""
        if self.in_game:
            if food == "トマト":
                self.happiness += 10
                self.hunger -= 20
                self.canvas.create_text(200, 350, text="トマトを食べた！", font=('Arial', 12), fill="green")
            elif food == "ハンバーガー":
                self.happiness += 15
                self.hunger -= 40
                self.canvas.create_text(200, 350, text="ハンバーガーを食べた！", font=('Arial', 12), fill="green")
            elif food == "おにぎり":
                self.happiness += 20
                self.hunger -= 30
                self.canvas.create_text(200, 350, text="おにぎりを食べた！", font=('Arial', 12), fill="green")

            self.canvas.itemconfig(self.status_text, text=self.get_status())
            self.show_eating_animation()

        # 食べ終わったらごはん選択肢を非表示にする
        self.food_frame.pack_forget()

    def show_eating_animation(self):
        """エサを食べているアニメーション"""
        self.canvas.itemconfig(self.face, fill="lightgreen")
        self.master.after(500, lambda: self.canvas.itemconfig(self.face, fill=self.color))

    def play(self):
        """遊ぶ"""
        if self.in_game:
            self.happiness = min(100, self.happiness + 20)
            self.canvas.itemconfig(self.status_text, text=self.get_status())

    def bath(self):
        """お風呂"""
        if self.in_game:
            self.happiness = min(100, self.happiness + 10)
            self.canvas.itemconfig(self.status_text, text=self.get_status())

    def sleep(self):
        """寝かせる"""
        if self.in_game:
            self.happiness = max(0, self.happiness - 10)
            self.hunger = min(100, self.hunger + 10)
            self.canvas.itemconfig(self.status_text, text=self.get_status())

    def get_status(self):
        """「がんばるっち」の状態をテキストとして返す"""
        return f"元気: {100 - self.hunger:.0f} 機嫌: {self.happiness:.0f} 年齢: {self.age:.1f} 成長: {self.growth}"

    def show_restart_button(self):
        """再挑戦ボタンを表示"""
        restart_button = tk.Button(self.master, text="再挑戦", command=self.restart_game)
        restart_button.pack(pady=20)

    def restart_game(self):
        """ゲームを再スタート"""
        # ゲームの状態をリセット
        self.hunger = 0
        self.happiness = 100
        self.growth = 0
        self.age = 0
        self.color = "yellow"
        self.in_game = False

        # ゲームのウィンドウを再初期化
        for widget in self.master.winfo_children():
            widget.destroy()

        self.start_game()

# ゲームを実行
root = tk.Tk()
game = TamagotchiGame(root)
root.mainloop()
