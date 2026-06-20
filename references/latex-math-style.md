# Reference: LaTeX 数学公式风格

## 目标

让数学公式排版符合 lailai 习惯。提炼自站点 `docs/project/guides/text.mdx`（LaTeX 章节）与 `docs/project/guides/latex.mdx`。

## 适用场景

- 任何含数学公式的内容（文章、笔记、题解、聊天）。
- 审查公式写法是否符合 lailai 习惯。

## 核心规则

### 分隔符与位置

1. **统一用 `$...$`（行内）与 `$$...$$`（行间）**，所有场景一致，不用 `\(...\)` / `\[...\]`。
2. 行间公式前后各 `$$` **单独成行**。
3. 数学公式**不放在**标题、加粗、斜体、链接等格式里。
4. 行内公式避免多余空格；**反斜杠命令后接数字时加空格**（`\sin 2\alpha`，不是 `\sin2\alpha`）。
   - **不手动调间距**：禁用一切显式间距命令 `\,` `\;` `\:` `\!` `\quad` `\qquad` `\ `（连写空格），交给 KaTeX 默认排版。括号紧贴内容：写 `c(f_{i,j})`，不写 `c(\,f_{i,\,j}\,)`。（注：上一条「命令后接数字加空格」用的是普通空格，不是这类间距命令。）

### 用数学语言，而非代码语言

5. 赋值用 `\to` 或 `\gets`，不用 `=`。
6. 取模用 `\bmod` 或 `\pmod`，不用 `%` 或 `\mod`。
7. 数列用 `a_i`，不用 `a[i]`。
8. 向下取整 `\lfloor\rfloor`，向上取整 `\lceil\rceil`。
9. 位运算用 `\operatorname{and}` / `\operatorname{or}` / `\operatorname{xor}`。
10. 文本用 `\text`，字符串用 `\texttt`。
11. 未定义但约定俗成的函数用 `\operatorname`（如 `\operatorname{lca}`、`\operatorname{lcm}`）。

### 符号选择（用左、不用右）

12. **`\frac`** ← `\dfrac`。
13. 乘法 **`\times`** 或 **`\cdot`** ← `*`。
14. 绝对值 **`||`** ← `\lvert\rvert`。
15. 角度 **`\circ`** ← `\degree`。
16. 横向省略号 **`\dots`** ← `\cdots` / `\ldots`；纵向 `\vdots`；斜向 `\ddots`。
17. 空集 **`\varnothing`** ← `\emptyset`。
18. 逻辑用 `\implies` / `\impliedby` / `\iff`。

### 格式细节

19. 变量名用**单个字母**加上下标，不用多字母（`a_i`，不是 `idx`）。
20. 物理单位用 `\mathrm`（`\mathrm{m/s^2}`）；罗马微分 `\mathrm{d}x`。
21. 特殊数集用 `\mathbb`（`\mathbb{R}`）。
22. 包裹大高度公式的括号用 `\left \right`。
23. 复杂度用大 $O$ 记号，**不带常数**（`$O(n\log n)$`，不是 `$O(2n\log n)$`）。
24. 大数字用科学计数法。
25. 多步推导用 `\begin{aligned}`；分段用 `\begin{cases}`；矩阵用 `\begin{bmatrix}`。
26. 数字默认纯文本，`$...$` 只给真数学。散文里的年份 / 日期 / 分数 / 计数 / 百分比 / 度量是纯文本（`616 分`、`2 月 26 日`、`95%`、`17 km`、`20 世纪`）；只有作为公式 / 关系 / 变量 / 下标 / 运算符操作数的数才包（`$2^{10}=1024$`、`$3:1$`、`$\mu\pm 3\sigma$`、`$X\sim N(\mu,\sigma^2)$`）。
27. 范围：数学内用 `\sim`（`$1\sim n$`）；其余一律 en dash `–`（紧贴无空格，操作数含空格时才留空），任何地方不用波浪号字符（`～`/`〜`/`~`）表范围。

## 示例

```latex
设 $S_k=\sum_{i=1}^{k}a_i$，则区间 $[l,r]$ 的和为 $S_r-S_{l-1}$。

$$
\begin{aligned}
f(x) &= a \\
&= b
\end{aligned}
$$
```

## Self-review Checklist

- [ ] 用 `$...$` / `$$...$$`，行间 `$$` 单独成行，公式不在标题 / 加粗里？
- [ ] 用数学语言（`\to` 赋值、`\bmod` 取模、`a_i` 而非 `a[i]`、`\lfloor\rfloor`）？
- [ ] 符号选对（`\frac` 非 `\dfrac`、`\dots` 非 `\cdots`、`\varnothing` 非 `\emptyset`、`\times` 非 `*`）？
- [ ] 变量单字母、复杂度大 $O$ 不带常数、单位 `\mathrm`、数集 `\mathbb`？
- [ ] 反斜杠命令后接数字加了空格？没用 `\,` `\;` `\quad` 等手动间距命令？
- [ ] 散文数字是纯文本、`$...$` 只给真数学？范围数学内 `\sim`、其余 en dash `–`、无波浪号？
