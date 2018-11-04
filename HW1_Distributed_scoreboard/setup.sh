echo '######upgrade apt-get######'
sudo apt-get update
echo '######install python######'
sudo apt-get install python
echo '######install python pip######'
sudo apt-get install -y python-pip
echo '######in case the LC_ALL variable is missing######'
export LC_ALL=C
echo '######install kazoo######'
pip install kazoo
echo '######install scipy######'
pip install scipy
echo '######copy player to bash command######'
echo '######to run the player program you can type "player [ip:port] [name] [count] [delay] [mean]"'
sudo cp -pf player.py /usr/local/bin/player
echo '######copy watcher to bash command######'
echo '######to run the watcher program you can type "watcher [ip:port] [watcher list size]"'
sudo cp -pf watcher.py /usr/local/bin/watcher
