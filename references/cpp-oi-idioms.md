# Reference: OI C++ 个人算法惯用实现

## 目标

题解代码不仅要符合通用排版，还要像 lailai 过去的代码。已有固定写法时，功能等价但
命名、接口、语句顺序或拆分方式不同的实现仍不合格。

## 使用规则

1. 写代码前识别其中的标准组件，优先复用本文件的固定实现。
2. 只按题目需要调整类型、数组界、模数、返回信息与必要扩展；未受影响的核心逐句保留。
3. 只使用一次的外围逻辑仍按 `cpp-oi-style.md` 内联；不要为了套模板引入无用接口。
4. 本文件未收录的算法按历史命名表与通用风格实现。不得从参考题解继承变量组或函数拆分。
5. 新实现反复稳定出现后，再经维护流程收录。一次生成的写法不能自行升级为个人模板。

## 未收录组件

未收录的组件也不能随意选一套常见模板。先检查本 Skill 已有命名和相邻组件；维护本
Skill 时，还应对照多份 lailai 第一方历史代码。若多份代码存在稳定共同实现，就把它
记录为观察，并在 lailai 确认后收录。若历史写法不一致，则选择与当前题目语义最接近的
版本，不能拼接成历史中不存在的混合模板。

第一方历史代码只能用于提取 lailai 本人的惯用法。题目特有的推导、变量组、函数边界与
控制流程仍须独立设计，不能借个人风格之名复制第三方题解。

## 快速幂

```cpp
ll Pow(ll x,ll y)
{
	x%=mod;
	ll res=1;
	while(y)
	{
		if(y&1)res=res*x%mod;
		x=x*x%mod;
		y>>=1;
	}
	return res;
}
```

模数是参数时只增加 `ll mod`，并保持 `Pow`、`res` 与循环主体不变；不要改成 `qpow`、
`quick_pow` 或递归版本。

## 扩展欧几里得

```cpp
tuple<ll,ll,ll> exgcd(ll a,ll b)
{
	if(!b)return {a,1,0};
	auto [g,x,y]=exgcd(b,a%b);
	return {g,y,x-a/b*y};
}
```

调用处使用 `auto [g,x,y]=exgcd(a,b);`。确实需要原地改写引用参数时才换引用版本，不能
仅因参考代码使用引用就改变个人惯用接口。

## 并查集

最小核心如下：

```cpp
int fa[N];
int find(int u){return u==fa[u]?u:fa[u]=find(fa[u]);}
```

按实际复用需要选用下列接口，不需要就不保留：

```cpp
void init(int n){for(int i=1;i<=n;i++)fa[i]=i;}
void merge(int u,int v){fa[find(u)]=find(v);}
bool query(int u,int v){return find(u)==find(v);}
```

普通并查集使用 `fa`、`find`、`merge`、`query`，不改成 `parent`、`root`、`unite`。带权、
可撤销或按秩合并等变体只增加其必要状态。

## 树状数组

```cpp
struct BIT
{
	int c[N];
	void add(int u,int v){while(u<N){c[u]+=v;u+=u&-u;}}
	int sum(int u){int res=0;while(u){res+=c[u];u-=u&-u;}return res;}
};
```

值域需要时把 `c`、`v`、`res` 同步改为 `ll`。二维、区间修改等变体沿用 `BIT`、`c`、
`add`、`sum` 与 `u&-u` 的核心命名。

## 其它稳定表面

| 组件 | 固定表面 |
| :-- | :-- |
| 线性逆元 | `inv[i]=i==1?1:(mod-mod/i)*inv[mod%i]%mod;` |
| 组合数 | `inv`、`fac`、`jv`，函数 `init`、`C`、`A` |
| 欧拉筛 | `sieve`、`vis`、`pri`、`cnt` |
| KMP | `kmp(string s,string t)` 与 `nxt` |
| 图的邻接表 | `vector<int> G[N]`；二字段加权边优先 `vector<pair<int,int>> G[N]` |
| ST 表 | `struct ST`，成员 `a`，接口 `init`、`query` |
| 线段树 | `struct SEG`，成员 `val`、`tag`，接口 `gx`、`push_up`、`push_down`、`build`、`update`、`query` |
| 树链剖分 | `G`、`fa`、`son`、`siz`、`dep`、`top`、`dfn`、`rnk`、`out`，函数 `dfs1`、`dfs2`、`lca` |

这些名称不是建议。题目只用到组件的一部分时删除无用部分，不另造同义接口。

## Self-review Checklist

- [ ] 识别并复用了所有已收录的标准组件？
- [ ] 函数名、变量名、接口和核心语句顺序与固定实现一致？
- [ ] 改动仅来自题目语义，并保留了未受影响的核心？
- [ ] 未从已有题解继承其私有符号、变量组或函数拆分？
- [ ] 未为只使用一次的逻辑保留无用模板接口？
