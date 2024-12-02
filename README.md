# Domain-Subdomain Port Scanner

Questo script Python effettua la scansione dei sottodomini di un dominio specificato, raccogliendo informazioni sulle porte aperte e sui servizi attivi su ciascun sottodominio.

### Funzionalità principali
- **Rilevamento dei sottodomini**: Utilizza l'API di [DNSDumpster](https://dnsdumpster.com/) per ottenere una lista di sottodomini associati a un dominio.
- **Scansione delle porte**: Esegui una scansione delle porte aperte su ciascun sottodominio utilizzando [Nmap](https://nmap.org/).
- **Identificazione dei servizi**: Identifica i servizi attivi su ciascuna porta aperta utilizzando Nmap.
- **Salvataggio dei risultati**: Salva i risultati della scansione in due file di testo separati: uno per i sottodomini con porte aperte e uno per quelli senza.

---

## Requisiti

- **Python 3.x**: Lo script è scritto in Python 3. Assicurati di avere Python 3 installato sul tuo sistema.
- **Nmap**: Lo script utilizza il tool Nmap per eseguire la scansione delle porte. Nmap deve essere installato localmente.

### Installazione di Nmap

- Su **Ubuntu** o altre distribuzioni Linux basate su Debian:
  ```bash
  sudo apt-get install nmap
  ```
- Su **Windows** o altre distribuzioni Linux basate su Debian:
  ```bash
  pip install python-nmap
  ```
## Come utilizzare lo script

### 1. Configurare la chiave API di DNSDumpster
Lo script utilizza l'API di DNSDumpster per ottenere una lista di sottodomini per un dominio. Devi registrarti su [DNSDumpster](https://dnsdumpster.com/) per ottenere una chiave API.

Una volta ottenuta la chiave, sostituisci il valore di `api_key` nel codice con la tua chiave API:

```python
api_key = "YOUR_API_KEY"
```
### 2. Esegui lo script
Per eseguire lo script, apri il terminale e utilizza il seguente comando, sostituendo <dominio> con il dominio che desideri scansionare (ad esempio, example.com):

```python
python3 domain_scanner.py <dominio>
```

### 3. Risultati attesi
Dopo che la scansione è stata completata, lo script genererà due file di output:
### Esempio di un file `domain_scan_results.txt`:

```python
example.com - Sottodomini con porte aperte
==================================================
sub1.example.com
>80 - http     Apache httpd
>443 - ssl/http Nginx

sub2.example.com
>21 - ftp      vsftpd 2.0.8 or later
>80 - http     Apache httpd
==================================================
```
### Esempio di un file `domain_no_ports.txt`:

```python
sub3.example.com
==================================================
```
