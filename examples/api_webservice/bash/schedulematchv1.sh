#!/usr/bash

sitehostname=manageddreams.com
# sitehostname=localhost
pagepath=/springgridstaging/api_webservice.py
# pagepath=/springgrid/api_webservice.py

contentfile=$(mktemp)
cat >$contentfile << EOF
<?xml version="1.0"?>
<methodCall>
  <methodName>schedulematchv1</methodName>
  <params>
     <param>
        <value>SmallDivide.smf</value>
     </param>
     <param>
        <value>Balanced Annihilation V6.96</value>
     </param>
     <param>
        <value><array><data>
           <value><struct>
              <member>
                 <name>ai_version</name>
                 <value><string>0.9</string></value>
              </member>
              <member>
                 <name>ai_name</name>
                 <value><string>AAI</string></value>
              </member>
           </struct></value>
           <value><struct>
              <member>
                 <name>ai_version</name>
                 <value><string>0.9</string></value>
              </member>
              <member>
                 <name>ai_name</name>
                 <value><string>AAI</string></value>
              </member>
           </struct></value>
        </data></array></value>
     </param>
     <param>
        <value><array><data>
        </data></array></value>
     </param>
  </params>
</methodCall>
EOF

cat $contentfile
contentsize=$(cat $contentfile | wc -c)
echo $contentsize

httpcontentfile=$(mktemp)
cat >$httpcontentfile << EOF
POST ${pagepath} HTTP/1.0
Host: ${sitehostname}
Content-type: text/xml
Content-length: $contentsize

EOF

cat ${contentfile} >> ${httpcontentfile}
cat ${httpcontentfile}

nc ${sitehostname} 80 <${httpcontentfile}

