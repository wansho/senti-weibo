# Memory Optimization

由于经费有限，我们只在阿里云上购买了 双核4GB 的低配服务器。因为 Web 服务/数据库/模型训练/爬虫等所有任务都在这一台机器上完成，所以内存优化是我们的一个重点。内存优化主要有如下几个方面的优化：

1. Linux 系统层级的优化
2. Mysql 访问优化
3. 模型与分词器优化
4. Web 服务优化
5. Python 编码优化

## Linux 系统层级的优化

由于需要频繁对数据库进行读写，久而久之，`buff/cache` 就会占用大量的内存空间(极端情况下，会占用 3GB 左右的内存)，导致模型无法加载。所以我们编写了 crontab 脚本，在 `buff/cache`  达到 500MB 的阈值时，定期对齐释放空间。

## Mysql 访问优化

* 我们对爬虫的数据存储，进行了优化，从每条微博存储一次，到 `bulk_create` 批量的存储
* 我们对微博存放的大表进行 partition 处理，加速数据库的读写速度
* 加入 key 提高访问速度

## 模型与分词器优化

目前效果较好的中文分词器是 [pkuseg](<https://github.com/lancopku/pkuseg-python>)，但是加载 pkuseg 需要消耗 700MB 的内存，导致分词器运行时，模型因为内存不够而加载失败，所以我们选择了性能与资源占用平衡的 [jieba](<https://github.com/fxsjy/jieba>) 作为分词工具。需要注意的是，如果训练集和测试集的分词工具不一样，那么分词结果的不同会直接影响到分类器的分类效果。

## Web 服务优化



## Python 编码优化

Python 编码是一个很多人容易忽视的地方，有大量的细节可以去优化，有时候，一个错误的。例如：

1. 字符串优化

   ```python
   # 字符串拓展
   
   # good case
   ss += "python 优化" 
   # bad case
   ss = ss + "python 优化"
   ```

2. sequence 优化

   ```python
   # sequence 相加
   
   lol = ["rw", "edg", "rng"]
   lpl = ["ig", "top", "snake"]
   
   # good case
   lol.extend(lpl)
   lol += lpl
   # bad case
   lol = lol + lpl
   ```

3. `in-place method` 优化

   ```python
   # 排序优化
   
   # good case
   list1.sort()
   # bad case
   sorted(list1)
   ```

4. 用 生成器 替换 列表推导式

   ```python
   # good case
   floats = array("d", (random() for i in range(10**7)))
   # bad case
   floats = array("d", [random() for i in range(10**7)])
   ```

5. Others

经过优化后的 Fluent Python 代码，相较于 生硬的Python 代码，其性能的提升，绝对是肉眼可见的。