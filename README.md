# Domain-Subdomain Port Scanner

This script was developed to meet the need of obtaining a list of active subdomains for a given domain and quickly identifying open ports on them. 
This helps in performing daily checks to ensure that everything is functioning correctly.


### Main Features
- **Subdomain Detection**: Uses the [DNSDumpster](https://dnsdumpster.com/) API to get a list of subdomains associated with a domain.
- **Port Scanning**: Performs a scan of open ports on each subdomain using [Nmap](https://nmap.org/).
- **Service Identification**: Identifies active services on each open port using Nmap.
- **Saving Results**: Saves the scan results into two separate text files: one for subdomains with open ports and one for those without.

---

## Requirements

- **Python 3.x**: The script is written in Python 3. Make sure you have Python 3 installed on your system.
- **Nmap**: The script uses the Nmap tool to perform the port scan. Nmap must be installed locally.

### Installing Nmap

- On **Ubuntu** or other Debian-based Linux distributions:
  ```bash
  sudo apt-get install nmap
  ```
- On **Windows** :
  ```bash
  pip install python-nmap
  ```
  
## How to Use the Script

### 1. Configure the DNSDumpster API Key
The script uses the DNSDumpster API to get a list of subdomains for a domain. You must sign up at [DNSDumpster](https://dnsdumpster.com/) to obtain an API key.

Once you have the key, replace the value of `api_key` in the code with your API key

```python
api_key = "YOUR_API_KEY"
```
### 2. Run the Script
To run the script, open the terminal and use the following command, replacing <domain> with the domain you want to scan (for example, example.com):

```python
python3 domain_scanner.py <domain>
```

### 3. Expected Results
After the scan is completed, the script will generate two output files:

### Example of a `domain_scan_results.txt` file:

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
### Example of a `domain_no_ports.txt` file:

```python
sub3.example.com
==================================================
```
