asdf
- \<INT> phy interface
- \<MARK> num integer value
- <RT_NAME>   Route Table Name
- <IP_INT>    IP of local interface
- <IP_GW>     Gateway
- <IP_NET>    Network
- <IP_NMASK>  Netmask


## Iptables
    iptables -A PREROUTING -t mangle -i <INT> -j MARK --set-mark <MARK>
    iptables -A PREROUTING -t mangle -i <INT> -j CONNMARK --save-mark
    iptables -A OUTPUT -t mangle -j CONNMARK --restore-mark
  
echo 'net.ipv4.conf.eth0/12.src_valid_mark=12' >  /etc/sysctl.d/10-tim-route.conf
sysctl -p /etc/sysctl.d/10-tim-route.conf
echo "12 tim-route" /etc/iproute2/rt_tables.d/tim-12.conf

ip rule add priority 1000 fwmark 12 table tim-route
ip route add table tim-route 0.0.0.0/0 via 192.168.7.1 dev <INT> src 192.168.7.9



ip route add table tim-route 62.101.127.116 via 192.168.7.1 dev <INT> src 192.168.7.9

## Interfaces
  
    auto <INT>
    iface <INT> inet static
            address <IP_INT>
            netamsk <IP_NMASK>

            post-up ip rule add priority 1000 fwmark 12 table tim
            post-up ip route add table tim 0.0.0.0/0 via <IP_GW> dev <INT> src <IP_INT>  # default gateway
            post-up ip route add table tim <IP_NET>/<IP_NMASK> dev <INT>            

            post-down ip rule del priority 1000 fwmark 12 table tim
            post-down ip route del table tim 0.0.0.0/0 via <IP_GW> dev <INT> src <IP_INT>  # default gateway
            post-down ip route del table tim <IP_NET>/<IP_NMASK> dev <INT>      

