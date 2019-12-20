# gz_file_filter
filter lines from Large number of gz files without unzip

由于很多原始数据/报告都使用gz压缩，由于json数据存在大量冗余导致解压之后数据量巨大，很多时候都只是为了筛选一些具体的数据，所以就有了这个脚本。

参数表:

--input_dir 默认值:'.' 输入的文件夹，将向下递归遍历所有子目录中符合条件的文件；

--output_dir 默认值:'output' 输出结果的文件夹，第一版的处理方式是将所有符合条件的行汇总到一个文件中；

--file_type 默认值:'.gz' 这个参数暂时不支持更改，因为暂时只处理了标准gz的逻辑；

--target_str 默认值:'' 筛选字符串名，脚本会输出包含这个字符串的行，过滤条件1；

--file_prefix 默认值:'rawlog.' 文件前缀，筛选条件2.


# raw_data_counter 

主要用于检查一段时间内原始数据的分布情况，在现有脚本基础上优化了IO和内存使用，所有gz文件不会在磁盘上解压或者缓存到临时文件中，在内存上完成统计并释放，同时减少了磁盘写入。

参数表:
--input_dir 默认值:'.' 输入的文件夹，将向下递归遍历所有子目录中符合条件的文件；

--event_type_field 默认值: 

输出文件:
counter.txt (utf-8 编码)