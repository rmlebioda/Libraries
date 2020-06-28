
def copy_cb(obj):
	import pyperclip
	import jsonpickle
	pyperclip.copy(jsonpickle.encode(obj))
