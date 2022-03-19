# ecgdata
在 ecg_data 文件夹下 放置 官网下载的数据

然后运行 make_data.py 后会生成两个 txt 文件

一个训练数据文件 traindata.txt，一个 测试数据文件 testdata.txt



### txt文件格式约定

每行给出一个心拍的数据 包括 300 个信号点 与 一个标签

300个信号点对应的电压值均以浮点数表示， 空格隔开

心律标签用一个整形数据表示, 与第300个信号点数据用空格隔开， 整形数据后有一个换行符

数据表示具体对应关系如下

| 标签 | Figure |
| :--: | :----: |
|  N   |   0    |
|  A   |   1    |
|  V   |   2    |
|  L   |   3    |
|  R   |   4    |

N A V L R 的具体含义参见[博客](https://www.cnblogs.com/lxy764139720/p/12830037.html)

附一个c读取代码：

```cpp
/**
	filename 文件名
	row 数据文件中心拍的个数 即 行数
	col 每个心拍记录的信号点个数 本例中为300
	input label 分别存放数据与所对应的标签
**/
void loadData(const char* filename, int row, int col, double **input, int *label) {	
	if (input == NULL || label == NULL) return;
	FILE *df = fopen(filename, "r");
	for (int i = 0; i < row; ++i) {
		for (int j = 0; j < col; ++j) {
			fscanf(df, "%lf", &input[i][j]);
		}
		fscanf(df, "%d", &label[i]);
	}
	fclose(df);
}
```

