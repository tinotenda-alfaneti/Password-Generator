import pyttsx3
import random
# module for encrypting
from cryptography.fernet import Fernet
#module for speech recognition
import speech_recognition as sr

Letters = []
Numbers = []
Special_characters = []
password = ""
# these lines below are to generate the key for encrypting and that is the one supposed to be used for decrypted
key = Fernet.generate_key()
encrypter = Fernet(key)
#

# defining the function for generating password with the arguments name of the user and site the password is for.
def passwordGen(name, site):
    global e_password
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak anything: ")
        audio = r.listen(source)

        text = r.recognize_google(audio, language='en-UK')
        best_phrase = ("{}".format(text))
        print(best_phrase)


    lucky_number = input("Enter numbers 0-9: ")
    special_characters = input("Enter at least 5 special characters: ")
    # Here is where the password is spiced. Using the random data from the user, 3 lists are created
    # From the lists, the code randomly picks anything in the list to come up with the string by concatenating the choices
    # the code also checks to remove spaces as characters and making sure the string in lucky_number contains numeral only
    for letter in best_phrase:
        if letter != " ":
            Letters.append(letter)
    for number in lucky_number:
        if number.isnumeric():
            Numbers.append(number)
    for character in special_characters:
        Special_characters.append(character)
    password = "{}{}{}{}{}{}{}{}".format(random.choice(Letters).upper(), random.choice(Numbers),
                                         random.choice(Letters).lower(), random.choice(Numbers),
                                         random.choice(Letters).upper(), random.choice(Special_characters),
                                         random.choice(Letters).lower(), random.choice(Special_characters))
    # the statements below are for writing the password on a file
    f = open("Passwords.txt", "w")
    f.write(password + " : " + site)
    # this stage is when the password is encypted in order to keep the password safe.
    # the encrypted password is also printed to the screen in string form
    e_password = encrypter.encrypt(password.encode())
    print("\n" + str(e_password, "utf8"))
    new = open("hiddenPassword.txt", "w")
    new.write("\n\n" + str(e_password, "utf8") + " : " + site)
    new.close()
    f.close()
    say = "\n\nHi " + name + "\nYour password for " + site + " is " + password + "\nIt's in " + f.name
    # Saying the owner of the password, the site for the password, the password and where it is stored.
    # Some few tips also on password safety.
    engine = pyttsx3.init()
    engine.say(say)
    engine.say(
        "Keep your password safe. Make sure you delete the password in Passwords.txt. Just keep the encrypted one.")
    engine.setProperty("rate", 10)  # voice speed
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.runAndWait()
    return say


def decrypt():
    global e_password
    decrypted = encrypter.decrypt(e_password)
    # print(str(decrypted, "utf8"))
    encrypted = open("decrypted_password.txt", "w")
    encrypted.write(str(decrypted, "utf8"))
    encrypted.close()
    read = open("decrypted_password.txt", "r")
    print(read.read())


passwordGen("Rodney", "Blockchain Account")
decrypt()