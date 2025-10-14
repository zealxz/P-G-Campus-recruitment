import tkinter as tk
from tkinter import ttk
import itertools


class ExpressionFinder:
    def __init__(self):
        # 预计算所有可能的表达式和结果
        self.expressions_dict = self.precompute_expressions()

    def precompute_expressions(self):
        """预计算所有可能的表达式和结果，每种类型只保留一个解法"""
        expressions_dict = {}
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # 生成所有3个不同数字的排列
        for a, b, c in itertools.permutations(digits, 3):
            # 计算所有可能的3个数字的表达式
            expressions = [
                (f"{a}+{b}+{c}", a + b + c, "a+b+c"),
                (f"{a}+{b}-{c}", a + b - c, "a+b-c"),
                (f"{a}*{b}+{c}", a * b + c, "a*b+c"),
                (f"{a}*{b}-{c}", a * b - c, "a*b-c"),
                (f"{a}*{b}*{c}", a * b * c, "a*b*c")
            ]

            # 将表达式添加到字典中，每种类型只保留一个
            for expr, result, expr_type in expressions:
                if result not in expressions_dict:
                    expressions_dict[result] = {}
                if expr_type not in expressions_dict[result]:
                    expressions_dict[result][expr_type] = expr

        # 生成所有4个不同数字的排列
        for a, b, c, d in itertools.permutations(digits, 4):
            # 计算所有可能的4个数字的表达式
            expressions = [
                (f"{a}+{b}+{c}+{d}", a + b + c + d, "a+b+c+d"),
                (f"{a}+{b}+{c}-{d}", a + b + c - d, "a+b+c-d"),
                (f"{a}*{b}+{c}+{d}", a * b + c + d, "a*b+c+d"),
                (f"{a}*{b}+{c}-{d}", a * b + c - d, "a*b+c-d"),
                (f"{a}*{b}*{c}+{d}", a * b * c + d, "a*b*c+d"),
                (f"{a}*{b}*{c}-{d}", a * b * c - d, "a*b*c-d")
            ]

            # 将表达式添加到字典中，每种类型只保留一个
            for expr, result, expr_type in expressions:
                if result not in expressions_dict:
                    expressions_dict[result] = {}
                if expr_type not in expressions_dict[result]:
                    expressions_dict[result][expr_type] = expr

        return expressions_dict

    def find_expressions(self, target):
        """查找结果为指定值的表达式，每种类型只返回一个"""
        try:
            target_num = int(target)
            if target_num in self.expressions_dict:
                # 返回每种表达式类型的一个解法
                return list(self.expressions_dict[target_num].values())
            else:
                return []
        except ValueError:
            return []


class ExpressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("数字表达式查找工具")
        self.root.geometry("600x400")

        # 创建表达式查找器实例
        self.finder = ExpressionFinder()

        # 创建界面元素
        self.create_widgets()

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重，使界面可调整大小
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # 输入标签和输入框
        ttk.Label(main_frame, text="输入目标结果:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry = ttk.Entry(main_frame, width=20)
        self.entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        self.entry.bind('<Return>', lambda event: self.calculate())  # 绑定回车键

        # 计算按钮
        self.calc_button = ttk.Button(main_frame, text="查找表达式", command=self.calculate)
        self.calc_button.grid(row=0, column=2, padx=5, pady=5)

        # 结果显示框
        ttk.Label(main_frame, text="""
            1.在"输入目标结果"输入框中输入答案
            2.点击"查找表达式"
            3.获得对应算式
            --By 找不到工作的25应届生 v:zealxfk
            """).grid(row=1, column=0, sticky=tk.W, pady=5)

        # 创建文本框和滚动条
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.text_area = tk.Text(text_frame, width=60, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)

        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

    def calculate(self):
        """计算按钮的回调函数"""
        target = self.entry.get().strip()

        if not target:
            self.status_var.set("请输入目标结果")
            return

        self.text_area.delete(1.0, tk.END)
        self.status_var.set("查找中...")

        # 更新界面
        self.root.update()

        # 查找表达式
        expressions = self.finder.find_expressions(target)

        # 显示结果
        if expressions:
            self.text_area.insert(tk.END, f"找到 {len(expressions)} 种表达式类型的结果为 {target}:\n\n")
            for i, expr in enumerate(expressions, 1):
                self.text_area.insert(tk.END, f"{i}. {expr} = {target}\n")
            self.status_var.set(f"找到 {len(expressions)} 种表达式类型")
        else:
            self.text_area.insert(tk.END, f"没有找到结果为 {target} 的表达式")
            self.status_var.set("未找到匹配的表达式")


# 创建主窗口并运行应用
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpressionApp(root)
    root.mainloop()