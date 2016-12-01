from django import template
# from apps.account.inc.id_sync import AESCipher

register = template.Library()

@register.filter(name='access')
def access(value, arg):
	if arg in value:
		return value[arg]
	else:
		return 0

def length():
	pass

# @register.filter(name='encrypt_raw')
# def encrypt_raw(value):
# 	encrypted_value = AESCipher.encrypt(value)
# 	return encrypted_value

# @register.filter(name='decrypt_value')
# def decrypt_value(value):
# 	decrypted_value = AESCipher.decrypt(value)
# 	return decrypted_value
	