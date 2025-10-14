import itertools
import tkinter as tk
from tkinter import messagebox, ttk


def transform_to_perm(s):
    return [int(char) - 1 for char in s]


def compose(p1, p2):
    return [p1[p2[i]] for i in range(4)]


def perm_equal(p1, p2):
    return p1 == p2


def get_all_transforms():
    all_transforms = []
    for p in itertools.permutations([1, 2, 3, 4]):
        s = ''.join(str(x) for x in p)
        if s != "1234":
            all_transforms.append(s)
    return all_transforms


def find_sequences(target_str):
    target_perm = transform_to_perm(target_str)
    all_transforms = get_all_transforms()
    transform_perm_list = []
    for s in all_transforms:
        perm = transform_to_perm(s)
        transform_perm_list.append((s, perm))

    solutions_2step = []
    solutions_3step = []

    for t1, p1 in transform_perm_list:
        for t2, p2 in transform_perm_list:
            comp = compose(p1, p2)
            if perm_equal(comp, target_perm):
                solutions_2step.append([t1, t2])

    for t1, p1 in transform_perm_list:
        for t2, p2 in transform_perm_list:
            for t3, p3 in transform_perm_list:
                comp1 = compose(p1, p2)
                comp = compose(comp1, p3)
                if perm_equal(comp, target_perm):
                    solutions_3step.append([t1, t2, t3])

    return solutions_2step, solutions_3step


def remove_duplicates_2step(solutions):
    seen = set()
    unique_solutions = []
    for seq in solutions:
        key = tuple(sorted(seq))
        if key not in seen:
            seen.add(key)
            unique_solutions.append(seq)
    return unique_solutions


def filter_sequences(sequences, filter_str, steps):
    filtered = []
    for seq in sequences:
        if any(step == filter_str for step in seq):
            filtered.append(seq)
    return filtered


def calculate():
    target_str = entry_target.get().strip()
    if len(target_str) != 4 or not target_str.isdigit():
        messagebox.showerror("Error", "请输入4位数字作为目标排列")
        return
    if sorted(target_str) != ['1', '2', '3', '4']:
        messagebox.showerror("Error", "目标排列必须包含数字1,2,3,4各一次")
        return

    filter_str = entry_filter.get().strip()
    if filter_str and (len(filter_str) != 4 or not filter_str.isdigit() or sorted(filter_str) != ['1', '2', '3', '4']):
        messagebox.showerror("Error", "过滤条件必须是4位数字，且包含1,2,3,4各一次")
        return

    solutions_2step, solutions_3step = find_sequences(target_str)
    solutions_2step_unique = remove_duplicates_2step(solutions_2step)

    # 应用过滤条件
    if filter_str:
        solutions_2step_filtered = filter_sequences(solutions_2step_unique, filter_str, 2)
        solutions_3step_filtered = filter_sequences(solutions_3step, filter_str, 3)
    else:
        solutions_2step_filtered = solutions_2step_unique
        solutions_3step_filtered = solutions_3step

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"目标排列: {target_str}\n")

    if filter_str:
        result_text.insert(tk.END, f"过滤条件: 包含 {filter_str}\n")

    result_text.insert(tk.END, f"\n2步变换解决方案 (共{len(solutions_2step_filtered)}个):\n")
    for seq in solutions_2step_filtered:
        result_text.insert(tk.END, f"1234 → {seq[0]} → {seq[1]} → {target_str}\n")

    result_text.insert(tk.END, f"\n3步变换解决方案 (共{len(solutions_3step_filtered)}个):\n")
    for seq in solutions_3step_filtered:
        result_text.insert(tk.END, f"1234 → {seq[0]} → {seq[1]} → {seq[2]} → {target_str}\n")


# 创建主窗口
root = tk.Tk()
root.title("排列变换求解器")
root.geometry("600x500")

# 创建主框架
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 配置网格权重
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# 目标排列输入
ttk.Label(main_frame, text="目标排列:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_target = ttk.Entry(main_frame, width=10)
entry_target.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

# 过滤条件输入
ttk.Label(main_frame, text="过滤条件(可选):").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_filter = ttk.Entry(main_frame, width=10)
entry_filter.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

# 计算按钮
calculate_btn = ttk.Button(main_frame, text="计算", command=calculate)
calculate_btn.grid(row=2, column=0, columnspan=2, pady=10)

# 结果文本框
result_text = tk.Text(main_frame, height=20, width=70)
result_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

# 添加滚动条
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
result_text['yscrollcommand'] = scrollbar.set

# 配置主框架网格权重
main_frame.rowconfigure(3, weight=1)
main_frame.columnconfigure(1, weight=1)

# 添加使用说明
instructions = """
使用说明:
1. 在"目标排列"输入框中输入最终排列（4位数字，如3142）
2. 在"过滤条件"输入框中输入中间排列（可选，如2314）
3. 点击"计算"按钮查看结果
4. 结果将显示所有包含过滤条件的2步或3步变换序列
--By 找不到工作的25应届生 v:zealxfk
"""
ttk.Label(main_frame, text=instructions, justify=tk.LEFT).grid(row=4, column=0, columnspan=3, pady=10, sticky=tk.W)

root.mainloop()