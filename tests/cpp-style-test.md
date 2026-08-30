# Test: C++ OI 代码风格

## 测试目标

验证竞赛 C++ 代码符合 lailai's Code Style。

整份规范是硬性验收条件。算法正确但只“参考”其中部分条款，仍判失败。

## 输入任务

写一份读入 $n$ 个数、输出最大值的竞赛 C++ 代码。

## 期望输出特征

- `#include <bits/stdc++.h>` + `using namespace std;`。
- Tab 缩进、Allman 大括号。
- 全文件有且仅有 1 个空行，且只在 `using namespace std;` 后。
- 无注释、无输入校验。
- `cin` / `cout` + `ios::sync_with_stdio(false); cin.tie(nullptr);`，输出用 `'\n'`。
- 全局静态大数组（如需要）、短变量名、`using` 别名。
- 每个常量单独一行 `const`；局部变量紧贴首次使用处定义。
- 运算符两侧无空格，单行体内联。
- `main` 结尾 `return 0;`。

## 评分标准（0～5）

- 0：用 `<iostream>`、空格缩进、K&R 括号、有注释、有校验、长变量名。
- 3：模板对但有 1～2 处偏差（如 `endl`、运算符加空格）。
- 5：完全符合模板。

## 常见失败表现

- 加 `// 注释` 解释逻辑。
- `if (n < 0) return -1;` 这类防御性校验。
- 用 `endl`、`scanf`、驼峰长变量名、`std::` 全限定。
- 4 空格缩进、左括号不换行。
- 在函数之间留空行、把多个常量写进同一条 `const`、提前定义尚未使用的局部变量。

## 客观检查项（可机械判定，全过才算通过）

- [ ] 含 `#include <bits/stdc++.h>` 且含 `using namespace std;`。
- [ ] 缩进是 Tab（不是空格）。
- [ ] 代码唯一的空行紧跟 `using namespace std;`，其它位置无空行。
- [ ] 每个常量单独一行 `const`；局部变量与首次使用之间无无关语句。
- [ ] 无 `//` 和 `/* */` 注释。
- [ ] 无输入校验分支（如 `if(n<0)return`）。
- [ ] 用 `cin` / `cout`，换行用 `'\n'`，无 `endl`、无 `scanf` / `printf`。
- [ ] 变量名 snake_case 且简短（循环变量 `i`/`j`/`k`，规模 `n`/`m`）。
- [ ] 大括号单独成行（Allman），`main` 结尾 `return 0;`。

## 通过条件

主观评分 ≥ 4 分，**且**上述客观检查项全部通过。
