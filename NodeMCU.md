# NodeMCU

* Instalar ferramenta "esptool":

```shell
sudo pip install -U esptool
```

* Plugue o NodeMCU na USB

* Apague o NodeMCU:

```shell
sudo esptool.py --port /dev/ttyUSB0 erase_flash
```

* Faça download do firmware:

```shell
wget -c "http://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin"
```

* Escreva o firmware no dispositivo:

```shell
$ sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20180511-v1.9.4.binesptool.py v2.5.1

Serial port /dev/ttyUSB0
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
MAC: 2c:3a:e8:37:d8:a3
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Flash params set to 0x0040
Compressed 604872 bytes to 394893...
Wrote 604872 bytes (394893 compressed) at 0x00000000 in 9.0 seconds (effective 538.9 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

* Instale o pacote `picocom` para acessar o shell:

```
sudo apt-get install picocom
```

* Acesse o prompt:

```shell
sudo picocom /dev/ttyUSB0 -b115200
```

* No prompt, configure o Access Point com as credenciais (`nodemcu`, `_n0d3mcu`):

```shell
>>> import network
>>> ap_if = network.WLAN(network.AP_IF)
>>> ap_if.config(essid="nodemcu", authmode=network.AUTH_WPA_WPA2_PSK, password="_n0d3mcu")
```

* Com as mesmas credenciais, configure a shell web `WebREPL`:

```shell
>>> import webrepl_setup
WebREPL daemon auto-start status: disabled

Would you like to (E)nable or (D)isable it running on boot?
(Empty line to quit)
> E
Would you like to change WebREPL password? (y/n) y
New password (4-9 chars): _n0d3mcu
Confirm password: _n0d3mcu
Changes will be activated after reboot
Would you like to reboot now? (y/n) 
```

* Restarte o serviço `WebREPL` para obter o ip de conexão:

```shell
>>> import webrepl
>>> webrepl.stop()
>>> webrepl.start()
WebREPL daemon started on ws://192.168.4.1:8266
WebREPL daemon started on ws://172.20.19.237:8266
Started webrepl in normal mode
>>> 
```

* Baixe a interface para acessar e abra no browser:

```shell
wget -c "https://github.com/micropython/webrepl/archive/master.zip"
mv master.zip webrepl.zip
unzip webrepl.zip
rm webrepl.zip
mv webrepl-master/ webrepl
xdg-open webrepl/webrepl.html
```

* Conecte-se a rede Wi-fi `nodemcu`. Após isso, você conseguirá conectar na interface `WebREPL`.

* Configure os parâmetros no arquivos `nodemcu/main.py`

* Tendo configurado o arquivo, envie todos arquivos `.py` da pasta `nodemcu` para o dispositivo através da interface WebREPL