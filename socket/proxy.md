nginx tcp proxy conf

【均衡规则】
a. 轮询（默认）
b. weight(调度权重)
c. ip_hash（重复请求固定调度）
d. fair（按相应时间调度）


【其他可选项】
1.down 表示单前的server暂时不参与负载

2.weight 默认为1，weight越大，负载的权重就越大

3.max_fails：允许请求失败的次数默认为1，当超过最大次数时，返回proxy_next_upstream模块定义的错误

4.fail_timeout:max_fails次失败后，暂停的时间

5.backup：其它所有的非backup机器down或者忙的时候，请求backup机器。所以这台机器压力会最轻


【范例】
stream {
    server {
        listen 5300;
        proxy_pass server_cluster;
    }

    upstream server_cluster {
        server 172.18.14.132:8888;
        server 172.18.14.132:9999;
    }
}
