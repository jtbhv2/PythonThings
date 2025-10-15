import base64
def obfuscate_password(password):
    encoded_password = base64.b64encode(password.encode('utf-8'))
    return encoded_password.decode('utf-8')
def deobfuscate_password(obfuscated_password):
    decoded_password = base64.b64decode(obfuscated_password.encode('utf-8'))
    return decoded_password.decode('utf-8')
# Example usage
password = "P@ss.word1234!!"
obfuscated_password = obfuscate_password(password)
print("Obfuscated password:", obfuscated_password)
decoded_password = deobfuscate_password(obfuscated_password)
print("Decoded password:", decoded_password)