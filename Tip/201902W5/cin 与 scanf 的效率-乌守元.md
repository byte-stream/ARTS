在刷算法题时，遇到特别大的数据，总会 Time Out。包括但不仅限于 PAT、Leetcode。一般情况下，争对大量的数据，我们首先想到的方法是更快的读取方式，毕竟比优化算法要快。在 C++ 中常用的输入就是 std::cin 了，然而一般情况下，cin 是慢的。

而 cin 慢是有原因的，其实默认的时候，cin 与s tdin 总是保持同步的，也就是说这两种方法可以混用，而不必担心文件指针混乱，同时 cout 和 stdout 也一样，两者混用不会输出顺序错乱。正因为这个兼容性的特性，导致 cin 有许多额外的开销，如何禁用这个特性呢？只需一个语句std::ios::sync_with_stdio(false);，这样就可以取消 cin 于 stdin 的同步了。

第二种情况就是用 scanf 来获取输入了。

具体比较参考如下代码：

scanf 的时间：

```c++
#include <ctime>

const int MAXN = 10000000;
 
int numbers[MAXN];
 
void scanf_read()
{
	freopen("data.txt","r",stdin);
	for (int i=0;i<MAXN;i++)
		scanf("%d",&numbers[i]);
}

int main()
{
	int start = clock();
	scanf_read();
	printf("%.3lf\n",double(clock()-start)/CLOCKS_PER_SEC);
}
```

cin 的时间（未更改）：

```c++
#include <ctime>

const int MAXN = 10000000;
 
int numbers[MAXN];

void cin_read()
{
	freopen("data.txt","r",stdin);
	for (int i=0;i<MAXN;i++)
		std::cin >> numbers[i];
}

int main()
{
	int start = clock();
	scanf_read();
	printf("%.3lf\n",double(clock()-start)/CLOCKS_PER_SEC);
}
```

cin 的时间（已更改）：

```c++
#include <ctime>

const int MAXN = 10000000;
 
int numbers[MAXN];

void cin_read_nosync()
{
	freopen("data.txt","r",stdin);
	std::ios::sync_with_stdio(false);
	for (int i=0;i<MAXN;i++)
		std::cin >> numbers[i];
}

int main()
{
	int start = clock();
	scanf_read();
	printf("%.3lf\n",double(clock()-start)/CLOCKS_PER_SEC);
}
```

[参考博客](https://blog.csdn.net/yujuan_mao/article/details/8119529)