ssh -t localhost -- bash /usr/local/src/nheim/perso-cv-jinja/prod_01.sh
ssh vps01.37rtm.local -- sudo rm -rf /var/www/html/resume/*
ssh localhost "cd /usr/local/src/nheim/perso-cv-jinja/out/; tar cfh - cv*" | ssh vps01.37rtm.local "cd /var/www/html/resume; sudo tar xf -"
REM ssh vps01.37rtm.local -- sudo /bin/bash -c "cd /var/www/html/resume/ && chown 'www-data:www-data' * && ln -s ./cv.html ./dc.html"
ssh vps01.37rtm.local -- sudo /bin/bash -c "id && { cd /var/www/html/resume; sudo chown 'www-data:www-data' * && sudo ln -s ./cv.html ./dc.html; }"

