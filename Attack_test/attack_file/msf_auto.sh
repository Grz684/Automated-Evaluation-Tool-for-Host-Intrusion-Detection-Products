#!/bin/bash
export PATH="/opt/metasploit-framework/bin:$PATH"
/opt/metasploit-framework/bin/msfconsole -r msf_handler.rc &> connect_output.log

