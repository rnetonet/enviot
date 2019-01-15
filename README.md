# Roteiro - Implantação MATE84 - Projeto EnvIOT

## Pré-requisitos

Em todas máquinas envolvidas, você precisará do Python 3 e do `pip` instalado ([https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)).


## Coleta

Foram utilizados dois dispositivos de coleta durante o semestre de 2018.2. 

Inicialmente, uma placa NodeMCU, cuja documentação de setup pode ser vista em [NodeMCU](NodeMCU.md).

Contudo, oficialmente, optou-se por utilizar o dispositivo **SonOFF**, cujo setup detalharemos a seguir.


## Middleware - FOG

* Instale o `MongoDB`, siga as instruções em [https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

* Inicie o servidor MongoDB

```
service mongod start
```

* Instale o `mosquitto`:

```
sudo apt-get install mosquitto mosquitto-clients
```

* Crie um arquivo de configuração padrão para o mosquitto:

```
root@localhost:/opt/enviot# vim /etc/mosquitto/conf.d/default.conf 
```

Com o conteúdo:

```
listener 1883 0.0.0.0
```

* Reinicie o serviço do mosquitto:

```
service mosquitto restart
```

* Faça uma cópia do projeto `enviot` em `/opt/`. Use `git` ou `scp`

```
$/opt/enviot# ls
application  middleware  perception  README.md  requirements.txt
```

> Certifique-se que você executará os próximos passos estando na pasta `/opt/enviot`

* Instale o `pip`:

```
apt-get install python3-minimal python3-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

* Instale os requisitos do `enviot`:

```
pip install -r requirements.txt 
```

* Parametrize corretamente o arquivo `middleware.ini`, dentro da pasta `middleware`

* Inicie o serviço do `middleware` em *background*:

```
root@localhost:/opt/enviot# pwd
/opt/enviot

root@localhost:/opt/enviot# nohup python3 middleware/middleware.py &
[1] 7140
```

* Cada um dos plugins irá produzir um arquivo `nome.log`, são dois plugins principais. Um de armazenamento local e coleta com o sonoff, `sonoff` e outro de sincronização com a nuvem, `cloud_sync`.

## Camada de Aplicação - Nuvem

* Instale o `MongoDB`, siga as instruções em [https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

* Inicie o servidor MongoDB

* Faça uma cópia do projeto `enviot` em `/opt/`. Use `git` ou `scp`

```
$/opt/enviot# ls
application  middleware  perception  README.md  requirements.txt
```

> Certifique-se que você executará os próximos passos estando na pasta `/opt/enviot`

* Instale o `pip`:

```
apt-get install python3-minimal python3-dev
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

* Instale os requisitos do `enviot`:

```
pip install -r requirements.txt 
```

* Parametrize o arquivo `web/web.ini`

* Realizados os passos, o último passo de execução,  dentro da pasta `/opt/enviot`:

```
nohup python3 application/web/web.py &
```

* Será disponibilizado uma interface gráfica no ip `0.0.0.0` (`localhost` e o ip público da máquina), na porta `80`.

## SonOFF

O SonOFF deve ser configurado realizando os passos descritos na página `13` da documentação [PlataformaSOFT-IoT](PlataformaSOFT-IoT.pdf).

- O nome do device deve ser o mesmo parametrizado no *middleware*. 
- O servidor MQTT deverá ser o IP do *middleware*.
- O servidor MQTT dispensa login e senha.

Verifique o início da coleta analisando os logs do *middleare* e do *application*.


