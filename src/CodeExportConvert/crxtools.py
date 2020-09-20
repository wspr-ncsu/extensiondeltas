import os
import zipfile
import json
import traceback

import jsmin

def do_load_json_buffer(buf, encoding="utf-8"):
	ret = None
	try:
		ret = json.loads(jsmin.jsmin(buf.decode(encoding)), strict=False)
	except json.JSONDecodeError:
		pass
	except UnicodeDecodeError:
		pass
	return ret

def load_json_buffer(buf):
	ret = do_load_json_buffer(buf)
	if not ret: # Try again with utf-8-sig.
		ret = do_load_json_buffer(buf, "utf-8-sig")
	return ret

def _open_zip_from_file(f):
	zipf = None
	try:
		zipf = zipfile.ZipFile(f, "r")
	except zipfile.BadZipFile:
		pass
	return zipf

def _read_zip_file(zipf, path):
	try:
		return zipf.read(path)
	except KeyError:
		pass
	return None

def get_extension_name(crx):
	zipf = _open_zip_from_file(crx)
	if not zipf:
		return None

	manifest_json = _read_zip_file(zipf, "manifest.json")
	if not manifest_json:
		return None

	manifest = load_json_buffer(manifest_json)
	if not manifest:
		return None

	try:
		name = manifest["name"]
	except KeyError:
		return None

	if name.startswith("__MSG_"):
		# Need to get locale-specific name.
		name_key = manifest["name"][len("__MSG_"):][:-2]
		name = None
		try:
			default_locale = manifest["default_locale"]

			messages_json = _read_zip_file(zipf,
					os.path.join("_locales", default_locale, "messages.json"))
			if not messages_json:
				return None

			messages = load_json_buffer(messages_json)
			if messages:
				for k in messages:
					# Looks like the name key is case insensitive.
					if k.lower() == name_key.lower():
						name_key = k
						break
				name = messages[name_key]["message"]
		except KeyError:
			pass

	return name

def get_extension_version(crx):
	zipf = _open_zip_from_file(crx)
	if not zipf:
		return None

	manifest_json = _read_zip_file(zipf, "manifest.json")
	if not manifest_json:
		return None

	manifest = load_json_buffer(manifest_json)
	if not manifest:
		return None

	try:
		return manifest["version"]
	except KeyError:
		pass
	return None
