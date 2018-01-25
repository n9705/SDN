## 负载均衡
### topo.py用于建立实验拓扑
输入命令
`
sudo mn --custom topo.py --topo mytopo --controller=remote,ip=127.0.0.1,port=6653 --switch ovsk,protocols=OpenFlow13
`
### 建立拓扑后运行sdn.py，实现负载均衡
输入命令
`
sudo python sdn.py
`
## 实验场景
![](http://images2017.cnblogs.com/blog/1226734/201801/1226734-20180125205629709-775168189.png)  

服务器h2 h3上各自有不同的服务，h1是客户端。实现一个负载均衡的北向程序，当h2和h3向h1传输数据时，北向应用根据链路的使用状况动态的调整路由规则。

例如:当h2向h1使用s1-s2链路达到满负荷状态下，h3向h1的传输路径应该动态的调整为s3所在路径，而当h2停止向h1传输数据时，h3应调整回s1-s2路径。

