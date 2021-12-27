Make your file
```
/etc/rsyslog.d/my_remote_syslog.conf 
```

```bash
# provides UDP syslog reception
module(load="imudp")
input(type="imudp" port="514")

# template
$template RemoteLogs,"/var/log/vodafone/%FROMHOST-IP%.log"
# avoid to manage localhost logs
if $fromhost-ip != '127.0.0.1' then -?RemoteLogs

& stop
```

