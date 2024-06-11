#!/usr/bin/env make
#
# cgi-bin - CGI demonstration code

# Makefile tool environment
#
SHELL= bash
SED= sed
SORT= sort
FMT= fmt
INSTALL= install
LN= ln
BASENAME= basename
CMP= cmp
CHOWN= chown
CHMOD= chmod
MV= mv
CP= cp
RM= rm
ID= id

HTML_USER= chongo
HTML_GROUP= html

CGI_USER= cgi
CGI_GROUP= cgi

# where the web pages reside
#
DOCROOT= /home/www/isthe.com/html

# CGI directory
#
CGI_DIR= /home/www/isthe.com/cgi-bin/chongo

# from where the number utility is installed
#
NUMBER_BIN= ../number/number.pl

# the whoami.cgi source code directory
#
WHOAMI_DIR= ../whoami

# As input files:
#
# CGI= the .cgi scripts that are under RCS control
# ALT_CGI= the .cgi scripts from another location are fetched
#
# As files that are built:
#
# NOTE: The list below can be built by using the output from the:
#
#	make update
#
# Just add a *.cgi name to the CGI list, insert the 'make update' output
# and remove the old CGI lines.
#
# NOTE: We do not put number here since their source
#	is built and installed from elsewhere.
#
# NOTE: We do not put whoami.cgi here since the Makefile in ${WHOAMI_DIR}
# 	installs whoami.cgi into the cgi-bin directory directly.
# 	We only use whoami.cgi in $(TECH_COMP_CGI} because we want
# 	to install the file into our web source page.
#
CGI= cgi-example.cgi cgi-simple.cgi html.cgi nothing.cgi
ALT_CGI= whoami.cgi
ALT_SRC= whoami.cgi.alt
#
###
#
# SPECIAL_CGI=		cgi special targets
#
SPECIAL_CGI= number.cgi index.html

###
#
# TECH_COMP_CGI_DIR - location of www.isthe.com/chongo/tech/comp/cgi/
# TECH_COMP_CGI - files to be exported to ${TECH_COMP_CGI_DIR}
#
TECH_COMP_CGI_DIR= ${DOCROOT}/chongo/tech/comp/cgi
TECH_COMP_CGI= html.cgi cgi-example.cgi cgi-simple.cgi \
		${ALT_CGI}

# targets - that can be removed
#
TARGETS= ${ALT_CGI} number.cgi

# NOTE: We duplicate the critical chown and chmod commands that must be
#	in place so that apache suexec will or will not execute them
#
all: ${ALT_CGI} ${CGI} ${SPECIAL_CGI} exported
	@${CHMOD} 0555 ${ALT_CGI} ${CGI} ${SPECIAL_CGI}

# number.cgi is constructed from a /usr/local program.   That prog has a
# makefile that will also deposit itself in this directory.
#
# NOTE: Besure that the install rule of /usr/local/src/cmd/number/Makefile
#	is the equivalent to the number.cgi rule found below.
#
number.cgi: ${NUMBER_BIN}
	-${RM} -f $@
	-${CP} $? $@
	-${CHMOD} 0555 $@

${ALT_CGI}: ${WHOAMI_DIR}/${ALT_SRC}
	-${RM} -f $@
	-${CP} $? $@
	-${CHMOD} 0555 $@

${WHOAMI_DIR}/${ALT_SRC}: ${WHOAMI_DIR}/${ALT_CGI}
	cd ${WHOAMI_DIR}; ${MAKE} ${ALT_SRC}

# index.html directory listing hiding
#
index.html: nothing.cgi
	-${RM} -f $@
	-${LN} -s $? $@

# Given the ${CGI}, print the new CGI lists
#
update:
	@-(echo "xxxxx"; \
	   for i in ${CGI}; do \
	    echo $$i; \
	done | ${SORT}) | ${FMT} -70 | \
	    ${SED} -e '1s/xxxxx/CGI=/' -e '2,$$s/^/	/' \
		   -e 's/$$/ \\/' -e '$$s/ \\$$//'
	@-(echo "xxxxx"; \
	   for i in ${ALT_CGI}; do \
	    echo $$i; \
	done | ${SORT}) | ${FMT} -70 | \
	    ${SED} -e '1s/xxxxx/ALT_CGI=/' -e '2,$$s/^/	/' \
		   -e 's/$$/ \\/' -e '$$s/ \\$$//'
	@-(echo "xxxxx"; \
	   for i in ${ALT_CGI}; do \
		echo $$i.alt; \
	done | ${SORT}) | ${FMT} -70 | \
	    ${SED} -e '1s/xxxxx/ALT_SRC=/' -e '2,$$s/^/	/' \
		   -e 's/$$/ \\/' -e '$$s/ \\$$//'

# exported - export cgi scripts into .txt files for html use
#
exported: ${TECH_COMP_CGI}

clean:

clobber: clean
	${RM} -f ${TARGETS}

install: all
	@if [[ `$(ID) -u` != 0 ]]; then \
	    echo "ERROR: must be root to install" 1>&2; \
	    exit 1; \
	fi
	@-if [[ -d "${DOCROOT}" ]]; then \
	    for i in ${TECH_COMP_CGI}; do \
		j="`echo $$i | ${SED} -e 's/\.cgi/_cgi/'`"; \
		if cmp -s $$i ${TECH_COMP_CGI_DIR}/$$j.txt; then \
		    :; \
		else \
		    echo "	${CP} $$i ${TECH_COMP_CGI_DIR}/$$j.txt.new"; \
		    ${CP} -f $$i ${TECH_COMP_CGI_DIR}/$$j.txt.new; \
		    echo "	${CHOWN} ${HTML_USER}:${HTML_GROUP} ${TECH_COMP_CGI_DIR}/$$j.txt.new"; \
		    ${CHOWN} ${HTML_USER}:${HTML_GROUP} ${TECH_COMP_CGI_DIR}/$$j.txt.new; \
		    echo "	${CHMOD} 0444 ${TECH_COMP_CGI_DIR}/$$j.txt.new"; \
		    ${CHMOD} 0444 ${TECH_COMP_CGI_DIR}/$$j.txt.new; \
		    echo "	${MV} -f ${TECH_COMP_CGI_DIR}/$$j.txt.new ${TECH_COMP_CGI_DIR}/$$j.txt"; \
		    ${MV} -f ${TECH_COMP_CGI_DIR}/$$j.txt.new ${TECH_COMP_CGI_DIR}/$$j.txt; \
		fi; \
	    done; \
	else \
	    echo "skipping export actions due to lack of directory: ${DOCROOT}"; \
	fi
	@-if [[ -d "${CGI_DIR}" ]]; then \
	    ${INSTALL} -d -m 0555 -o ${CGI_USER} -g ${CGI_GROUP} ${CGI_DIR}; \
	    ${INSTALL} -v -c -m 0555 -o ${CGI_USER} -g ${CGI_GROUP} ${CGI} ${SPECIAL_CGI} ${CGI_DIR}; \
	else \
	    echo "skipping install commands due to lack of directory: ${CGI_DIR}"; \
	fi
