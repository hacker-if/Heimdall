sudo apt update
sudo apt upgrade
sudo apt install nginx python3-pip

cd ~
git clone https://github.com/hackerspaceIFUSP/Heimdall
cd Heimdall

#configuracao do site

pip3 install -U --user pip
pip3 install --user pipenv

pipenv --three
pipenv install

pipenv run flask db init && flask db migrate -m "init" && flask db upgrade

sudo cp config_files/heimdall.service /etc/systemd/system/
sudo systemctl enable heimdall.service
# sudo systemctl start heimdall.service

# configuracao do nginx

sudo rm /etc/nginx/sites-enabled/default
sudo cp config_files/nginx /etc/nginx/sites-available/heimdall
sudo ln -s /etc/nginx/sites-available/heimdall /etc/nginx/sites-enabled/heimdall
sudo systemctl restart nginx
