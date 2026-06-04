#include <bits/stdc++.h>
using namespace std;

using ll=long long;
const int N=200005;
int a[N];
ll s[N];

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int n,q;
	cin>>n>>q;
	for(int i=1;i<=n;i++)
	{
		cin>>a[i];
		s[i]=s[i-1]+a[i];
	}
	while(q--)
	{
		int l,r;
		cin>>l>>r;
		cout<<s[r]-s[l-1]<<'\n';
	}
	return 0;
}
