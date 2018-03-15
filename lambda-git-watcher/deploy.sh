rm -f zappa_settings.json
envsubst < zappa_settings.json.tpl > zappa_settings.json
zappa deploy dev
zappa schedule dev