# Reference: OI / 算法竞赛 C++ 风格

## 目标

写出符合 lailai's Code Style 的竞赛 C++ 代码。提炼自站点 `docs/project/guides/code.mdx`（lailai 自己的《代码风格指南》，参考 Google C++ Style、Menci、Baoshuo 的 OI 风格）。

## 适用场景

- 写 OI / 算法竞赛题解代码。
- 审查竞赛 C++ 是否符合 lailai 风格。

> 仅适用于**算法竞赛中的 C++**，不是工程代码风格。工程 TS / React 走 Prettier（见 [project-docs-style.md](project-docs-style.md)）。

## 通用

1. **C++17**，避免不兼容特性。改风格不改逻辑。
2. UTF-8；扩展名 `.cpp`（不用 `.cc` / `.cxx`）。
3. **1 个 Tab 缩进**，空行不缩进。文件以 1 个空行结尾，不连续用 2 个空行。

## 结构

4. **简洁**：不写注释、调试代码、防御性编程；不加多余空格；只定义必要的常量和变量。**简洁是审美，不是顺带**——写完主动再抠一层：能不能再省一个变量、降一档复杂度、去掉一对括号或一个判断；该问"能不能 $O(n)$"就去抠。多份题解可融合取各家最优，极致处优雅压可读性（但不靠牺牲正确）。
5. **大括号**单独成行。**唯一能省大括号的情形是完全内联同一行**（`for(...)if(...)return 0;`、`if(n%i==0)return 0;`）；只要换行、或内层语句已带大括号（如嵌套循环外层），外层就**必须加大括号**——不允许「换行 + 省略大括号」，嵌套循环外层也不例外。

   ```cpp
   for(int i=1;i<=n;i++)
   {
       /* code */
   }
   if(x<=l&&r<=y){gx(u,v,r-l+1);return;}
   if(n%i==0)return 0;
   for(int x=l;x<=r;x++)if(a[x])return 0;
   ```

6. **头文件**用万能头 `#include <bits/stdc++.h>`（`#include` 与头文件间 1 个空格），特殊需求再补。
7. **命名空间**用 `using namespace std;`，特殊需求再补（如 `__gnu_pbds`）。
8. 宏定义按需用（`#define ls (u<<1)` / `mid (l+r>>1)`）。

## 主体

9. **主函数放末尾**，返回 `int`，以 `return 0;` 结束。
10. 文件读写用 `freopen`；数据量大时加快读：`ios::sync_with_stdio(false); cin.tie(nullptr);`。
11. 读写默认用 `cin` / `cout`，避免 `scanf` / `printf`；按需 `getline`。**唯一该用 `scanf` / `printf` 的情形是输入带固定格式分隔符、非它不可**（如 `scanf("%d:%d:%d %d:%d:%d",&h1,&m1,&s1,&h2,&m2,&s2);` 读时间）。**精度输出一律 `cout<<fixed<<setprecision(k)`，绝不用 `printf("%.3f")`。** 且**同一份代码不混用**：要么全程 `cin` / `cout`，要么全程 `scanf` / `printf`，不一半一半。
12. **单字符字面量一律用单引号** `'x'`（非 `"x"`）——输出 `cout<<'x'`、字符串拼接 `s+'('+...`（不写 `s+"("`）都算，作字符不作字符串；换行**永远是独立的** `<<'\n'`，**字符串字面量里绝不夹 `\n`**——`cout<<"No solution."<<'\n';`，不写 `cout<<"No solution.\n";`（也不用 `"\n"` / `endl`）；**例外：交互题需要即时刷新缓冲区时可用 `endl`**（它同时换行 + flush，正好满足交互的刷新需求）。忽略行尾空格和末尾多余换行。
13. 自增自减用后置（`x++`）；`sizeof` 后通常不加括号（`sizeof x`）。

## 类型

14. 用合适类型：能 `int` 不 `long long`，能 `bool` 不 `int`。
15. 长类型名用 `using` 定义别名（不用宏）：`using ll=long long;`、`using pii=pair<int,int>;`。
16. `const` 定义常量（不用宏）；**避免 `static` / `register` / `inline`**。
17. 小型变量定义在局部作用域，避免全局；**大型数组用全局**。避免频繁临时变量。
18. **普通静态数组 `int a[N]` 优先**（与 `lailai0916.github.io` 的题解代码一致）。`vector` 只在确实优雅处用——典型是邻接表存图 `vector<int> G[N]`，遍历 `for(auto v:G[u])dfs(v);`。**整段全是 `vector` 是 AI-tell，避免。**
19. **`auto` 受欢迎**：用来省去冗长类型（尤其迭代器、range-based for），不手写一长串迭代器类型。

## 命名

20. **snake_case**。小型变量简洁，通常 ≤ 3 字符；语义用**英文单词的辅音字母**，不用拼音。
21. 常量：数据规模 `N` / `M` / `K`（值 = 题目最大规模 $+5$）；模数 `mod`；无穷大 `inf=0x3f3f3f3f`（便于 `memset`）；无穷小 `eps`；`pi=acos(-1)`、`e=exp(1)`、`phi=(sqrt(5)+1)/2`。
22. 变量：多组数据 `T`，输出组号用 `_`；规模 `n`，操作次数 `m` / `q`，操作种类 `op`；循环变量 `i` / `j` / `k`。**循环计数器一律 `i` / `j` / `k`，即使它带语义角色**（周期、断点、枚举的因子等）**也不另起语义名**（别因为「是周期」就写 `p`）；语义名留给非计数器的量。**同一层的兄弟循环复用同名计数器**（两个并列的第三层循环都用 `k`，不一个 `k` 一个 `p`），保持一致。
23. 常用名：`ans`（答案）`cnt`（计数）`cur`（当前）`dep`（深度）`dis`（距离）`fa`（父）`len`（长）`mn` / `mx`（最值）`pos`（位置）`res`（返回）`rt`（根）`siz`（大小）`son`（子）`sum`（和）`tag`（标记）`tmp`（临时）`val`（价值）`vis`（访问）。比较函数（`sort` 的 comparator）惯用 `cmp`，别自造名（如 `better`）。
24. **DP 数组用 `f`**：`f[N]` / `f[N][N]`，**不用 `dp`**；题解里数学符号同样 `$f_{i,j}$`，不用 `$dp$`（站内 109 篇题解 `dp[` 出现 $0$ 次）。

## 常用写法与调试（语料校准）

- **同类型定义合并一行**：`string s,f[N][N];`、`int n,m,a[N];`。变量多则**标量一行、数组一行**分开（标量归标量、数组归数组），不混排。相邻、相同类型的多个定义也要合并（`vector<int> cv,mL,ms;`，不拆成三行）。
- **引用 / 指针符号贴变量名、留前空格**：`Type &x`（`auto &f`、`const string &a`、`int &v=T[u][c]`），不写 `auto&f`；范围 for 取引用同理 `for(auto &v:G[u])`。
- **`.size()` 不转 `int`**：一般直接用 `v.size()`（如 `for(int i=0;i<v.size();i++)`、`int n=s.size();`），不写 `(int)v.size()`；需要参与有符号运算时先存进 `int` 变量，别就地强转。
- **常用算法严格用站内个人模板，不自创**：快速幂、乘法逆元、存图、并查集、线段树等一律照 `docs/contest/personal/common-templates.mdx`（lailai《常用模板》）的写法与命名。典型：快速幂 `ll Pow(ll x,ll y)`（先 `x%=mod;`）；线性逆元 `inv[i]=i==1?1:(mod-mod/i)*inv[mod%i]%mod;`；存图 `vector<int> G[N]`（大写 `G`，配规则 18）。别自己另起 `qpow` / `e[]` 之类的命名或实现。
- **bool 值用 `0`/`1`**：不写 `false`/`true`（`return 0;` 不写 `return false;`）；唯一例外是固定惯用写法 `ios::sync_with_stdio(false)`。
- **简单二选一 return 用三目**：`if(c)return a; return b;` 合并为 `return c?a:b;`（规则 4「再抠一层」的落地）；复杂逻辑别硬塞三目伤可读。
- **操作分发用完整 `else if` 链**：按操作类型 `op` 分支时，每个分支都写明判定，**哪怕只剩最后一种也写 `else if(op==k)`，不收尾成裸 `else`**——`if(op==1)…else if(op==2)…`、`if(op==0)…else if(op==1)…else if(op==2)…else if(op==3)…`。让每条分支与它处理的 `op` 一一对应、可读可改。（裸 `else` 只用于真正的「其余一切」语义，不用于「就差这一种」。）
- **一行一条语句**：不把两条**不同**的语句挤一行。`int u,v;ll w;` 必须拆成 `int u,v;` 和 `ll w;` 两行（不同类型是两条声明）；唯一允许同一行的是**完全对称、同构**的并列操作 `x1++;y1++;`。注意这与「同类型定义合并」不冲突：`int u,v;`（一条声明里多变量）合并，`int u,v;` + `ll w;`（两条声明）分行。
- **不为一次性逻辑造中间变量**：只用来「接住」`++cnt` 的临时变量删掉，直接用 `cnt`。写 `++tot; len[tot]=…; ch[p][c]=tot;`，不写 `int cur=++tot; len[cur]=…; ch[p][c]=cur;`（规则 4 简洁、规则 17 避免临时变量的落地）。
- **辅助函数按复用次数决定**：同一段逻辑用到 $\ge2$ 次才抽成 helper（如周期判定 `period`、位数 `dig`）；**只用一次**的短逻辑直接内联，不为一次性逻辑造函数（规则 4 简洁）。重构后复用次数变了就跟着调：变 $1$ 次内联、变 $2$ 次抽出。
- **二分用左闭右开**：`int l=x,r=y+1; while(l<r){int mid=l+r>>1; if(check(mid))r=mid; else l=mid+1;}`，返回 `l`；区间记法统一左闭右开。
- **改代码点对点**：定位 bug 时只指最核心错误、给最小修改，不重写、不贴完整代码、不动调试与冗余部分。
- **高尔夫是另一套标准**：打码高尔夫为压字节可上逗号运算符返回值、三目短路等奇技；只用于高尔夫，**不带进正式题解**——题解仍按上面的优雅简洁来。

## 模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll=long long;
const int N=100005;
int a[N];
int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int n;
	cin>>n;
	for(int i=1;i<=n;i++)cin>>a[i];
	ll sum=0;
	for(int i=1;i<=n;i++)sum+=a[i];
	cout<<sum<<'\n';
	return 0;
}
```

## Self-review Checklist

- [ ] C++17，`<bits/stdc++.h>`，`using namespace std;`？
- [ ] 1 Tab 缩进，大括号单独成行，简短语句内联？
- [ ] 无注释、无防御性编程、无多余空格？
- [ ] `cin` / `cout` + 快读，`'\n'` 换行，单引号字符？
- [ ] 能 `int` 不 `long long`；`using` 别名；`const` 常量；无 `static` / `register` / `inline`？
- [ ] 普通数组 `int a[N]` 优先（`vector` 仅存图等，无"全是 vector"的 AI-tell）；`auto` 省冗长类型；大数组全局、小变量局部？
- [ ] snake_case，小变量 ≤ 3 字符，按命名表（`N`+5、`inf=0x3f3f3f3f`、`ans` / `cnt` / `siz`…）？
- [ ] 主函数在末尾，`return 0;`？
