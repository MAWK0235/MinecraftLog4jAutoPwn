![image](https://github.com/MAWK0235/MinecraftLog4jAutoPwn/assets/90433993/8e88e5d8-9000-4e56-8c51-4bfb4bb941c6)

# MinecraftLog4jAutopwn: Automate Minecraft Server Exploitation with Log4j

Are you tired of manually exploiting Minecraft servers using Log4j vulnerabilities? Say no more! Introducing MinecraftLog4jAutopwn – your ultimate tool for automating the exploitation process, saving you time and effort. With MinecraftLog4jAutopwn, effortlessly exploit Minecraft servers with Log4j vulnerabilities and gain access efficiently!

note: you might need to change the java compiler version if the server was compiled with a different version then my example

## Key Features

- **Automated Exploitation**: MinecraftLog4jAutopwn automates the entire process of exploiting Minecraft servers with Log4j vulnerabilities, streamlining your workflow and saving valuable time.

- **HTTP and LDAP Server Setup**: Automatically sets up HTTP and LDAP servers for delivering payloads to the target Minecraft server.

- **Payload Injection**: Inject payloads into Minecraft servers seamlessly, with support for both Linux and Windows targets.

- **Flexible Authentication**: Support for authenticating with Minecraft servers using usernames and passwords.

## Installation

```bash
git clone https://github.com/yourusername/MinecraftLog4jAutopwn.git

```

## Usage

```bash
python MinecraftLog4jAutopwn.py --target <target_IP> --username <minecraft_username> --LHOST <your_IP>
```

## Command Line Arguments

- `--target`: Specify the IP address of the target Minecraft server.
- `--username`: Provide the username for authenticating with the Minecraft server.
- `--LHOST`: Specify the IP address of your machine where payloads will be delivered.

## Examples

```bash
# Exploit a Minecraft server with Log4j vulnerability
python MinecraftLog4jAutopwn.py --target 192.168.1.1 --username user --password pass --LHOST 10.0.0.1
```

## Response Codes

- **Success**: Successfully exploited the Minecraft server.
- **Authentication Failed**: Failed to authenticate with the Minecraft server.
- **Connection Error**: Couldn't connect to the Minecraft server.

![MinecraftLog4jAutopwn](minecraft_log4j_autopwn_image.png)

*Note: Replace `yourusername` in the installation command with your GitHub username.*
