# 📡 Modmobmap

<div align="center">

**Mobile Network Intelligence & Mapping Tool**

*Retrieve comprehensive information on 2G/3G/4G/5G cellular networks with minimal equipment*

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-BEER--WARE-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Available-2496ED?logo=docker)](https://hub.docker.com/r/penthertz/modmobmap)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)](https://www.linux.org/)

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-usage-examples) • [Docker](#-docker-deployment)

</div>

---

## 🎯 Overview

Modmobmap is a comprehensive cellular network reconnaissance tool designed for security researchers, RF engineers, and penetration testers. Originally presented at [BeeRump 2018](https://www.rump.beer/2018/slides/modmobmap.pdf), it combines multiple techniques to map and analyze mobile networks using both commercial smartphones and Software-Defined Radio (SDR) devices.

### 🔥 Key Features

<table>
<tr>
<td>

**📱 Smartphone-Based Scanning**
- Samsung Galaxy devices (S3-S20)
- ServiceMode interface support
- XGold modem compatibility
- Real-time cell information

</td>
<td>

**📻 SDR Integration**
- GNU Radio GSM scanning
- srsRAN LTE/NB-IoT support
- Multi-band analysis
- Passive reconnaissance

</td>
</tr>
<tr>
<td>

**🌐 Network Coverage**
- 2G/GSM networks
- 3G/UMTS systems
- 4G/LTE cells
- NB-IoT detection

</td>
<td>

**💾 Data Management**
- JSON export format
- Real-time logging
- Cell database
- Operator caching

</td>
</tr>
</table>

---

## 🛠️ Supported Hardware

### 📱 Mobile Devices (Rooted Required)

<details>
<summary><b>✅ Tested & Confirmed</b></summary>

- **Samsung Galaxy S3** (via [xgoldmon](https://github.com/FlUxIuS/xgoldmon))
- **Samsung Galaxy S4** (GT-I9500)
- **Samsung Galaxy S5**
- **Samsung Galaxy Note 2** (LTE version)
- **Samsung Galaxy S20**
- **Samsung Galaxy Nexus** (GT-I9250, rooted)
- **Samsung Galaxy S2** (GT-I9100)

> 💡 **Note:** All devices must be rooted. For non-rooted devices, manual DFR technique required.

</details>

### 📻 SDR Devices (via gr-osmosdr & UHD)

<details>
<summary><b>🎛️ Compatible SDR Hardware</b></summary>

| Device | Driver | GSM | LTE | Notes |
|--------|--------|-----|-----|-------|
| **RTL-SDR** | rtlsdr/soapy | ✅ | ✅ | Budget option |
| **HackRF One** | hackrf | ✅ | ✅ | Wide frequency range |
| **BladeRF** | bladerf | ✅ | ✅ | High performance |
| **USRP (all models)** | uhd | ✅ | ✅ | Professional grade |
| **ANTSDR E200** | uhd | ✅ | ✅ | Requires proper UHD setup |
| **AirSpy** | airspy | ✅ | ❌ | GSM only |
| **SDRplay RSP** | sdrplay | ✅ | ❌ | GSM only |
| **FunCube Dongle** | fcd | ✅ | ❌ | GSM only |

</details>

---

## 🚀 Installation

### Prerequisites

```bash
# Core dependencies
- Python 3.x
- Android SDK (for ADB)
- GNU Radio 3.10+ with gr-gsm
- Valid/invalid SIM card (for IMSI)
```

### 🐧 Ubuntu 24.04 Quick Install

```bash
# Clone repository with submodules
git clone --recursive https://github.com/FlUxIuS/modmobmap.git
cd modmobmap

# Run automated installation script
sudo ./install_all-Ubuntu_24.04.sh

# Update submodules (if needed)
git submodule update --init --recursive --remote
```

### 🔧 Manual Installation

<details>
<summary><b>Click to expand manual installation steps</b></summary>

```bash
# 1. Install Python dependencies
pip3 install -r requirements.txt

# 2. Install Android SDK
# Download from: https://developer.android.com/studio/#downloads
export ANDROID_SDK_ROOT=/path/to/android-sdk

# 3. Install GNU Radio & gr-gsm
sudo apt-get install gnuradio gr-gsm

# 4. Build srsRAN (for LTE scanning)
cd thirdparty/srsLTE
mkdir build && cd build
cmake ../
make -j$(nproc)
sudo make install
```

</details>

---

## 🎯 Quick Start

### 🔰 Basic Scanning (Smartphone)

```bash
# Auto-detect operators and scan all available networks
sudo python3 modmobmap.py

# Specify Android SDK location (if not in default path)
sudo python3 modmobmap.py -s /opt/Android/sdk
```

**Expected Output:**
```
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 2 operator(s)
{'20810': 'F SFR', '20820': 'F-Bouygues Telecom'}

[+] New cell detected [CellID/PCI-DL_freq (4XXX-81)]
 Network type=2G
 PLMN=208-10
 ARFCN=81

[+] New cell detected [CellID/PCI-DL_freq (3XX-6300)]
 Network type=4G
 PLMN=208-10
 Band=20
 Downlink EARFCN=6300
```

### ⚡ Speed Up Scanning (Cached Operators)

Create `cache/operators.json`:
```json
{
    "20801": "Orange",
    "20810": "F SFR",
    "20815": "Free",
    "20820": "F-Bouygues Telecom"
}
```

Run with cache:
```bash
sudo python3 modmobmap.py -o
```

### 🎯 Target Specific Operators

```bash
# Focus on Orange (MCC/MNC: 20801)
sudo python3 modmobmap.py -n 20801

# Multiple operators
sudo python3 modmobmap.py -n 20801,20810,20815
```

> 📚 **MCC/MNC Lookup:** [Wikipedia Mobile Country Codes](https://en.wikipedia.org/wiki/Mobile_country_code)

---

## 📖 Usage Examples

### 🔵 Method 1: ServiceMode (Samsung Devices)

The default and most straightforward method:

```bash
sudo python3 modmobmap.py -m servicemode
```

### 🟢 Method 2: XGoldmon (XGold Modems)

For devices with XGold chipsets (S3, S4, Nexus):

**Terminal 1 - Start xgoldmon:**
```bash
cd /path/to/xgoldmon
sudo ./xgoldmon -t s3 -m /dev/ttyACM1
# Creates celllog.fifo
```

**Terminal 2 - Run Modmobmap:**
```bash
sudo python3 modmobmap.py \
    -f /path/to/xgoldmon/celllog.fifo \
    -m xgoldmod \
    -a /dev/ttyACM0 \
    -o
```

### 🟡 Method 3: GSM Scanning (SDR - gr-gsm)

Scan GSM bands with Software-Defined Radio:

```bash
# RTL-SDR scanning GSM-R and GSM900
python3 modmobmap.py -m grgsm -b GSM-R,GSM900 -g rtlsdr

# BladeRF scanning multiple bands
python3 modmobmap.py -m grgsm -b GSM850,GSM900,DCS1800 -g bladerf

# HackRF with custom gain
python3 modmobmap.py -m grgsm -b GSM900 -g "driver=hackrf,gain=40"
```

**Available GSM Bands:**
- `GSM850` (824-849 MHz)
- `GSM-R` (876-880 MHz, Railway)
- `GSM900` (890-915 MHz)
- `DCS1800` (1710-1785 MHz)
- `PCS1900` (1850-1910 MHz)

### 🔴 Method 4: LTE Scanning (SDR - srsRAN)

Scan LTE cells using srsRAN:

```bash
# USRP scanning LTE Band 28
python3 modmobmap.py -m srslte_pss -b 28 -g 'driver=usrp'

# BladeRF scanning Band 7
python3 modmobmap.py -m srslte_pss -b 7 -g 'driver=bladerf'

# RTL-SDR via Soapy (specify device ID!)
python3 modmobmap.py -m srslte_pss -b 20 -g 'soapy:id=1'

# Multiple bands
python3 modmobmap.py -m srslte_pss -b 3,7,20,28 -g 'driver=usrp'
```

### 🟣 Method 5: NB-IoT Scanning

Detect Narrowband IoT cells:

```bash
sudo python3 modmobmap.py -m srslte_npss -b 20 -g 'soapy:id=1'
```

---

## 🔍 Finding Your SDR Device

### List Soapy Devices
```bash
SoapySDRUtil --find
```

**Example Output:**
```
Found device 0
  driver = rtlsdr
  label = Generic RTL2832U OEM :: 00000001
  serial = 00000001

Found device 1
  driver = bladerf
  label = BladeRF #0 [bd7fffbf..d5958b06]
  serial = bd7fffbf8efb4de4ba08d94bd5958b06
```

### List UHD Devices
```bash
uhd_find_devices
```

---

## 💾 Data Export

Results are automatically saved when you stop the scan (`Ctrl+C`):

```bash
[+] Cells save as cells_1595446203.json
```

### JSON Output Format

```json
{
  "3XX-6300": {
    "PLMN": "208-10",
    "band": 20,
    "bandwidth": "10MHz",
    "eARFCN": 6300,
    "PCI": "3XX",
    "TAC": "XXXX",
    "type": "4G"
  }
}
```

---

## 🐳 Docker Deployment

### Pre-built Image (Recommended)

```bash
# Pull latest image
docker pull penthertz/modmobmap:latest_with_e200

# Run with device access
docker run -it --privileged \
  -v /dev/bus/usb:/dev/bus/usb \
  penthertz/modmobmap:latest_with_e200 \
  python3 modmobmap.py -m grgsm -b GSM900 -g rtlsdr
```

### Build Your Own

```bash
# Clone and build
git clone --recursive https://github.com/FlUxIuS/modmobmap.git
cd modmobmap
docker build -t modmobmap:local .

# Run
docker run -it --privileged -v /dev:/dev modmobmap:local
```

> 🔐 **Security Note:** `--privileged` flag required for USB/hardware access

---

## 📊 Command Reference

```bash
python3 modmobmap.py [OPTIONS]

Required Options:
  -m, --module MODULE       Scanning module: servicemode|xgoldmod|grgsm|srslte_pss|srslte_npss
  
Optional Parameters:
  -n, --networks NETWORKS   Target MCC/MNC codes (comma-separated)
  -o, --cached_operator     Use cached operators for faster scanning
  -s, --sdk PATH           Android SDK path (default: auto-detect)
  -a, --at DEVICE          AT serial device (e.g., /dev/ttyUSB0)
  -f, --file FILE          FIFO file for xgoldmon integration
  -b, --bands BANDS        Frequency bands to scan (SDR modes)
  -g, --args ARGS          SDR device arguments (driver, gain, etc.)

Examples:
  # Basic smartphone scan
  sudo python3 modmobmap.py
  
  # GSM scan with RTL-SDR
  python3 modmobmap.py -m grgsm -b GSM900 -g rtlsdr
  
  # LTE scan targeting Band 7
  python3 modmobmap.py -m srslte_pss -b 7 -g 'driver=usrp'
  
  # Cached operators, specific network
  sudo python3 modmobmap.py -n 20810 -o
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Bug Reports:** Open an issue with details
- 🔧 **Device Support:** Add parsers for new phones
- 📡 **SDR Engines:** Integrate new hardware/software
- 📚 **Documentation:** Improve guides and examples

---

## 📞 Support & Community

- 🐦 **Twitter:** [@Penthertz](https://twitter.com/penthertz)
- 🌐 **Website:** [penthertz.com](https://www.penthertz.com)

---

## 📜 License

```
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<sebastien.dudek(@)penthertz.com> wrote this file. As long as you retain 
this notice you can do whatever you want with this stuff. If we meet some 
day, and you think this stuff is worth it, you can buy me a beer in return.
                                                            FlUxIuS ;)
----------------------------------------------------------------------------
```

---

## 🙏 Acknowledgments

- Original presentation: [BeeRump 2018](https://www.rump.beer/2018/slides/modmobmap.pdf)
- [gr-gsm](https://github.com/ptrkrysik/gr-gsm) by Piotr Krysik
- [srsRAN](https://github.com/srsran/srsRAN) by Software Radio Systems
- [xgoldmon](https://github.com/2b-as/xgoldmon) by 2b-as

---

<div align="center">

**Made with ☕ & 📡 by the Penthertz Team**

⭐ Star us on GitHub if this project helped you!

</div>
