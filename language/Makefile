.PHONY: po mo

po:
	xgettext -Lpython --output=messages.pot ../main.py
	msgmerge --update --no-fuzzy-matching --backup=off po/en.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/sv.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/fi.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/de.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/fr.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/es.po messages.pot

mo:
	mkdir -p data/locales/en/LC_MESSAGES
	mkdir -p data/locales/sv/LC_MESSAGES
	mkdir -p data/locales/fi/LC_MESSAGES
	mkdir -p data/locales/de/LC_MESSAGES
	mkdir -p data/locales/fr/LC_MESSAGES
	mkdir -p data/locales/es/LC_MESSAGES
	msgfmt -c -o data/locales/en/LC_MESSAGES/langapp.mo po/en.po
	msgfmt -c -o data/locales/sv/LC_MESSAGES/langapp.mo po/sv.po
	msgfmt -c -o data/locales/fi/LC_MESSAGES/langapp.mo po/fi.po
	msgfmt -c -o data/locales/de/LC_MESSAGES/langapp.mo po/de.po
	msgfmt -c -o data/locales/fr/LC_MESSAGES/langapp.mo po/fr.po
	msgfmt -c -o data/locales/es/LC_MESSAGES/langapp.mo po/es.po
