#!/usr/bin/bash

echo "[+] Retrieving submodules"
git submodule update --init --recursive

echo "[+] Installing Python3 requirements"
sudo apt install -y python3-pip

echo "[+] Installing GNU Radio dependencies"
install_antsdr_uhd() {
	sudo apt-get install autoconf automake build-essential ccache cmake cpufrequtils doxygen ethtool \
	g++ git inetutils-tools libboost-all-dev libncurses5 libncurses5-dev libusb-1.0-0 libusb-1.0-0-dev \
	libusb-dev python3-dev python3-mako python3-numpy python3-requests python3-scipy python3-setuptools \
	python3-ruamel.yaml
	git clone https://github.com/MicroPhase/antsdr_uhd.git
	cd antsdr_uhd
	cd host/
	mkdir build
	cd build
	cmake ../
	make -j$(nproc)
	sudo make install
	sudo ldconifg
	cd ../../
}

sudo apt-get install gnuradio gnuradio-dev -y

sudo apt install -y git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy \
python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev \
libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 \
liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins \
python3-zmq python3-scipy python3-gi python3-gi-cairo gobject-introspection gir1.2-gtk-3.0 \
libsndfile-dev libtalloc-dev libpcsclite-dev wget unzip python3-pip libbladerf-dev \
libuhd-dev uhd-host librtlsdr-dev

while true; do
	read -p "Do you which to install the UHD version of ANTSDR (YES), or the original one [NO]? " yn
        case $yn in
                [Yy]* ) install_antsdr_uhd; break;;
                [Nn]* ) sudo apt install libuhd-dev uhd-host librtlsdr-dev; break;;
                * ) echo "Please answer [Y]yes or [N]no.";;
        esac
done

sudo pip3 install pyserial --break-system-packages

echo "[+] Installing osmocore"
sudo apt -y install build-essential libosmocore libosmocore-dev libtool libtalloc-dev libsctp-dev shtool autoconf automake git-core pkg-config make gcc gnutls-dev libusb-1.0-0-dev libmnl-dev
cd thirdparty
REMPATH=`pwd`
#sudo apt install gr-osmosdr
git clone https://github.com/PentHertz/gr-osmosdr.git
cd gr-osmosdr
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
make -j$(nproc)
sudo make install
cd $REMPATH
echo "[+] Downloading gr-gsm for Python3 and GNU Radio 3.10"
git clone https://github.com/FlUxIuS/gr-gsm.git
echo "[+] Building and installing gr-gsm for GNU Radio 3.10"
cd gr-gsm
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr/local ../
make -j$(nproc)
sudo make install
cd ../../
echo "[+] Installing SDK tools"
sudo apt install -y openjdk-25-jdk
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
unzip platform-tools-latest-linux.zip
sudo mkdir -p /opt/Android
sudo cp -R platform-tools
echo "[+] Installing dependencies for srsLTE"
sudo apt-get install cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev
sudo apt install libsoapysdr-dev
#osmo sdr support:
sudo apt-get install osmo-sdr soapysdr-module-osmosdr
#rtl sdr support:
sudo apt-get install rtl-sdr soapysdr-module-rtlsdr
#blade rf support:
sudo apt-get install bladerf soapysdr-module-bladerf
#hack rf support:
sudo apt-get install hackrf soapysdr-module-hackrf
#usrp support:
sudo apt-get install uhd-soapysdr soapysdr-module-uhd
#miri SDR support:
sudo apt-get install miri-sdr soapysdr-module-mirisdr
#rf space support:
sudo apt-get install soapysdr-module-rfspace
#airspy support:
sudo apt-get install airspy soapysdr-module-airspy
echo "[+] Installaing srsLTE for Modmobmap"
cd $REMPATH
ls 
cd srsLTE
mkdir build
cd build
cmake ../
make -j$(nproc)
echo "====END===="
