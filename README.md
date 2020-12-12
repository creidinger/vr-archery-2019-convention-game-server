# vr-archery-2019-convention-game-server

## Hardware
- Windows pc
- raspberrypi
- VR Headset / trackers
- Barcode scanner

## Sofware
- Steam
- unity
- git
- python3

## PI setup
- Enable SSH
- Connect to wifi and copy ssh keys
```
ssh-copy-id pi@xxx.xxx.xxx.xxx
```
- Set player Environment variable in /etc/profile
```
sudo nano /etc/profile
```
Paste a player variable at the bottom of file... Ex:
```
export PLAYER="p1"
```
- Updated your ansible /inventories/hosts file with the IP addresses of your PIs
```
[pis]
10.0.0.66
10.0.0.71
```
- Navigate to ansible directory and run ansible
```
ansible-playbook -i inventories/hosts -u pi config_rpi.yml
```
