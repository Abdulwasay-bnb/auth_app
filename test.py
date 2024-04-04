import bcrypt

# Password to Hash
my_password = 'admin1234'.encode('utf-8')

# Generating Salt
salt = bcrypt.gensalt()

print('salt', salt)
# Hashing Password
hash_password = bcrypt.hashpw(
    password=my_password,
    salt=b'$2b$12$z3sRi9j2aoaaf6oREVbhcO'
)

print(f"Actual Password: {my_password.decode('utf-8')}")
# Print Hashed Password
print(f"Hashed Password: {hash_password.decode('utf-8')}")


if bcrypt.checkpw(my_password, hash_password) == True:
    print('AUTHHHHHHHHHHHHHHHH')