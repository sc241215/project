import tkinter as tk

class TamagotchiGame:
    def __init__(self, master):
        self.master = master
        self.master.title("がんばるっち育成ゲーム")
        
        # 初期設定
        self.hunger = 0  # エサの必要度
        self.happiness = 100  # 機嫌
        self.growth = 0  # 成長段階（0:卵、1:子供、2:大人、3:進化後）
        self.age = 0  # 年齢
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
        1. エサを与える: "エサを与える"ボタンでお腹を満たします。
        2. 遊ぶ: "遊ぶ"ボタンで「がんばるっち」の機嫌を良くします。
        3. 寝かせる: "寝かせる"ボタンで「がんばるっち」の機嫌を回復します。
        
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

        # ゲームの初期設定
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="lightblue")
        self.canvas.pack()

        # キャラクターの色を選択する
        self.choose_color()

        # たまごっち（がんばるっち）の顔（卵からスタート）
        self.face = self.create_face()

        # ステータス表示
        self.status_text = self.canvas.create_text(10, 10, anchor="nw", text=self.get_status(), font=('Arial', 12), fill="black")

        # エサボタンの作成
        self.feed_bibimba_button = tk.Button(self.master, text="ビビンバを与える", command=lambda: self.feed("ビビンバ"))
        self.feed_bibimba_button.pack(side="left")

        self.feed_burger_button = tk.Button(self.master, text="ハンバーガーを与える", command=lambda: self.feed("ハンバーガー"))
        self.feed_burger_button.pack(side="left")

        self.feed_tomato_button = tk.Button(self.master, text="トマトを与える", command=lambda: self.feed("トマト"))
        self.feed_tomato_button.pack(side="left")

        # 遊ぶボタンと寝かせるボタン
        self.play_button = tk.Button(self.master, text="遊ぶ", command=self.play)
        self.play_button.pack(side="left")

        self.sleep_button = tk.Button(self.master, text="寝かせる", command=self.sleep)
        self.sleep_button.pack(side="left")

        # ゲーム開始
        self.in_game = True
        self.update_game()

    def choose_color(self):
        """キャラクターの色を選択する"""
        self.color = "yellow"  # キャラクターの色を「黄色」に設定（簡略化）

    def create_face(self):
        """顔の描画 (目、口、顔の輪郭を作成)"""
        # 顔の輪郭
        self.face = self.canvas.create_oval(120, 120, 280, 280, fill=self.color)

        # 目（初期状態）
        self.left_eye = self.canvas.create_oval(160, 170, 190, 200, fill="black")
        self.right_eye = self.canvas.create_oval(210, 170, 240, 200, fill="black")

        # 口（初期状態）
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
                return  # ゲーム終了

            # 幸せが100未満にならないように調整
            self.happiness = max(0, self.happiness)
            self.hunger = min(100, self.hunger)

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

    def feed(self, food):
        """エサを与える"""
        if self.in_game:
            if food == "ビビンバ":
                self.happiness += 20
                self.hunger -= 30
                self.canvas.create_text(200, 350, text="ビビンバを食べた！", font=('Arial', 12), fill="green")
            elif food == "ハンバーガー":
                self.happiness += 15
                self.hunger -= 40
                self.canvas.create_text(200, 350, text="ハンバーガーを食べた！", font=('Arial', 12), fill="green")
            elif food == "トマト":
                self.happiness += 10
                self.hunger -= 20
                self.canvas.create_text(200, 350, text="トマトを食べた！", font=('Arial', 12), fill="green")

            self.canvas.itemconfig(self.status_text, text=self.get_status())
            self.show_eating_animation()

    def show_eating_animation(self):
        """エサを食べているアニメーション"""
        self.canvas.itemconfig(self.face, fill="lightgreen")
        self.master.after(500, lambda: self.canvas.itemconfig(self.face, fill=self.color))

    def play(self):
        """遊ぶ"""
        if self.in_game:
            self.happiness = min(100, self.happiness + 20)
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

# ゲームを実行
root = tk.Tk()
game = TamagotchiGame(root)
root.mainloop()
