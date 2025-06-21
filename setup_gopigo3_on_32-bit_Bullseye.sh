#!/bin/bash

# FILE: setup_gopigo3_on_32-bit_Bullseye.sh

# called next
check_if_run_with_pi() {
  ## if not running with the pi user then exit
  if [ $(id -ur) -ne $(id -ur pi) ]; then
    echo "GoPiGo3 installer script must be run with \"pi\" user. Exiting."
    exit 6
  fi
}

echo "Check running as user pi"
check_if_run_with_pi

echo "Install needed python packages and git"
sudo apt install -y --no-install-recommends python3-pip python3-numpy python3-curtsies git

echo "Check default python"
python --version

echo "Check pip version"
pip --version

echo "Check for setuptools"
dpkg -l | grep setuptools

echo "Check for wheel"
dpkg -l | grep wheel

echo "Bring down GoPiGo3 code"
cd ~
sudo git clone http://www.github.com/DexterInd/GoPiGo3.git /home/pi/Dexter/GoPiGo3

echo "Install DI update_tools"
sudo curl -kL dexterindustries.com/update_tools | bash -s -- --system-wide --use-python3-exe-too --install-deb-debs --install-python-package

echo "Bring down DI_Sensors code"
sudo git clone https://github.com/DexterInd/DI_Sensors.git /home/pi/Dexter/DI_Sensors

echo "Put copy of serial number file where expected"
cp ~/Dexter/GoPiGo3/Install/list_of_serial_numbers.pkl ~/Dexter/.list_of_serial_numbers.pkl

echo "Setup espeak-ng for ip feedback"
sudo apt install -y espeak-ng

echo "Bring down ip_feedback setup script"
wget https://raw.githubusercontent.com/slowrunner/GoPiGo3-Bullseye_32-bit/main/setup_ip_feedback.sh
chmod 777 setup_ip_feedback.sh

echo "Run ip feedback setup script"
sudo ./setup_ip_feedback.sh

echo "Get and make particular pigpio package required by GoPiGo3"
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
cd ..
rm master.zip

echo "Create non-forking pigpio service required by GoPiGo3"
echo "[Unit]" > pigpiod.service
echo "Description=Pigpio daemon" >> pigpiod.service
echo "After=network.target syslog.target" >> pigpiod.service
echo "StartLimitIntervalSec=60" >> pigpiod.service
echo "StartLimitBurst=5" >> pigpiod.service
echo "StartLimitAction=reboot" >> pigpiod.service
echo " " >> pigpiod.service
echo "[Service]" >> pigpiod.service
echo "Type=simple" >> pigpiod.service
echo "ExecStartPre=/sbin/sysctl -w net.ipv4.tcp_keepalive_time=300" >> pigpiod.service
echo "ExecStartPre=/sbin/sysctl -w net.ipv4.tcp_keepalive_intvl=60" >> pigpiod.service
echo "ExecStartPre=/sbin/sysctl -w net.ipv4.tcp_keepalive_probes=5" >> pigpiod.service
echo "# Don't fork pigpiod" >> pigpiod.service
echo "ExecStart=/usr/local/bin/pigpiod -g" >> pigpiod.service
echo "ExecStop= " >> pigpiod.service
echo "Restart=always" >> pigpiod.service
echo "RestartSec=10" >> pigpiod.service
echo " " >> pigpiod.service
echo "[Install]" >> pigpiod.service
echo "WantedBy=multi-user.target" >> pigpiod.service

echo "Finished non-foking pigpiod.service file"
cat pigpiod.service

echo "Setup, enable, start the non-forking pigpiod service"
sudo cp pigpiod.service /etc/systemd/system
sudo systemctl enable pigpiod.service
sudo systemctl start pigpiod.service
# echo "Status of the new service"
# systemctl status pigpiod.service

echo "Remove the local service file"
rm pigpiod.service

echo "Remove the pigpio-master files"
sudo rm -r pigpio-master/

echo "Enable SPI and I2C"
if grep -q "#dtparam=spi=on" /boot/config.txt; then
        sudo sed -i 's/#dtparam=spi=on/dtparam=spi=on/g' /boot/config.txt
        echo "SPI enabled"
    elif grep -q "dtparam=spi=on" /boot/config.txt; then
        echo "SPI already enabled"
    else
        sudo sh -c "echo 'dtparam=spi=on' >> /boot/config.txt"
        echo "SPI enabled"
    fi

if grep -q "#dtparam=i2c_arm=on" /boot/config.txt; then
        sudo sed -i 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/config.txt
        echo "I2C  enabled"
    elif grep -q "dtparam=i2c_arm=on" /boot/config.txt; then
        echo "I2C already enabled"
    else
        sudo sh -c "echo 'dtparam=i2c_arm=on' >> /boot/config.txt"
        echo "I2C enabled"
    fi

if grep -q "#dtparam=i2c1=on" /boot/config.txt; then
        sudo sed -i 's/#dtparam=i2c1=on/dtparam=i2c1=on/g' /boot/config.txt
        echo "I2C_1 enabled"
    elif grep -q "dtparam=i2c1=on" /boot/config.txt; then
        echo "I2C_1 already enabled"
    else
        sudo sh -c "echo 'dtparam=i2c1=on' >> /boot/config.txt"
        echo "I2C_1 enabled"
    fi
    
    
echo "Get R4R_Tools (for I2C_mutex)"
sudo git clone https://github.com/DexterInd/RFR_Tools.git /home/pi/Dexter/lib/Dexter/RFR_Tools
sudo apt install -y libffi-dev
cd /home/pi/Dexter/lib/Dexter//RFR_Tools/miscellaneous/
sudo python3 setup.py install

echo "Get wiringPi"
cd /home/pi/Dexter/lib
git clone https://github.com/DexterInd/wiringPi/
cd wiringPi
sudo chmod +x ./build
sudo ./build

echo "Skipping antenna_wifi service install"

echo "Get and install GPG3_POWER service"
cd ~
sudo cp /home/pi/Dexter/GoPiGo3/Install/gpg3_power.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/gpg3_power.service
sudo systemctl daemon-reload
sudo systemctl enable gpg3_power.service
sudo systemctl start gpg3_power.service

echo "Skipping autodetect robot"

echo "Setup GoPiGo3 and DI_Sensors Python3 eggs"
cd /home/pi/Dexter/GoPiGo3/Software/Python
sudo python3 setup.py install
cd /home/pi/Dexter/DI_Sensors/Python
sudo python3 setup.py install


echo "============="
echo "GOPIGO3 INSTALL COMPLETE"
echo " "
echo "Checking Installation Result"
installresult=$(python3 -c "import gopigo3; g = gopigo3.GoPiGo3()" 2>&1)
if [[ $installresult == *"ModuleNotFoundError"* ]]; then
   echo "GOPIGO3 SOFTWARE INSTALLATION FAILURE: "+$installresult
   echo "Suggest installing over Legacy Pi OS (Buster)."
elif [[ $installresult == *"IOError"* ]]; then
   echo "No SPI response. GoPiGo3 not detected: "+$installresult
   echo "Ensure SPI is enabled in raspi-config."
elif [[ $installresult == *"FirmwareVersionError"* ]]; then
   echo "GoPiGo3 detected with a possible firmware issue: "
   echo $installresult
else
    echo "GOPIGO3 SOFTWARE INSTALLATION SUCCESSFUL."
fi

echo " ================= "
echo "PERFORM FULL POWER OFF BY:"
echo "sudo shutdown -h now"
