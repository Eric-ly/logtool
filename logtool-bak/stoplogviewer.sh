kill   -9   `ps   -ef|grep  "logviewer.py" | grep -v "grep"|awk   '{print   $2} '`

