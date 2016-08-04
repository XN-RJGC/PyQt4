#! /bin/sh

if test $# -ne 2
then
	echo "[error]:input two path params!"
else
	python /opt/PyQt-x11-gpl-4.11.4/pyuic/uic/pyuic.py -o $1 $2
	if $? -ne 0
	then
		echo "execute successfully!"
	fi
fi
