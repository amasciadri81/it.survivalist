# TR-069 XML parser (awk + grep)
```sh
<data model client> | grep -v SERCOMM_CML | grep '<' | \
awk -v root=${1%\.*\.}. -F'"' \
'BEGIN{
    if (root != "Device..") {
        path[0]=root; id=1
    } else 
        id=0; 
} \
/name="(.*)"/{ 
    sub(/^.*name="/,"",$0); 
 	  path[id]=$1; 
	  if ( $0 ~ /value/ ) {
	      sub(/^.*value="/, "", $0); 
		    for (i = 0; i <= id ; ++i) 
		        printf "%s" path[i];
            print " = "$1;
	  } else id++ ;
	  next
} 
{ delete path[id];  id--}'; 
```

```sh
data_model_list () { <data model client> $1 | grep -v SERCOMM_CML | grep '<' | awk -v root=${1%\.*\.}. -F'"' 'BEGIN{ if (root != "Device..") {path[0]=root; id=1} else id=0; }/name="(.*)"/{ sub(/^.*name="/,"",$0); path[id]=$1; if ( $0 ~ /value/ ) {sub(/^.*value="/, "", $0); for (i = 0; i <= id ; ++i) printf "%s" path[i]; print " = "$1;} else id++ ; next} { delete path[id];  id--}'; }
```
