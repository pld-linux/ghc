# NOTE
# - happy, alex needed only when using darcs checkout or regenerating parsers
#   http://hackage.haskell.org/trac/ghc/wiki/Building/Prerequisites
# TODO
# - FIX files (it's a rough mess now)
# - system gmp/gmp-4.2.1.tar.gz
# - system libffi/libffi-3.0.4.tar.gz
# - ghc-pkg is called with invalid args for 6.10 (-l, --show-package), and the .m4 are not distributed (present only in aclocal.m4 (mv to acinclude.m4?)
# - patch libraries/terminfo/configure.ac to link against tinfo not ncurses (-Wl,--as-needed) and run autotools only there?
# - http://hackage.haskell.org/trac/ghc/wiki/Building/Porting
#
# Conditional build:
%bcond_with	bootstrap	# use foreign (non-rpm) ghc to bootstrap (extra 140MB to download)
%bcond_with	unregistered	# non-registerised interpreter (use for build problems/new arches)
%bcond_without	doc		# don't build documentation (requires haddock)
%bcond_without	extralibs	# don't build extra libs
#
Summary:	Glasgow Haskell Compilation system
Summary(pl.UTF-8):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	6.10.4
Release:	0.2
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.bz2
# Source0-md5:	167687fa582ef6702aaac24e139ec982
Source1:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src-extralibs.tar.bz2
# Source1-md5:	37ce285617d7cebabc3cf6805bdbca25
%if %{with bootstrap}
Source3:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-i386-unknown-linux.tar.bz2
# NoSource3-md5:	ba9eefecf9753a391d84ffe9f8515e1c
NoSource:	3
Source4:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-x86_64-unknown-linux.tar.bz2
# NoSource4-md5:	3521c5a12808811d32f9950fe7a3815c
NoSource:	4
%endif
Patch0:	%{name}-cabal-flags.patch
URL:		http://haskell.org/ghc/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
%{!?with_bootstrap:BuildRequires:	alex >= 2.0}
BuildRequires:	freealut-devel
%{!?with_bootstrap:BuildRequires:	ghc >= 6.6}
BuildRequires:	gmp-devel
%{!?with_bootstrap:BuildRequires:	happy >= 1.15}
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.213
%if %{with doc}
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	tetex
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex-bibtex
#For generating documentation in PDF: fop or xmltex
%endif
Provides:	haddock
# there is no more ghc ports in PLD
Provides:	haskell
# th-ppc removed:
#error: ghc: no such package
#error: haddock: no such package
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with bootstrap}
#%%define		specflags	-O2 -pipe
%endif

%description
Haskell is the standard lazy purely functional programming language.
The current language version is Haskell 98, agreed in December 1998,
with a revised version published in January 2003.

GHC is a state-of-the-art programming suite for Haskell. Included is
an optimising compiler generating good code for a variety of
platforms, together with an interactive system for convenient, quick
development. The distribution includes space and time profiling
facilities, a large collection of libraries, and support for various
language extensions, including concurrency, exceptions, and foreign
language interfaces (C, C++, whatever).

A wide variety of Haskell related resources (tutorials, libraries,
specifications, documentation, compilers, interpreters, references,
contact information, links to research groups) are available from the
Haskell home page at <http://haskell.org/>.

%description -l pl.UTF-8
Haskell to standardowy leniwy i czysto funkcyjny język programowania.
Bieżącą wersją języka jest Haskell 98, uzgodniony w grudniu 1998, ze
zmodyfikowaną wersją opublikowaną w styczniu 2003.

GHC to dojrzałe i nowoczesne środowisko do programowania w Haskellu.
Zawiera optymalizujący kompilator generujący dobry kod dla różnych
platform, wraz z interakcyjnym systemem do wygodnego
eksperymentowania. Dystrybucja zawiera narzędzia do profilowania
zużycia pamięci i czasu, sporą kolekcję bibliotek i wsparcie dla
różnych rozszerzeń języka, w tym współbieżności, wyjątków i łączenia z
innymi językami (np. C albo C++).

Różnorodne zasoby związane z Haskellem (podręczniki, biblioteki,
specyfikacje, dokumentacja, kompilatory, interpretery, literatura,
informacje kontaktowe, odsyłacze do grup naukowo-badawczych) są
dostępne ze strony domowej Haskella pod <http://haskell.org/>.

%package prof
Summary:	Profiling libraries for GHC
Summary(pl.UTF-8):	Biblioteki profilujące dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling libraries for Glorious Glasgow Haskell Compilation System
(GHC). They should be installed when GHC's profiling subsystem is
needed.

%description prof -l pl.UTF-8
Biblioteki profilujące dla GHC. Powinny być zainstalowane kiedy
potrzebujemy systemu profilującego z GHC.

%prep
%setup -q %{?with_extralibs:-b1}
%if %{with bootstrap}
%ifarch %{ix86}
%{__tar} -xjf %{SOURCE3}
%endif
%ifarch %{x8664}
%{__tar} -xjf %{SOURCE4}
%endif
mv %{name}-%{version} binsrc
%endif
%patch0

# 0.10.1 ghc-pkg -l is not supported
sed -i -e 's,fp_ghc_pkg_guess" -l,fp_ghc_pkg_guess" list,' configure

%build
cat <<'EOF' > mk/build.mk
# http://darcs.haskell.org/ghc/mk/build.mk.sample
#SRC_HC_OPTS	 = -O2 -H64m -fasm
#GhcStage1HcOpts = -O0 -fasm -Wall
#GhcStage2HcOpts = -O0 -fasm -Wall
#GhcHcOpts	   = -Rghc-timing
#GhcLibHcOpts	= -O2 -XGenerics
#GhcLibWays	  = p
#SplitObjs	   = YES
#SplitObjs	   = No
#GhcBootLibs	 = %{!?with_extralibs:NO}%{?with_extralibs:YES}
#%{?without_doc:HADDOCK_DOCS = NO}
EOF

%if %{with unregistered}
cat << 'EOF' >> mk/build.mk
# An unregisterised build is one that compiles via vanilla C only
# http://hackage.haskell.org/trac/ghc/wiki/Building/Unregisterised
GhcUnregisterised=YES
GhcWithNativeCodeGen=NO
GhcWithInterpreter=NO
SplitObjs=NO
EOF
%endif

top=$(pwd)
%if %{with bootstrap}
# we need to first install the tarball somewhere, as seems the programs don't
# work out of the path otherwise
if [ ! -f .bindist.install.mark ]; then
	top=$(pwd)
	cd binsrc
	./configure \
		--prefix=$top/bindist
	%{__make} install \
		LATEX_DOCS=NO \
		HADDOCK_DOCS=NO
	cd ..

	touch .bindist.install.mark
fi
%endif

%{?with_bootstrap:PATH=$top/bindist/bin:$PATH:%{_prefix}/local/bin}

%configure \
	--prefix=%{_prefix} \
	--with-gcc="%{__cc}" \
	--with-curses-includes=/usr/include/ncursesw \
%if %{with bootstrap}
	GhcPkgCmd=$top/bindist/bin/ghc-pkg \
%endif
%if %{with bootstrap2}
	--with-ghc=$top/bindist/bin/ghc \
%endif
%if %{with bootstrap1}
	--with-hc=$PWD/bindist/bin/ghc \
	--with-ghc=$PWD/bindist/ghc/dist-stage2/build/ghc/ghc \
	--with-hc=$PWD/bindist/ghc/dist-stage2/build/ghc/ghc \
%endif

%{__make}

%if %{with doc}
%{__make} html
# broken
#%{__make} -C docs/ext-core ps
%{__make} -C docs/storage-mgt ps
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	datadir=$RPM_BUILD_ROOT%{_libdir}/%{name}-%{version} \
	libdir=$RPM_BUILD_ROOT%{_libdir}/%{name}-%{version} \
	docdir=$(pwd)/docs-root

%if %{with doc}
rm -rf html
%{__make} install-docs \
	datadir=$(pwd) \
	mandir=RPM_BUILD_ROOT%{_mandir} \
	docdir=$(pwd)/docs-root
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCE README
%if %{with doc}
%doc docs/users_guide/users_guide docs/comm
%doc docs/*-*/*.ps
%doc docs-root/libraries
%endif
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/ghc-%{version}
%{_libdir}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/extra-gcc-opts
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-asm
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-pkg
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-split
%attr(755,root,root) %{_libdir}/ghc-%{version}/haddock
%attr(755,root,root) %{_libdir}/ghc-%{version}/hsc2hs
%attr(755,root,root) %{_libdir}/ghc-%{version}/runghc
%attr(755,root,root) %{_libdir}/ghc-%{version}/unlit
%{_libdir}/ghc-%{version}/libHS*.a
%{_libdir}/ghc-%{version}/libffi.a
%exclude %{_libdir}/ghc-%{version}/libHS*_p.a
%ifarch %{ix86} %{x8664} ppc ppc64 sparc sparcv9 sparc64
%{_libdir}/ghc-%{version}/HS*.o
%endif
%{_libdir}/ghc-%{version}/ghc*-usage.txt
%{_libdir}/ghc-%{version}/hsc2hs-*
%{_libdir}/ghc-%{version}/html
%{_libdir}/ghc-%{version}/package.conf
%{_libdir}/ghc-%{version}/array-*
%{_libdir}/ghc-%{version}/base-*
%{_libdir}/ghc-%{version}/bytestring-*
%{_libdir}/ghc-%{version}/Cabal-*
%{_libdir}/ghc-%{version}/containers-*
%{_libdir}/ghc-%{version}/directory-*
%{_libdir}/ghc-%{version}/dph-base-*
%{_libdir}/ghc-%{version}/dph-par-*
%{_libdir}/ghc-%{version}/dph-prim-interface-*
%{_libdir}/ghc-%{version}/dph-prim-par-*
%{_libdir}/ghc-%{version}/dph-prim-seq-*
%{_libdir}/ghc-%{version}/dph-seq-*
%{_libdir}/ghc-%{version}/extensible-exceptions-*
%{_libdir}/ghc-%{version}/filepath-*
%{_libdir}/ghc-%{version}/ghc-%{version}
%{_libdir}/ghc-%{version}/ghc-prim-*
%{_libdir}/ghc-%{version}/haddock-*
%{_libdir}/ghc-%{version}/haskell98-*
%{_libdir}/ghc-%{version}/haskell-src-*
%{_libdir}/ghc-%{version}/hpc-*
%{_libdir}/ghc-%{version}/html-*
%{_libdir}/ghc-%{version}/HUnit-*
%{_libdir}/ghc-%{version}/integer-*
%{_libdir}/ghc-%{version}/mtl-*
%{_libdir}/ghc-%{version}/network-*
%{_libdir}/ghc-%{version}/old-locale-*
%{_libdir}/ghc-%{version}/old-time-*
%{_libdir}/ghc-%{version}/packedstring-*
%{_libdir}/ghc-%{version}/parallel-*
%{_libdir}/ghc-%{version}/parsec-*
%{_libdir}/ghc-%{version}/pretty-*
%{_libdir}/ghc-%{version}/process-*
%{_libdir}/ghc-%{version}/QuickCheck-*
%{_libdir}/ghc-%{version}/random-*
%{_libdir}/ghc-%{version}/regex-base-*
%{_libdir}/ghc-%{version}/regex-compat-*
%{_libdir}/ghc-%{version}/regex-posix-*
%{_libdir}/ghc-%{version}/stm-*
%{_libdir}/ghc-%{version}/syb-*
%{_libdir}/ghc-%{version}/template-haskell-*
%{_libdir}/ghc-%{version}/time-*
%{_libdir}/ghc-%{version}/unix-*
%{_libdir}/ghc-%{version}/xhtml-*

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/libHS*_p.a
