#!/usr/bin/env python3

import requests
import subprocess
import json
import argparse
import re
import concurrent.futures
import logging
from typing import List, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_subdomains(domain: str, api_key: str) -> List[str]:
    url = f"https://api.dnsdumpster.com/domain/{domain}"
    headers = {
        "X-API-Key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [entry.get("host") for entry in data.get("a", []) if entry.get("host")]
    except requests.exceptions.RequestException as e:
        logging.error(f"[ERROR] Errore durante la richiesta per {domain}: {e}")
        return []


def scan_ports(subdomain: str) -> str:
    command = ["nmap", "-T4", "-F", "-Pn", "-sV", subdomain]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"[ERROR] Errore nella scansione di {subdomain}: {e}")
        return ""


def format_scan_result(scan_result: str) -> Optional[str]:
    open_ports = re.findall(r'(\d+/tcp)\s+open\s+(.+)', scan_result)
    if open_ports:
        formatted_result = ""
        for port, service in open_ports:
            port_number = port.split('/')[0]
            formatted_result += f"> {port_number} - {service}\n"
        return formatted_result
    return None


def write_to_file(filename: str, content: str) -> None:
    with open(filename, "a") as file:
        file.write(content)
        file.write("\n" + "=" * 40 + "\n")


def scan_subdomains_in_parallel(domain: str, subdomains: List[str], output_filename: str, no_ports_filename: str) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scan_ports, subdomain): subdomain for subdomain in subdomains}

        for future in concurrent.futures.as_completed(futures):
            subdomain = futures[future]
            try:
                scan_result = future.result()
                formatted_result = format_scan_result(scan_result)
                if formatted_result:
                    write_to_file(output_filename, f"{subdomain}\n{formatted_result}")
                    logging.info(f"[SUCCESS] Scansione completata per {subdomain}")
                else:
                    write_to_file(no_ports_filename, f"{subdomain}\n")
                    logging.info(f"[INFO] Nessuna porta aperta per {subdomain}")
            except Exception as e:
                logging.error(f"[ERROR] Errore durante la scansione di {subdomain}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Scansiona le porte dei sottodomini di un dominio.")
    parser.add_argument("domain", help="Il dominio da scansionare (esempio: dominio.com)")
    args = parser.parse_args()

    domain = args.domain
    api_key = "APIKEY dnsdumpster"

    subdomains = get_subdomains(domain, api_key)

    if subdomains:
        logging.info(f"Trovati {len(subdomains)} sottodomini per {domain}.")

        output_filename = f"{domain}_scan_results.txt"
        no_ports_filename = f"{domain}_no_ports.txt"

        write_to_file(output_filename, f"{domain} - Sottodomini con porte aperte\n")
        write_to_file(no_ports_filename, f"{domain} - Sottodomini senza porte aperte\n")

        # scansioni in parallelo
        scan_subdomains_in_parallel(domain, subdomains, output_filename, no_ports_filename)
    else:
        logging.error(f"[ERROR] Nessun sottodominio trovato per {domain}.")


if __name__ == "__main__":
    main()
