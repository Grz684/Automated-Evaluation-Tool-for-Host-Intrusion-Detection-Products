#!/bin/bash
export PATH="/opt/metasploit-framework/bin:$PATH"
/opt/metasploit-framework/bin/msfconsole -r msf_generate_payload.rc &> generate_payload_output.log