ChatGPT suggestie, niet getest!

Hieronder staat de volledige configuratie om een unidirectionele MPLS-verbinding op te zetten tussen de machines PING en PONG, met een datadiode ertussen, en om Forward Error Correction (FEC) in te stellen op de verbinding met behulp van Reed-Solomon FEC, met een netwerkmasker van 255.255.255.0 (/24) en IP-adressen 10.0.0.1 voor PING en 10.0.0.2 voor PONG:

Installeer de nodige software: Voer de volgende opdracht uit om de benodigde software te installeren:
```
sudo apt-get install mpls-tools
```
Configureer de IP-adressen: Voer op beide machines de volgende opdrachten uit om IP-adressen te configureren voor de netwerkinterfaces die verbonden zijn met de datadiode:
Op de zendende machine PING:

```
ip addr add 10.0.0.1 dev eno4
ip link set eno4 up
```
Op de ontvangende machine PONG:
```
ip addr add 10.0.0.2 dev eno3
ip link set eno3 up
```
Configureer de MPLS-labels: Voer op beide machines de volgende opdrachten uit om de labels te configureren die zullen worden gebruikt in de MPLS-verbinding:
Op de zendende machine PING:
```
ip route add 10.0.0.2 via 10.0.0.1 dev eno4 mpls 1001
```
Op de ontvangende machine PONG:
```
ip route add 10.0.0.1 via 10.0.0.2 dev eno3 mpls 1002
```
Configureer de FEC-parameters: Voer op beide machines de volgende opdrachten uit om de FEC-parameters te configureren voor de MPLS-verbinding:
Op de zendende machine PING:
```
mpls ip route 10.0.0.2 255.255.255.0 10.0.0.1 fec-type rs interworking ip
```
Op de ontvangende machine PONG:
```
mpls ip route 10.0.0.1 255.255.255.0 10.0.0.2 fec-type rs interworking ip
```
Test de verbinding: Voer op de zendende machine PING de volgende opdracht uit om te testen of de verbinding correct is opgezet:
Op de ontvangende machine PONG:
```
nc -ul  10.0.0.2 12345
```
Op de zendende machine PING:
```
echo "hallo wereld" | nc -u 10.0.0.2 12345
```

Houd er rekening mee dat u de juiste IP-adressen en netwerkinterfaces moet opgeven voor uw specifieke omgeving.
