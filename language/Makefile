.PHONY: po mo

po:
	xgettext -Lpython --output=messages.pot ../main.py
	msgmerge --update --no-fuzzy-matching --backup=off po/en.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/sv.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/fi.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/de.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/fr.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/es.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/it.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/nl.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/pt.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/da.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/is.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/no.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/et.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/lt.po messages.pot

mo:
	mkdir -p data/locales/en/LC_MESSAGES
	mkdir -p data/locales/sv/LC_MESSAGES
	mkdir -p data/locales/fi/LC_MESSAGES
	mkdir -p data/locales/de/LC_MESSAGES
	mkdir -p data/locales/fr/LC_MESSAGES
	mkdir -p data/locales/es/LC_MESSAGES
	mkdir -p data/locales/it/LC_MESSAGES
	mkdir -p data/locales/nl/LC_MESSAGES
	mkdir -p data/locales/pt/LC_MESSAGES
	mkdir -p data/locales/da/LC_MESSAGES
	mkdir -p data/locales/is/LC_MESSAGES
	mkdir -p data/locales/no/LC_MESSAGES
	mkdir -p data/locales/et/LC_MESSAGES
	mkdir -p data/locales/lt/LC_MESSAGES
	msgfmt -c -o data/locales/en/LC_MESSAGES/langapp.mo po/en.po
	msgfmt -c -o data/locales/sv/LC_MESSAGES/langapp.mo po/sv.po
	msgfmt -c -o data/locales/fi/LC_MESSAGES/langapp.mo po/fi.po
	msgfmt -c -o data/locales/de/LC_MESSAGES/langapp.mo po/de.po
	msgfmt -c -o data/locales/fr/LC_MESSAGES/langapp.mo po/fr.po
	msgfmt -c -o data/locales/es/LC_MESSAGES/langapp.mo po/es.po
	msgfmt -c -o data/locales/it/LC_MESSAGES/langapp.mo po/it.po
	msgfmt -c -o data/locales/nl/LC_MESSAGES/langapp.mo po/nl.po
	msgfmt -c -o data/locales/pt/LC_MESSAGES/langapp.mo po/pt.po
	msgfmt -c -o data/locales/da/LC_MESSAGES/langapp.mo po/da.po
	msgfmt -c -o data/locales/is/LC_MESSAGES/langapp.mo po/is.po
	msgfmt -c -o data/locales/no/LC_MESSAGES/langapp.mo po/no.po
	msgfmt -c -o data/locales/et/LC_MESSAGES/langapp.mo po/et.po
	msgfmt -c -o data/locales/lt/LC_MESSAGES/langapp.mo po/lt.po