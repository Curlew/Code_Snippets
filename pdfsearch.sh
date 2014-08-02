#!/bin/bash
## Öffnen eines XFCE-Terminals, falls nicht aus Konsole gestartet
tty -s; if [ $? -ne 0 ]; then xfce4-terminal -e "$0"; exit; fi
PROGNAME="PDF-Search"
CREATOR="by Martin Jung"
COPYRIGHT="(c) 2011 - Marburg"
## Kleines Bash-Script, welches rekursiv alle Unterordner und Dateien
## anhand eines Suchbegriffes durchsucht und hinterher die Option gibt
## gefundene Suchergebnisse mit einem PDF-Reader zu öffnen.
#####################################################################
##### Variablen #####
SEARCHDIR=$(pwd)		# im aktuellen Ordner starten
SAVEFILE="output.log"		# Der Name temporärer LOG-Datei
PDFREADER="/usr/bin/evince"	# PDF-Reader
DIVIDER="--------------------------------------------------"
################## Hier nichts mehr ändern ##########################
##### Beginn #####
clear
echo $PROGNAME $CREATOR | grep --color $PROGNAME
echo $COPYRIGHT
echo $DIVIDER
# Einlesen von alternativen Startordner für Rekursive Suche und Suchmuster	
echo "Standard:		$SEARCHDIR" 	 | grep --color "$SEARCHDIR"
echo "OK:			ENTER"
echo "Ändern:			/path/to/directory"
read INPUT			
	if [ "$INPUT" != "" ]; then	
		SEARCHDIR="$INPUT"
		echo "Suche in $SEARCHDIR nach...?" | grep --color "$SEARCHDIR"
	else
		echo "Suche nach...?"
	fi
read SEARCHSTRING
echo $DIVIDER
echo "Suche rekursiv nach $SEARCHSTRING durch `ls -R | wc -l` Dateien im Ordner $SEARCHDIR"	| grep --color -e "$SEARCHSTRING" -e "$SEARCHDIR"
echo $DIVIDER
export GREP_COLOR="31"
########################## Suchbefehl #####################
find $SEARCHDIR -type f -print 2>/dev/null | grep -i $SEARCHSTRING --exclude=$SAVEFILE | tee $SAVEFILE | grep -i --color $SEARCHSTRING
########################## Suchbefehl #####################
# Anzeige der gefundenen Dateien
echo $DIVIDER
export GREP_COLOR="01;31"			# fett, rot
echo "Suche beendet"
echo "\"$SEARCHSTRING\" insgesamt `cat $SAVEFILE | wc -l`-mal gefunden" | grep --color "$SEARCHSTRING"
# Anzeige aller Ergebnisse
COUNTER=0
              while read -r x
              do
		COUNTER=$(( $COUNTER + 1 ))
                printf "%s\n" "$x" | sed -e "s#$SEARCHDIR#[$COUNTER]: #g" | grep --color "$SEARCHSTRING"
              done < $SAVEFILE
# Öffnen einer PDF anhand einer Nummer
echo "Geben Sie die Nummer der zuöffnenden PDF-Datei ein:"
read CHOICE
	if [ "$CHOICE" != "" ]; then
		FILE=`sed -n $CHOICE"p" $SAVEFILE | sed -e 's#\ #\\\ #g'`
		echo $FILE 
		file $FILE
		# Outsourcing des Startprozesses des PDF-Readers mit der zuöffnenden Datei
		$PDFREADER $FILE &
	else
		echo "Keine PDF geöffnet. Programm wird beendet"
	fi
# Löschen der Logs und Schließen des Programmes
rm $SAVEFILE
exit

