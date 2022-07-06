# Configure OpenVPN Server on Mikrotik

## CERTIFICATES

### Add templates
    /certificate add country="IT" state="IT" locality="Milan" organization="myCompany" unit="mi" \
        name=template-CA common-name=my-CA \
        key-size=4096 days-valid=3650 key-usage=crl-sign,key-cert-sign
        
    /certificate add country="IT" state="IT" locality="Milan" organization="myCompany" unit="mi" \
        name=template-server common-name=my-server \
        key-size=4096 days-valid=3650 key-usage=digital-signature,key-encipherment,tls-server
        
    /certificate add country="IT" state="IT" locality="Milan" organization="myCompany" unit="mi" \
        name=template-client common-name=my-client \
        key-size=4096 days-valid=3650 key-usage=tls-client         
 
### Sign Certificates
Signing Certificates can need some minutes.

    /certificate sign template-CA ca-crl-host=_<A MIKROTIK IP>_ name=my-CA
    /certificate sign template-server ca=my-CA name=my-server
    /certificate sign template-client ca=my-CA name=my-client

### Trust Certificates

    /certificate set my-CA trusted=yes
    /certificate set my-server trusted=yes

### Export
You need the certificate to make the ovpn configuration file for clients.

    /certificate export-certificate my-CA export-passphrase="_<PASSPHRASE>_"
    /certificate export-certificate my-client export-passphrase="_<PASSPHRASE>_"

## POOL IP
If you want to assign automatically an IP Address to the remote client, you need to configure the POOL

    /ip pool add name=pool-ovpn ranges=192.168.25.10-192.168.25.254

## OpenVPN Service

    /ppp profile add name="profile-ovpn" use-encryption=yes \
        local-address=192.168.25.1 remote-address=pool-ovpn dns-server=8.8.8.8 
    /interface ovpn-server server set default-profile=profile-ovpn certificate=my-server \
        require-client-certificate=yes auth=sha1 cipher=aes128,aes192,aes256 enabled=yes mode=ip

### Firewall
Now you need to configure the firewall, you can set the port and the protocl of your OpenVpn Server.

    /ip firewall filter add chain=input action=accept comment=OpenVPN dst-port=1194 protocol=tcp log=no

  






