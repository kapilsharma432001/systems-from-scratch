## Authentication
- This is one of the most important topic in the interviews. Interviewers often start with a simple question like: JWT vs sessions and then they go deeper for different topics like: cookies, CSRF, refresh-token rotation, logout, scaling and security etc.

#### What happens during normal username/password authentication?
- Suppose the user registers as:-
email: kapil@example.com
password: hello123

- Now we should never store the password directly. Instead: **password -> password hashing algorithm -> hash -> Database**

##### Difference between hashing and encryption
- Encryption is reversible and hashing is one-way.
- In case of encryption, if we have the key - we can decrypt easily. Like plaintext -> encrypt (key) -> ciphertext -> decypt(key) -> plaintext
- Passwords shouldn't be encrypted because if key leaks, all passwords become recoverable.