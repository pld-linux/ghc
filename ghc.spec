#
# Conditional build:
%bcond_with	bootstrap	# use foreign (non-rpm) ghc to bootstrap
# due to http://hackage.haskell.org/trac/ghc/ticket/1427 (fixed by gcc42 patch)
%bcond_with	unregistered	# non-registerised interpreter
%bcond_without	doc		# don't build documentation (requires haddock)
#
Summary:	Glasgow Haskell Compilation system
Summary(pl.UTF-8):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	6.6.1
Release:	7
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.bz2
# Source0-md5:	ba9f4aec2fde5ff1e1548ae69b78aeb0
Source1:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src-extralibs.tar.bz2
# Source1-md5:	43a26b81608b206c056adc3032f7da2a
Patch0:		%{name}-ac.patch
Patch1:		%{name}-tinfo.patch
Patch2:		%{name}-gcc42.patch
Patch3:		%{name}-perl10.patch
URL:		http://haskell.org/ghc/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
%{!?with_bootstrap:BuildRequires:	alex >= 2.0}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	freealut-devel
%{!?with_bootstrap:BuildRequires:	ghc}
BuildRequires:	gmp-devel
%{!?with_bootstrap:BuildRequires:	happy >= 1.15}
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.213
%if %{with doc}
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	haddock
BuildRequires:	libxslt-progs
BuildRequires:	tetex
BuildRequires:	tetex-dvips
BuildRequires:	tetex-latex-bibtex
#For generating documentation in PDF: fop or xmltex
%endif
Provides:	haskell
# there is no more ghc ports in PLD
ExclusiveArch:	%{ix86} %{x8664} alpha ppc sparc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Haskell home page at http://haskell.org/.

Authors:
--------
    Krasimir Angelov <ka2_mail@yahoo.com>
    Manuel Chakravarty <chak@cse.unsw.edu.au>
    Koen Claessen <koen@cs.chalmers.se>
    Robert Ennals <Robert.Ennals@cl.cam.ac.uk>
    Sigbjorn Finne <sof@galconn.com>
    Gabrielle Keller <keller@cvs.haskell.org>
    Marcin Kowalczyk <qrczak@knm.org.pl>
    Jeff Lewis <jeff@galconn.com>
    Ian Lynagh <igloo@earth.li>
    Simon Marlow <simonmar@microsoft.com>
    Sven Panne <sven.panne@aedion.de>
    Ross Paterson <ross@soi.city.ac.uk>
    Simon Peyton Jones <simonpj@microsoft.com>
    Don Stewart <dons@cse.unsw.edu.au>
    Volker Stolz <stolz@i2.informatik.rwth-aachen.de>
    Wolfgang Thaller <wolfgang.thaller@gmx.net>
    Andrew Tolmach <apt@cs.pdx.edu>
    Keith Wansbrough <Keith.Wansbrough@cl.cam.ac.uk>
    Michael Weber <michael.weber@post.rwth-aachen.de>
    plus a dozen helping hands...

%description -l pl.UTF-8
Haskell to standardowy leniwy i czysto funkcyjny język programowania.
Bieżącą wersją języka jest Haskell 98, uzgodniony w grudniu 1998, ze
zmodyfikowaną wersją opublikowaną w styczniu 2003.

GHC to dojrzałe i nowoczesne środowisko do programowania w Haskellu.
Zawiera optymalizujący kompilator generujący dobry kod dla różnych
platform, wraz z interakcyjnym systemem do wygodnego eksperymentowania.
Dystrybucja zawiera narzędzia do profilowania zużycia pamięci i czasu,
sporą kolekcję bibliotek i wsparcie dla różnych rozszerzeń języka,
w tym współbieżności, wyjątków i łączenia z innymi językami (np. C
albo C++).

Różnorodne zasoby związane z Haskellem (podręczniki, biblioteki,
specyfikacje, dokumentacja, kompilatory, interpretery, literatura,
informacje kontaktowe, odsyłacze do grup naukowo-badawczych)
są dostępne ze strony domowej Haskella pod http://haskell.org/.

Autorzy:
--------
    Krasimir Angelov <ka2_mail@yahoo.com>
    Manuel Chakravarty <chak@cse.unsw.edu.au>
    Koen Claessen <koen@cs.chalmers.se>
    Robert Ennals <Robert.Ennals@cl.cam.ac.uk>
    Sigbjorn Finne <sof@galconn.com>
    Gabrielle Keller <keller@cvs.haskell.org>
    Marcin Kowalczyk <qrczak@knm.org.pl>
    Jeff Lewis <jeff@galconn.com>
    Ian Lynagh <igloo@earth.li>
    Simon Marlow <simonmar@microsoft.com>
    Sven Panne <sven.panne@aedion.de>
    Ross Paterson <ross@soi.city.ac.uk>
    Simon Peyton Jones <simonpj@microsoft.com>
    Don Stewart <dons@cse.unsw.edu.au>
    Volker Stolz <stolz@i2.informatik.rwth-aachen.de>
    Wolfgang Thaller <wolfgang.thaller@gmx.net>
    Andrew Tolmach <apt@cs.pdx.edu>
    Keith Wansbrough <Keith.Wansbrough@cl.cam.ac.uk>
    Michael Weber <michael.weber@post.rwth-aachen.de>
    oraz wiele pomocnych dłoni...

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
%setup -q -b1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%if %{with unregistered}
cat << 'EOF' >> mk/build.mk
GhcUnregisterised=YES
GhcWithNativeCodeGen=NO
SplitObjs=NO
EOF
%endif

%build
%{?with_bootstrap:PATH=$PATH:/usr/local/bin}
cp -f /usr/share/automake/config.sub .

%{__autoconf}
cd libraries/readline
%{__autoconf}
cd ../..

%configure \
	--prefix=%{_prefix} \
	--with-gcc="%{__cc}"

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
	datadir=$RPM_BUILD_ROOT%{_datadir}/%{name}-%{version} \
	libdir=$RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}

%if %{with doc}
rm -rf html
%{__make} install-docs \
	datadir=$(pwd) \
	mandir=RPM_BUILD_ROOT%{_mandir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCE README
%if %{with doc}
%doc docs/users_guide/users_guide docs/comm
%doc docs/*-*/*.ps
%doc libraries/html-docs
%doc html/* libraries/Cabal/doc/Cabal
%endif
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/ghc-%{version}
%{_libdir}/ghc-%{version}/hslibs-imports
%{_libdir}/ghc-%{version}/icons
%{_libdir}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/imports
%{_libdir}/ghc-%{version}/extra-gcc-opts
%exclude %{_libdir}/ghc-%{version}/imports/*.p_hi
%exclude %{_libdir}/ghc-%{version}/imports/*/*.p_hi
%exclude %{_libdir}/ghc-%{version}/imports/*/*/*.p_hi
%exclude %{_libdir}/ghc-%{version}/imports/*/*/*/*.p_hi
%attr(755,root,root) %{_libdir}/ghc-%{version}/cgprof
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-%{version}
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-asm
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-pkg.bin
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-split
%attr(755,root,root) %{_libdir}/ghc-%{version}/hsc2hs-bin
%attr(755,root,root) %{_libdir}/ghc-%{version}/unlit
%{_libdir}/ghc-%{version}/libHS*.a
%exclude %{_libdir}/ghc-%{version}/libHS*_p.a
%ifarch %{ix86} %{x8664} ppc ppc64 sparc sparcv9 sparc64
%{_libdir}/ghc-%{version}/HS*.o
%endif
%{_libdir}/ghc-%{version}/package.conf
%{_libdir}/ghc-%{version}/*.h
%{_libdir}/ghc-%{version}/ghc*-usage.txt

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/imports/*.p_hi
%{_libdir}/ghc-%{version}/imports/*/*.p_hi
%{_libdir}/ghc-%{version}/imports/*/*/*.p_hi
%{_libdir}/ghc-%{version}/imports/*/*/*/*.p_hi
%{_libdir}/ghc-%{version}/libHS*_p.a
