# goGithub
目的：解决访问Github慢的问题；

实现原理：

&emsp;&emsp;通过多地ping对**github.com**域名进行DNS解析，自动化调用本机PING命令对解析的IP进行测速，筛选出最快的IP，写入HOST缓存。



## 使用须知

1. python3(>3.7)+Win10/Ubuntu20.04 环境下测试通过，其他类型或版本的操作系统因**HOST文件路径以及ping回显的信息不同，脚本执行可能出现问题**
2. 结合多个多地ping检测网站的结果，效果更好
3. 该脚本比较适用于访问比较慢的未墙的国外域名，无法解决科学上网问题。
4. 若出现脚本执行完成后无法连接问题，尝试在TXT文件中删除上一次执行后推荐结果的第一个IP，然后重新执行脚本




## 使用说明

**最简单**

直接执行脚本

&emsp;&emsp;```sudo python speed.py```

**全流程**
1. 访问多地ping检测的网站，点击检测，获取DNS解析的IP结果

```
# 网站参考链接如下
https://www.wepcc.com/
https://ping.chinaz.com/github.com
https://www.boce.com/ping/github.com
```
2. Ctrl+A全选后Ctrl+C复制

3. Ctrl+V粘贴到github.txt文件中

4. 管理员权限运行speed.py脚本

&emsp;&emsp;```sudo python speed.py```



## 扩展

&emsp;&emsp;可根据需要对其他域名进行相同的测速以及增加HOST解析记录的操作，您要做的是新建一个空文件，例如stackoverflow.txt，重复上述操作，注意替换掉您要测速的域名，最后在speed.py中配置PAHT以及DOMAIN变量，Enjoy!

