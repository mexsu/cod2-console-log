#!/bin/bash
#TheUser=`whoami`
fsGame="mods/yes_cod2" #fs mode

sudo iptables -I INPUT -p UDP --sport 20700 -s cod2master.activision.com -j REJECT #Must be -I so it inserted as the first rule
sudo iptables -A INPUT -p udp -m string --algo bm --string "BANNED_CDKEY" --sport 20700 --dport 28960 -j DROP
sudo iptables -A INPUT -p udp -m string --algo bm --string "INVALID_CDKEY" --sport 20700 --dport 28960 -j DROP

#Save iptables with the new rules without deleting any or adding it more than once
mkdir -p ~/tmp
#sudo iptables-save > ~/tmp/iptables.conf
sudo iptables-save | awk '!x[$0]++' > ~/tmp/iptables_new.conf #remove duplicates without sorting
sudo iptables-restore < ~/tmp/iptables_new.conf

cd ~/Cod2Server # go to the folder where the game exists cod2
#should check if fsGame even exists if there any mode added or just create the fsGame even if its not created
mkdir -p $fsGame
mkdir -p /var/www/html/$fsGame
#g_allowvote 0 , move mods to web so player can download faster and for security , redirect to web
#exclude any folder and only take the mods that end with .iwd without _svr_.iwd and add fsGame as prefix so it can be copied because you are not in the same directory
cp `ls $fsGame | grep .iwd | grep -v _svr_.iwd | sed 's|.*|'${fsGame}'\/&|g'` /var/www/html/$fsGame/
> ~/.callofduty2/$fsGame/server.log  #empty file if exists/create new file,folder same as fs_game mod

rm screenlog.0 #log created by screen with option -L

screen -A -h 500 -m -d -S cod2 -L ./cod2_lnxded +set fs_game "$fsGame" +set rcon_password "YOU,RCON,PASSWORD,HERE" +exec config_filegyGB.cfg
#Don't add your rcon password to the config file
#use random config name file because it can be download and hacked by players and look at your the rcon_password
sleep 1
screen -A -h 500 -m -d -S console -L ./py.py
#sleep 1  # Waits 1 second
screen -r cod2 -X colon "logfile flush 0^M" #make the screen log file flush every 0 seconds so the log display in real time

screen -ls
echo "Done" #$TheUser
