tput setaf 1;
echo '--------------reiniciando el servidor------------------------------'
tput sgr0;
systemctl restart httpd
tput setaf 1;
echo '--------------Listo------------------------------'
tput sgr0;
exit