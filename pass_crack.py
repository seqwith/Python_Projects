import hashlib

flag = 0

# Get the hashed file name
pass_hash = input("md5 hash: ")

# Get the dictonary file with your list of passwords
wordlist = input("File Name: ")

# Open the dictonary file
try:
    pass_file = open(wordlist, 'r')
except:
    print("No file found")
    quit()

# Attempt to find a matching password in the hash and wordlist
for word in pass_file:
    enc_word = word.encode('utf-8')
    digest = hashlib.md5(enc_word.strip()).hexdigest()
    #print(word)
    #print(digest)
    #print(pass_hash)
    if digest.strip == pass_hash.strip():
        print("PASSWORD FOUND")
        print("Password is: " + word)
        flag = 1
        break
if flag == 0:
    print("Password is not in list")