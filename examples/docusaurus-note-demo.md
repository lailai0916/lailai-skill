# Example: Docusaurus 题解 / 笔记

展示站内 MDX 题解的标准形态。数学统一用 `$...$` / `$$...$$`。

## 输入

为一道"求 $1$ 到 $n$ 区间和"的入门题写一篇站内题解（虚构 PID `P0001`）。

## 处理原则

- 严格走题解模板（[docusaurus-style.md](../references/docusaurus-style.md)）。
- 数学用 `$...$`，数量包进数学。
- 思路段以复杂度收尾，无"总结"。
- 代码遵循 lailai's Code Style（[cpp-oi-style.md](../references/cpp-oi-style.md)）。

## 输出

```mdx
---
title: 题解：P0001 区间求和
tags: [oi, solution, luogu]
---

<Solution pid="P0001" lid="1" />

{/* truncate */}

## 题意简述

给定 $n$，求 $\sum_{i=1}^{n} i$。

## 解题思路

直接套等差数列求和：$\sum_{i=1}^{n} i = \dfrac{n(n+1)}{2}$。

注意 $n$ 较大时乘积会爆 `int`，用 `long long`。时间复杂度为 $O(1)$。

## 参考代码

\`\`\`cpp
#include <bits/stdc++.h>
using namespace std;

using ll=long long;
int main()
{
ios::sync_with_stdio(false);
cin.tie(nullptr);
ll n;
cin>>n;
cout<<n\*(n+1)/2<<'\n';
return 0;
}
\`\`\`
```

## 为什么符合 lailai.skill

- frontmatter 顺序、`tags: [oi, solution, luogu]`、`<Solution>` + `{/* truncate */}` 全合规。
- 站内数学用 `$...$`；`$n$`、`$\sum$` 都包进数学。
- 思路段以"时间复杂度为 $O(1)$。"收尾，没有"总结 / 希望帮到你"。
- 代码：`bits/stdc++.h`、Tab、Allman、无注释、`cin/cout`、`'\n'`、`return 0;`。
