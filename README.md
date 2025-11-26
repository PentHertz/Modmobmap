Modmobmap
==========

Modmobmap is a tool aimed to retrieve information on cellular networks.
As shown in the first [presentation made at BeeRump 2018](https://www.rump.beer/2018/slides/modmobmap.pdf), this tool is able to retrieve information of 2G, 3G, 4G, and more cellular network types with minimum requirement: only phone with ServiceMode.

For the moment, the tool has only been tested and developed for the following devices:
- Samsung Galaxy S3 via [xgoldmon (Modmobmap's edition)](https://github.com/FlUxIuS/xgoldmon);
- Samsung Galaxy S4;
- Samsung Galaxy S5;
- Samsung Galaxy Note 2 with LTE;
- Samsung Galaxy S20

Moreover, as it's compatible for XGold via Modmobmap's forked of *xgoldmon*, this tool should also be able to work with devices supported by *xgoldmon* as well:
- Samsung Galaxy S4 GT-I9500 (this is the version without LTE!)
- Samsung Galaxy Nexus GT-I9250 (has to be rooted!)
- Samsung Galaxy S2 GT-I9100
- Samsung Galaxy Note 2 GT-N7100

Note that all devices should be rooted. In any other case, you will have to use the DFR technique by hand!

Also: Patches, or engines, for other devices are very much welcomed! ;)

But this is not finished yet, Modmobmap include a GRGSM scanner to scan GSM cells with SDR. Compatible SDR devices are the same as those compatible with `gr-osmosdr` as follows:

* FunCube Dongle through libgnuradio-fcd
* FUNcube Dongle Pro+ through gr-fcdproplus
* sysmocom OsmoSDR Devices through libosmosdr
* Nuand LLC bladeRF through libbladeRF library
* Great Scott Gadgets HackRF through libhackrf
* Ettus USRP Devices through Ettus UHD library
* Fairwaves UmTRX through Fairwaves' fork of Ettus' UHD library
* RFSPACE SDR-IQ, SDR-IP, NetSDR (incl. X2 option)
* RTL2832U based DVB-T dongles through librtlsdr
* RTL-TCP spectrum server (see librtlsdr project)
* MSi2500 based DVB-T dongles through libmirisdr
* SDRplay RSP through SDRplay API library
* AirSpy R820t dongles through libairspy

Modmobmap is also able to scan LTE cells by wrapping srsLTE tools. The engine supports several SDR devices:

* USRP
* BladeRF
* HackRF
* RFSpace
* ANTSDR E200 (with the right UHD installation)
* and so on.

Requirements
-------------

Here are the following requirements:
- Python 3;
- Last Android SDK to run ADB: https://developer.android.com/studio/#downloads;
- A compatible mobile phone;
- GNU Radio 3.10 with gr-gsm to scan GSM stations with Software-Defined Radio
- A valid/invalid SIM card (just in case to provide an IMSI number).

Ubuntu installation
---------------------

A `install_all-Ubuntu_24.04.sh` script installing all dependencies for all engines is available in the root directory.

For other distributions, please adapt this script base on listed dependencies.

How to use
----------

The tool is provided with quick help that shows you the required argument as follows:

```
python modmobmap.py -h
usage: modmobmap.py [-h] [-m MODULE] [-n NETWORKS] [-o] [-s ANDROIDSDK]
                    [-a ATMODE] [-f FILE]Before running the engine, make sure all dependencies are installed. You can refer to the installation script 

Mobile network mapping tool with cheap equipments

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        Module to use (e.g: "servicemode" by default)
  -n NETWORKS, --networks NETWORKS
                        Networks in MCCMNC format splitted with commas
  -o, --cached_operator
                        Use operator in cache to speed up the passive scan
  -s ANDROIDSDK, --sdk ANDROIDSDK
                        Android SDK path
  -a ATMODE, --at ATMODE
                        AT access mode. If host put something like
                        "/dev/ttyUSBxx. By default it uses ADB."
  -f FILE, --file FILE  File to parse. For the moment it could be used in
                        combination with AT mode host.
```

Assuming the Android SDK is installed in */opt/Android*, the tool can be quickly started as follows:

```
$ sudo python modmobmap.py
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 2 operator(s)
{u'20810': u'F SFR', u'20820': u'F-Bouygues Telecom'} 
[+] Unregistered from current PLMN
[+] New cell detected [CellID/PCI-DL_freq  (4XXX-81)]
 Network type=2G
 PLMN=208-10
 ARFCN=81
[+] New cell detected [CellID/PCI-DL_freq  (6XXXXXX-2950)]
 Network type=3G
 PLMN=208-20
 Band=8
 Downlink UARFCN=2950
 Uplink UARFCN=2725
[+] New cell detected [CellID/PCI-DL_freq  (3XX-6300)]
 Network type=4G
 PLMN=208-10
 Band=20
 Downlink EARFCN=6300
[+] New cell detected [CellID/PCI-DL_freq  (3XX-2825)]
 Network type=4G
 PLMN=208-10
 Band=7
 Downlink EARFCN=2825
[+] New cell detected [CellID/PCI-DL_freq  (3XX-1675)]
 Network type=4G
 PLMN=208-10
 Band=3
 Downlink EARFCN=1675
[...]
```

Note: If the Android SDK is installed anywhere else, you can use the *-s* parameter to specify its directory.

Speed-up the passive scan
---------------------------

When looking for operators, an AT command is sent to the modem. If you want to speed-up the scanning, you can hardcoded the operators to the following file `cache/operators.json`:

```
{
    "20801": "Orange",
    "20810": "F SFR", 
    "20815": "Free",
    "20820": "F-Bouygues Telecom"
}
```

Only the MCC/MNC codes are important. Then you can re-launch the tool as follows:

```
$ sudo python modmobmap.py -o   
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 4 operators in cache, you choose to reuse them.
Found 4 operator(s)
{u'20810': u'F SFR', u'20820': u'F-Bouygues Telecom', u'20815': u'Free', u'20801': u'Orange'} 
[+] Unregistered from current PLMN
[+] New cell detected [CellID/PCI-DL_freq  (XXXX-10614)]
 Network type=3G
 PLMN=208-10
 Band=1
 Downlink UARFCN=10614
 Uplink UARFCN=9664
[...]
[+] New cell detected [CellID/PCI-DL_freq  (XXX-3501)]
 Network type=4G
 PLMN=208-20
 Band=8
 Downlink EARFCN=3501
[...]
[+] Unregistered from current PLMN
=> Changing MCC/MNC for: 20815
[+] New cell detected [CellID/PCI-DL_freq  (XXX-2825)]
 Network type=4G
 PLMN=208-15
 Band=7
 Downlink EARFCN=2825
[...]
=> Changing MCC/MNC for: 20801
[+] New cell detected [CellID/PCI-DL_freq  (XXXXX-3011)]
 Network type=3G
 PLMN=208-1
 Band=8
 Downlink UARFCN=3011
 Uplink UARFCN=2786
[...]
```

Note we have been able to detect other cells the AT command *AT+COPS* did not return.

A complete list of MCC and MNC codes could be retrieved anywhere on the internet and in Wikipedia: https://en.wikipedia.org/wiki/Mobile_country_code

Focusing some operators
------------------------

It is possible to tell *Modmobmap* to focus only on specific operators with the *-m* argument:

```
$ sudo python modmobmap.py -n 20801
=> Manual MCC/MNC processing...
Found 1 operator(s)
{'20801': '20801'} 
[...]
=> Changing MCC/MNC for: 20801
[+] New cell detected [CellID/PCI-DL_freq  (XXX-1675)]
 Network type=4G
 PLMN=208-01
 Band=3
 Downlink EARFCN=1675
[+] New cell detected [CellID/PCI-DL_freq  (XXXXX-3011)]
 Network type=3G
 PLMN=208-1
 Band=8
 Downlink UARFCN=3011
 Uplink UARFCN=2786
=> Changing network type for 3G only
[+] New cell detected [CellID/PCI-DL_freq  (XXXXX-2950)]
 Network type=3G
 PLMN=208-1
 Band=8
 Downlink UARFCN=2950
 Uplink UARFCN=2725
```

Using Modmobmap with xgoldmon
------------------------------

With XGold modems, the use of xgoldmon will be required. But for now, only the fork for *Modmobmap* works to retrieve exact information of cells via the DIAG interface and could be downloaded at: https://github.com/FlUxIuS/xgoldmon

Then after compiling, the tool *xgoldmon* could be started using the *-m* parameter like this:

```
sudo ./xgoldmon -t s3 -m /dev/ttyACM1
```

This will create a FIFO file that will be requested by Modmobmap later:

```
$ ls
celllog.fifo  Makefile   screenshot-mtsms-while-in-a-call.png  xgoldmon
```

Then we can start running *Modmobmap* as follows by specifying the AT serial interface (*/dev/ttyACM0*) and the FIFO file created by *xgoldmon* (*<xgoldmonpath/celllog.fifo*):

```
$ sudo python3 modmobmap.py -f /<xgoldmon path>/celllog.fifo -m xgoldmod -a /dev/ttyACM0  -o
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 4 operators in cache, you choose to reuse them.
Found 4 operator(s)
{'20801': 'Orange', '20810': 'F SFR', '20815': 'Free', '20820': 'F-Bouygues Telecom'} 
[+] New cell detected [CellID/PCI-DL_freq  (0x7XXXX-65535)]
 Network type=3G
 PLMN=208-1
 Downlink UARFCN=65535
 Uplink UARFCN=2850
[+] Unregistered from current PLMN
[+] New cell detected [CellID/PCI-DL_freq  (0x7XXXX-3011)]
 Network type=3G
 PLMN=208-1
 Downlink UARFCN=3011
 Uplink UARFCN=2786
[...]
[+] Unregistered from current PLMN
=> Changing MCC/MNC for: 20810
[+] New cell detected [CellID/PCI-DL_freq  (0x3XXXXX-3075)]
 Network type=3G
 PLMN=208-10
 Downlink UARFCN=3075
 Uplink UARFCN=2850
[...]
 ```

Note that retrieving results from AT+COPS command could take a lot of time and sometime would need to restart the tool. If the tool is blocked on the operator retrieving step, please use cached or targeted operators' features instead.

Using Modmobmap with GRGSM
------------------------------

Drivers supported:

* bladerf
* uhd
* rtlsdr
* redpitaya
* soapy

Modmodmap can be used with `gr-gsm` to retrieve GSM cells' information with a Software-Defined Radio device compatible with OSMOSDR.

To use this feature, please issue the following command:

```
$ python modmobmap.py -m grgsm -b GSM-R,GSM900 -g rtlsdr
=> Switching to GSM-R band
[+] New cell detected [CellID/PCI-DL_freq  (****)]
 Network type=2G
 PLMN=****
 ARFCN=978
[+] New cell detected [CellID/PCI-DL_freq  (*****)]
 Network type=2G
 PLMN=20820
 ARFCN=983
[+] New cell detected [CellID/PCI-DL_freq  (*****)]
 Network type=2G
 PLMN=20820
 ARFCN=1014
[+] New cell detected [CellID/PCI-DL_freq  (*****)]
 Network type=2G
 PLMN=20810
 ARFCN=79
[+] New cell detected [CellID/PCI-DL_freq  (****)]
 Network type=2G
 PLMN=20810
 ARFCN=86
=> Switching to GSM900 band
[+] New cell detected [CellID/PCI-DL_freq  (*****)]
 Network type=2G
 PLMN=20820
 ARFCN=978
```

Using Modmobmap with srsRAN
------------------------------

Supported drivers:

* uhd
* bladerf
* soapy


Modmodmap can be used with `srsRAN` to retrieve LTE cells with a Software-Defined Radio device compatible with UHD, and Soapy drivers like the RTL-SDR.

Before running the engine, make sure all dependencies are installed. You can refer to the installation script to install all appropriate dependencies. Also make sure that all submodules are pulled from the repository:

```
git submodule update --init --recursive
```


To launch the tool with USRP, or bladeRF, you can choose or not to specify the driver as follows:

```
$ python3 modmobmap.py -m srslte_pss -b 28 -g 'driver=usrp' 
```

With Soapy, use this format of command instead precising the `id` of the device to avoid picking a random device (e.g, sound device...):
```
python3 modmobmap.py -m srslte_pss -b 28 -g 'soapy:id=1'
Active RF plugins: libsrsran_rf_uhd.so libsrsran_rf_soapy.so libsrsran_rf_blade.so libsrsran_rf_zmq.so
Inactive RF plugins: 
Opening RF device...
Supported RF device list: UHD soapy bladeRF zmq file
[INFO] [UHD] linux; GNU C++ version 9.2.1 20200304; Boost_107100; UHD_3.15.0.0-2build5
Found Rafael Micro R820T tuner
[...]
Soapy has found device #1: available=Yes, driver=rtlsdr, label=Generic RTL2832U OEM :: 00000001, manufacturer=Realtek, product=RTL2838UHIDIR, rtl=0, serial=00000001, tuner=Rafael Micro R820T, 
Selecting Soapy device: 1
[...]
[+] New cell detected [CellID/PCI-DL_freq  (447-9230)]
 Network type=4G
 PLMN=-1
 Band=28
 Downlink EARFCN=9230
[ 21/449]: EARFCN 9231 Freq. 760.10 MHz looking for PSS.
[+] New cell detected [CellID/PCI-DL_freq  (303-9231)]
 Network type=4G
 PLMN=-1
 Band=28
 Downlink EARFCN=9231
[ 22/449]: EARFCN 9232 Freq. 760.20 MHz looking for PSS.
[+] New cell detected [CellID/PCI-DL_freq  (0-9233)]
 Network type=4G
 PLMN=-1
 Band=28
 Downlink EARFCN=9233
[ 24/449]: EARFCN 9234 Freq. 760.40 MHz looking for PSS
...
Found CELL ID 105. 25 PRB, 2 ports
[+] New cell detected [CellID/PCI-DL_freq  (105-9235)]
 Network type=4G
 PLMN=-1
 Band=28
 Downlink EARFCN=9235
[...]
^C[+] Cells save as cells_1595446203.json
```

The `g` parameters is not mandatory and is used mainly to select the right device to scan the Synchronization Signals.

To find the right device with Soapy, you can type the following command:

```
######################################################
##     Soapy SDR -- the SDR abstraction library     ##
######################################################

[INFO] [UHD] linux; GNU C++ version 9.2.1 20200304; Boost_107100; UHD_3.15.0.0-2build5
Found device 0
  driver = SpectranV6
  label = SpectranV6 RTSA HTTP Stream
  manufacturer = HB9FXQ
  product = SpectranV6 RTSA HTTP Stream
  serial = SPECTRAN-V6-00000000000

Found device 1
  backend = libusb
  device = 0x01:0x13
  driver = bladerf
  instance = 0
  label = BladeRF #0 [bd7fffbf..d5958b06]
  serial = bd7fffbf8efb4de4ba08d94bd5958b06
```

For NB-IoT scanning, you can use the `srslte_npss` option as follows:

```
$ sudo python modmobmap.py -m srslte_npss -b 20 -g 'soapy:id=1' # you need to precise the driver, and id of the device that way  
[INFO] [UHD] linux; GNU C++ version 9.2.1 20191008; Boost_106700; UHD_4.0.0.0-531-g5fb585c3
[INFO] [LOGGING] Fastpath logging disabled at runtime.

Found Rafael Micro R820T tuner
Found Rafael Micro R820T tuner
[INFO] Using format CF32.
[R82XX] PLL not locked!
[+] New cell detected [CellID/PCI-DL_freq  (1-6200)]
 Network type=4G
 PLMN=-1
 Downlink EARFCN=6200
[+] New cell detected [CellID/PCI-DL_freq  (1-6203)]
 Network type=4G
 PLMN=-1
 Downlink EARFCN=6203
[+] New cell detected [CellID/PCI-DL_freq  (446-6400)]
 Network type=4G
 PLMN=-1
 Downlink EARFCN=6400
[...]
```

Saving results
---------------

The process could be stopped at any time when killing the process with a keyboard interrupt signal. Then results will be automatically saved in a JSON file as follows:

```
[...]
^C[+] Cells save as cells_1528738901.json
```

## Docker image (in case of Apocalypse)

To avoid any issue installing the whole project, we have also a Docker container available at this address: https://hub.docker.com/r/penthertz/modmobmap

You can now use the `latest_with_e200` tag which is compatible with the ANTSDR E200.
