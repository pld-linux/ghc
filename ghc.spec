#
# NOTE
# - happy, alex needed only when using darcs checkout or regenerating parsers
#   http://hackage.haskell.org/trac/ghc/wiki/Building/Prerequisites
#
# - http://hackage.haskell.org/trac/ghc/wiki/Building/Porting
#
# Conditional build:
%bcond_with	bootstrap	# use foreign (non-rpm) ghc to bootstrap (extra 140MB to download)
%bcond_with	unregistered	# non-registerised interpreter (use for build problems/new arches)
%bcond_without	doc		# don't build documentation (requires haddock)

Summary:	Glasgow Haskell Compilation system
Summary(pl.UTF-8):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	7.2.1
Release:	0.1
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.bz2
# Source0-md5:	c2a6d1ce13b6bb95fa2d743a143835eb
%if %{with bootstrap}
Source3:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-i386-unknown-linux-n.tar.bz2
# Source3-md5:	8ed8540571f7b10d8caf782755e35818
Source4:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-x86_64-unknown-linux-n.tar.bz2
# Source4-md5:	d58e5a50d8b120ac933afbd10a773aef
%endif
Patch0:		%{name}-pld.patch
Patch1:		%{name}-pkgdir.patch
URL:		http://haskell.org/ghc/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
%{!?with_bootstrap:BuildRequires:	alex >= 2.0}
BuildRequires:	freealut-devel
%{!?with_bootstrap:BuildRequires:	ghc >= 6.8}
BuildRequires:	gmp-devel
%{!?with_bootstrap:BuildRequires:	happy >= 1.16}
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.607
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	dblatex
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	texlive
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-rsfs
BuildRequires:	texlive-latex-bibtex
#For generating documentation in PDF: fop or xmltex
%endif
Suggests:	ghc-haskell-platform
Provides:	haddock
Obsoletes:	haddock
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# There is nothing that may or should be compressed
%define		_noautocompressdoc	*

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
%setup -q
%if %{with bootstrap}
%ifarch %{ix86}
%{__tar} -xjf %{SOURCE3}
%endif
%ifarch %{x8664}
%{__tar} -xjf %{SOURCE4}
%endif
mv %{name}-%{version} binsrc
%endif
%patch0 -p1
%patch1 -p1

%build
# use ld.bfd
#install -d our-ld
#ln -s %{_bindir}/ld.bfd our-ld/ld
#export PATH=$(pwd)/our-ld:$PATH


%{__autoconf}
cd libraries/terminfo
%{__autoconf}
cd -

cat <<'EOF' > mk/build.mk
#GhcStage1HcOpts += -O0 -Wall
#GhcStage2HcOpts += -O0 -Wall
#SRC_HC_OPTS      += -lffi -O0 -H64m
#GhcHcOpts        += -Rghc-timing
#GhcLibHcOpts     += -O -dcore-lint -keep-hc-files
#SplitObjs        += NO
PlatformSupportsSharedLibs = YES
HADDOCK_DOCS        = %{!?with_doc:NO}%{?with_doc:YES}
LATEX_DOCS          = %{!?with_doc:NO}%{?with_doc:YES}
BUILD_DOCBOOK_HTMLS = %{!?with_doc:NO}%{?with_doc:YES}
BUILD_DOCBOOK_PDFS  = %{!?with_doc:NO}%{?with_doc:YES}
XSLTPROC_OPTS       += --nonet
EOF

%if %{with unregistered}
# An unregisterised build is one that compiles via vanilla C only
# http://hackage.haskell.org/trac/ghc/wiki/Building/Unregisterised
cat <<'EOF' >> mk/build.mk
GhcUnregisterised=YES
GhcWithNativeCodeGen=NO
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

PATH=$top/bindist/bin:$PATH:%{_prefix}/local/bin
%endif

%configure \
	--target=%{_target_platform} \
	--prefix=%{_prefix} \
	--with-gcc="%{__cc}" \
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

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
rm -rf docs-root

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a $RPM_BUILD_ROOT%{_datadir}/doc/%{name} docs-root
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

# fix paths to docs in package list
sed -i -e 's|%{_datadir}/doc/%{name}|%{_docdir}/%{name}-%{version}|g' $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/package.conf.d/*.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
if [ "$1" != 0 ]; then
	%ghc_pkg_recache
fi

%files
%defattr(644,root,root,755)
%doc ANNOUNCE README
%if %{with doc}
%doc docs/comm
%doc docs-root/html
%doc docs-root/*.pdf
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
%exclude %{_libdir}/ghc-%{version}/libHS*_p.a
%ifarch %{ix86} %{x8664} ppc ppc64 sparc sparcv9 sparc64
%{_libdir}/ghc-%{version}/HS*.o
%endif
%{_libdir}/ghc-%{version}/ghc*-usage.txt
%{_libdir}/ghc-%{version}/html
%dir %{_libdir}/ghc-%{version}/package.conf.d
%{_libdir}/ghc-%{version}/package.conf.d/*.conf
%config %verify(not md5 mtime size) %{_libdir}/ghc-%{version}/package.conf.d/package.cache
%{_libdir}/ghc-%{version}/template-hsc.h
%{_mandir}/man1/ghc.1*

%dir %{_libdir}/ghc-%{version}/array-*
%dir %{_libdir}/ghc-%{version}/array-*/Data
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/IO
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/*.hi
%{_libdir}/ghc-%{version}/array-*/HSarray-*.o
%{_libdir}/ghc-%{version}/array-*/libHSarray-*.a
%exclude %{_libdir}/ghc-%{version}/array-*/libHSarray-*_p.a

%dir %{_libdir}/ghc-%{version}/base-*
%dir %{_libdir}/ghc-%{version}/base-*/Control
%dir %{_libdir}/ghc-%{version}/base-*/Control/Concurrent
%{_libdir}/ghc-%{version}/base-*/Control/Concurrent/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Exception
%{_libdir}/ghc-%{version}/base-*/Control/Exception/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad
%{_libdir}/ghc-%{version}/base-*/Control/Monad/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad/ST
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Data
%dir %{_libdir}/ghc-%{version}/base-*/Data/Generics
%{_libdir}/ghc-%{version}/base-*/Data/Generics/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/STRef
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Debug
%{_libdir}/ghc-%{version}/base-*/Debug/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/C
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.hi
%{_libdir}/ghc-%{version}/base-*/Foreign/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/Marshal
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC
%{_libdir}/ghc-%{version}/base-*/GHC/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.hi
%{_libdir}/ghc-%{version}/base-*/*.hi
%{_libdir}/ghc-%{version}/base-*/HSbase-*.o
%{_libdir}/ghc-%{version}/base-*/include
%{_libdir}/ghc-%{version}/base-*/libHSbase-*.a
%exclude %{_libdir}/ghc-%{version}/base-*/libHSbase-*_p.a
%dir %{_libdir}/ghc-%{version}/base-*/System
%dir %{_libdir}/ghc-%{version}/base-*/System/Console
%{_libdir}/ghc-%{version}/base-*/System/Console/*.hi
%{_libdir}/ghc-%{version}/base-*/System/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/System/IO
%{_libdir}/ghc-%{version}/base-*/System/IO/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/System/Mem
%{_libdir}/ghc-%{version}/base-*/System/Mem/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/System/Posix
%{_libdir}/ghc-%{version}/base-*/System/Posix/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Text
%{_libdir}/ghc-%{version}/base-*/Text/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators
%{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Text/Read
%{_libdir}/ghc-%{version}/base-*/Text/Read/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Text/Show
%{_libdir}/ghc-%{version}/base-*/Text/Show/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Unsafe
%{_libdir}/ghc-%{version}/base-*/Unsafe/*.hi

%dir %{_libdir}/ghc-%{version}/bin-package-db-*
%dir %{_libdir}/ghc-%{version}/bin-package-db-*/Distribution
%dir %{_libdir}/ghc-%{version}/bin-package-db-*/Distribution/InstalledPackageInfo
%{_libdir}/ghc-%{version}/bin-package-db-*/Distribution/InstalledPackageInfo/*.hi
%{_libdir}/ghc-%{version}/bin-package-db-*/HSbin-package-db-*.o
%{_libdir}/ghc-%{version}/bin-package-db-*/libHSbin-package-db-*.a
%exclude %{_libdir}/ghc-%{version}/bin-package-db-*/libHSbin-package-db-*_p.a

%dir %{_libdir}/ghc-%{version}/bytestring-*
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/*.hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/HSbytestring-*.o
%{_libdir}/ghc-%{version}/bytestring-*/include
%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-*.a
%exclude %{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-*_p.a

%dir %{_libdir}/ghc-%{version}/Cabal-*
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/HSCabal-*.o
%dir %{_libdir}/ghc-%{version}/Cabal-*/Language
%dir %{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell
%{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/libHSCabal-*.a
%exclude %{_libdir}/ghc-%{version}/Cabal-*/libHSCabal-*_p.a

%dir %{_libdir}/ghc-%{version}/containers-*
%dir %{_libdir}/ghc-%{version}/containers-*/Data
%{_libdir}/ghc-%{version}/containers-*/Data/*.hi
%{_libdir}/ghc-%{version}/containers-*/HScontainers-*.o
%{_libdir}/ghc-%{version}/containers-*/libHScontainers-*.a
%exclude %{_libdir}/ghc-%{version}/containers-*/libHScontainers-*_p.a

%dir %{_libdir}/ghc-%{version}/directory-*
%{_libdir}/ghc-%{version}/directory-*/HSdirectory-*.o
%{_libdir}/ghc-%{version}/directory-*/include
%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-*.a
%exclude %{_libdir}/ghc-%{version}/directory-*/libHSdirectory-*_p.a
%dir %{_libdir}/ghc-%{version}/directory-*/System
%{_libdir}/ghc-%{version}/directory-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/dph-base-*
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data/Array
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Arr
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Arr/*.hi
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Base
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Base/*.hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/*.hi
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Stream
%dir %{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Stream/Flat
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Stream/Flat/*.hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Stream/*.hi
%{_libdir}/ghc-%{version}/dph-base-*/HSdph-base-*.o
%{_libdir}/ghc-%{version}/dph-base-*/include
%{_libdir}/ghc-%{version}/dph-base-*/libHSdph-base-*.a
%exclude %{_libdir}/ghc-%{version}/dph-base-*/libHSdph-base-*_p.a

%dir %{_libdir}/ghc-%{version}/dph-par-*
%dir %{_libdir}/ghc-%{version}/dph-par-*/Data
%dir %{_libdir}/ghc-%{version}/dph-par-*/Data/Array
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/*.hi
%dir %{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/*.hi
%dir %{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Lifted
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Lifted/*.hi
%dir %{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Prelude
%dir %{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Prelude/Base
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Prelude/Base/*.hi
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Prelude/*.hi
%{_libdir}/ghc-%{version}/dph-par-*/HSdph-par-*.o
%{_libdir}/ghc-%{version}/dph-par-*/libHSdph-par-*.a
%exclude %{_libdir}/ghc-%{version}/dph-par-*/libHSdph-par-*_p.a

%dir %{_libdir}/ghc-%{version}/dph-prim-interface-*
%dir %{_libdir}/ghc-%{version}/dph-prim-interface-*/Data
%dir %{_libdir}/ghc-%{version}/dph-prim-interface-*/Data/Array
%dir %{_libdir}/ghc-%{version}/dph-prim-interface-*/Data/Array/Parallel
%{_libdir}/ghc-%{version}/dph-prim-interface-*/Data/Array/Parallel/*.hi
%{_libdir}/ghc-%{version}/dph-prim-interface-*/HSdph-prim-interface-*.o
%{_libdir}/ghc-%{version}/dph-prim-interface-*/include
%{_libdir}/ghc-%{version}/dph-prim-interface-*/libHSdph-prim-interface-*.a
%exclude %{_libdir}/ghc-%{version}/dph-prim-interface-*/libHSdph-prim-interface-*_p.a

%dir %{_libdir}/ghc-%{version}/dph-prim-par-*
%dir %{_libdir}/ghc-%{version}/dph-prim-par-*/Data
%dir %{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array
%dir %{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/*.hi
%dir %{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted
%dir %{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/Distributed
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/Distributed/*.hi
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/*.hi
%dir %{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/Parallel
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/Parallel/*.hi
%{_libdir}/ghc-%{version}/dph-prim-par-*/HSdph-prim-par-*.o
%{_libdir}/ghc-%{version}/dph-prim-par-*/libHSdph-prim-par-*.a
%exclude %{_libdir}/ghc-%{version}/dph-prim-par-*/libHSdph-prim-par-*_p.a

%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/*.hi
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/*.hi
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/Flat
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/Flat/*.hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/*.hi
%dir %{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/Segmented
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/Segmented/*.hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/HSdph-prim-seq-*.o
%{_libdir}/ghc-%{version}/dph-prim-seq-*/libHSdph-prim-seq-*.a
%exclude %{_libdir}/ghc-%{version}/dph-prim-seq-*/libHSdph-prim-seq-*_p.a

%dir %{_libdir}/ghc-%{version}/dph-seq-*
%dir %{_libdir}/ghc-%{version}/dph-seq-*/Data
%dir %{_libdir}/ghc-%{version}/dph-seq-*/Data/Array
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/*.hi
%dir %{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/*.hi
%dir %{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Lifted
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Lifted/*.hi
%dir %{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Prelude
%dir %{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Prelude/Base
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Prelude/Base/*.hi
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Prelude/*.hi
%{_libdir}/ghc-%{version}/dph-seq-*/HSdph-seq-*.o
%{_libdir}/ghc-%{version}/dph-seq-*/libHSdph-seq-*.a
%exclude %{_libdir}/ghc-%{version}/dph-seq-*/libHSdph-seq-*_p.a

%dir %{_libdir}/ghc-%{version}/extensible-exceptions-*
%dir %{_libdir}/ghc-%{version}/extensible-exceptions-*/Control
%dir %{_libdir}/ghc-%{version}/extensible-exceptions-*/Control/Exception
%{_libdir}/ghc-%{version}/extensible-exceptions-*/Control/Exception/*.hi
%{_libdir}/ghc-%{version}/extensible-exceptions-*/HSextensible-exceptions-*.o
%{_libdir}/ghc-%{version}/extensible-exceptions-*/libHSextensible-exceptions-*.a
%exclude %{_libdir}/ghc-%{version}/extensible-exceptions-*/libHSextensible-exceptions-*_p.a

%dir %{_libdir}/ghc-%{version}/filepath-*
%{_libdir}/ghc-%{version}/filepath-*/HSfilepath-*.o
%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-*.a
%exclude %{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-*_p.a
%dir %{_libdir}/ghc-%{version}/filepath-*/System
%dir %{_libdir}/ghc-%{version}/filepath-*/System/FilePath
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.hi
%{_libdir}/ghc-%{version}/filepath-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-prim-*
%dir %{_libdir}/ghc-%{version}/ghc-prim-*/GHC
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-prim-*/HSghc-prim-*.o
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-*.a
%exclude %{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-*_p.a

%dir %{_libdir}/ghc-%{version}/ghc-%{version}
%{_libdir}/ghc-%{version}/ghc-%{version}/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/HSghc-%{version}.o
%{_libdir}/ghc-%{version}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}.a
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Alpha
%{_libdir}/ghc-%{version}/ghc-%{version}/Alpha/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/PPC
%{_libdir}/ghc-%{version}/ghc-%{version}/PPC/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/SPARC
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/X86
%{_libdir}/ghc-%{version}/ghc-%{version}/X86/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-binary-*
%{_libdir}/ghc-%{version}/ghc-binary-*/HSghc-binary-*.o
%{_libdir}/ghc-%{version}/ghc-binary-*/libHSghc-binary-*.a
%exclude %{_libdir}/ghc-%{version}/ghc-binary-*/libHSghc-binary-*_p.a
%dir %{_libdir}/ghc-%{version}/ghc-binary-*/Data
%{_libdir}/ghc-%{version}/ghc-binary-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-binary-*/Data/Binary
%{_libdir}/ghc-%{version}/ghc-binary-*/Data/Binary/*.hi

%dir %{_libdir}/ghc-%{version}/haskell98-*
%{_libdir}/ghc-%{version}/haskell98-*/*.hi
%{_libdir}/ghc-%{version}/haskell98-*/HShaskell98-*.o
%{_libdir}/ghc-%{version}/haskell98-*/libHShaskell98-*.a
%exclude %{_libdir}/ghc-%{version}/haskell98-*/libHShaskell98-*_p.a

%dir %{_libdir}/ghc-%{version}/hpc-*
%{_libdir}/ghc-%{version}/hpc-*/HShpc-*.o
%{_libdir}/ghc-%{version}/hpc-*/libHShpc-*.a
%exclude %{_libdir}/ghc-%{version}/hpc-*/libHShpc-*_p.a
%dir %{_libdir}/ghc-%{version}/hpc-*/Trace
%dir %{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc
%{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc/*.hi

%dir %{_libdir}/ghc-%{version}/integer-*
%dir %{_libdir}/ghc-%{version}/integer-*/GHC
%{_libdir}/ghc-%{version}/integer-*/GHC/*.hi
%dir %{_libdir}/ghc-%{version}/integer-*/GHC/Integer
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/*.hi
%dir %{_libdir}/ghc-%{version}/integer-*/GHC/Integer/GMP
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/GMP/*.hi
%{_libdir}/ghc-%{version}/integer-*/HSinteger-*.o
%{_libdir}/ghc-%{version}/integer-*/libHSinteger-*.a
%exclude %{_libdir}/ghc-%{version}/integer-*/libHSinteger-*_p.a

%dir %{_libdir}/ghc-%{version}/old-locale-*
%{_libdir}/ghc-%{version}/old-locale-*/HSold-locale-*.o
%{_libdir}/ghc-%{version}/old-locale-*/libHSold-locale-*.a
%exclude %{_libdir}/ghc-%{version}/old-locale-*/libHSold-locale-*_p.a
%dir %{_libdir}/ghc-%{version}/old-locale-*/System
%{_libdir}/ghc-%{version}/old-locale-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/old-time-*
%{_libdir}/ghc-%{version}/old-time-*/HSold-time-*.o
%{_libdir}/ghc-%{version}/old-time-*/include
%{_libdir}/ghc-%{version}/old-time-*/libHSold-time-*.a
%exclude %{_libdir}/ghc-%{version}/old-time-*/libHSold-time-*_p.a
%dir %{_libdir}/ghc-%{version}/old-time-*/System
%{_libdir}/ghc-%{version}/old-time-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/pretty-*
%{_libdir}/ghc-%{version}/pretty-*/HSpretty-*.o
%{_libdir}/ghc-%{version}/pretty-*/libHSpretty-*.a
%exclude %{_libdir}/ghc-%{version}/pretty-*/libHSpretty-*_p.a
%dir %{_libdir}/ghc-%{version}/pretty-*/Text
%{_libdir}/ghc-%{version}/pretty-*/Text/*.hi
%dir %{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/*.hi

%dir %{_libdir}/ghc-%{version}/process-*
%{_libdir}/ghc-%{version}/process-*/HSprocess-*.o
%{_libdir}/ghc-%{version}/process-*/include
%{_libdir}/ghc-%{version}/process-*/libHSprocess-*.a
%exclude %{_libdir}/ghc-%{version}/process-*/libHSprocess-*_p.a
%dir %{_libdir}/ghc-%{version}/process-*/System
%{_libdir}/ghc-%{version}/process-*/System/*.hi
%dir %{_libdir}/ghc-%{version}/process-*/System/Process
%{_libdir}/ghc-%{version}/process-*/System/Process/*.hi

%dir %{_libdir}/ghc-%{version}/random-*
%{_libdir}/ghc-%{version}/random-*/HSrandom-*.o
%{_libdir}/ghc-%{version}/random-*/libHSrandom-*.a
%exclude %{_libdir}/ghc-%{version}/random-*/libHSrandom-*_p.a
%dir %{_libdir}/ghc-%{version}/random-*/System
%{_libdir}/ghc-%{version}/random-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/syb-*
%dir %{_libdir}/ghc-%{version}/syb-*/Data
%dir %{_libdir}/ghc-%{version}/syb-*/Data/Generics
%{_libdir}/ghc-%{version}/syb-*/Data/Generics/*.hi
%{_libdir}/ghc-%{version}/syb-*/Data/*.hi
%{_libdir}/ghc-%{version}/syb-*/HSsyb-*.o
%{_libdir}/ghc-%{version}/syb-*/libHSsyb-*.a
%exclude %{_libdir}/ghc-%{version}/syb-*/libHSsyb-*_p.a

%dir %{_libdir}/ghc-%{version}/template-haskell-*
%{_libdir}/ghc-%{version}/template-haskell-*/HStemplate-haskell-*.o
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.hi
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.hi
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Syntax
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Syntax/*.hi
%{_libdir}/ghc-%{version}/template-haskell-*/libHStemplate-haskell-*.a
%exclude %{_libdir}/ghc-%{version}/template-haskell-*/libHStemplate-haskell-*_p.a

%dir %{_libdir}/ghc-%{version}/time-*
%dir %{_libdir}/ghc-%{version}/time-*/Data
%{_libdir}/ghc-%{version}/time-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar
%{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar/*.hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Clock
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/*.hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Format
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/*.hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime
%{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime/*.hi
%{_libdir}/ghc-%{version}/time-*/HStime-*.o
%{_libdir}/ghc-%{version}/time-*/include
%{_libdir}/ghc-%{version}/time-*/libHStime-*.a
%exclude %{_libdir}/ghc-%{version}/time-*/libHStime-*_p.a

%dir %{_libdir}/ghc-%{version}/unix-*
%{_libdir}/ghc-%{version}/unix-*/HSunix-*.o
%{_libdir}/ghc-%{version}/unix-*/include
%{_libdir}/ghc-%{version}/unix-*/libHSunix-*.a
%exclude %{_libdir}/ghc-%{version}/unix-*/libHSunix-*_p.a
%dir %{_libdir}/ghc-%{version}/unix-*/System
%{_libdir}/ghc-%{version}/unix-*/System/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Process
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Process/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/libHS*_p.a
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/array-*/libHSarray-*_p.a
%{_libdir}/ghc-%{version}/base-*/Control/Concurrent/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Exception/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/Generics/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Debug/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.p_hi
%{_libdir}/ghc-%{version}/base-*/libHSbase-*_p.a
%{_libdir}/ghc-%{version}/base-*/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Console/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Mem/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Posix/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/Read/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/Show/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Unsafe/*.p_hi
%{_libdir}/ghc-%{version}/bin-package-db-*/Distribution/InstalledPackageInfo/*.p_hi
%{_libdir}/ghc-%{version}/bin-package-db-*/libHSbin-package-db-0.0.0.0_p.a
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-*_p.a
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/libHSCabal-*_p.a
%{_libdir}/ghc-%{version}/containers-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/libHScontainers-*_p.a
%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-*_p.a
%{_libdir}/ghc-%{version}/directory-*/System/*.p_hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Arr/*.p_hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Base/*.p_hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Stream/Flat/*.p_hi
%{_libdir}/ghc-%{version}/dph-base-*/Data/Array/Parallel/Stream/*.p_hi
%{_libdir}/ghc-%{version}/dph-base-*/libHSdph-base-*_p.a
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Lifted/*.p_hi
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Prelude/Base/*.p_hi
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/Parallel/Prelude/*.p_hi
%{_libdir}/ghc-%{version}/dph-par-*/Data/Array/*.p_hi
%{_libdir}/ghc-%{version}/dph-par-*/libHSdph-par-*_p.a
%{_libdir}/ghc-%{version}/dph-prim-interface-*/Data/Array/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-interface-*/libHSdph-prim-interface-*_p.a
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/Distributed/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-par-*/Data/Array/Parallel/Unlifted/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-par-*/libHSdph-prim-par-*_p.a
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/Flat/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/Data/Array/Parallel/Unlifted/Sequential/Segmented/*.p_hi
%{_libdir}/ghc-%{version}/dph-prim-seq-*/libHSdph-prim-seq-*_p.a
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Lifted/*.p_hi
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/*.p_hi
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Prelude/Base/*.p_hi
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/Parallel/Prelude/*.p_hi
%{_libdir}/ghc-%{version}/dph-seq-*/Data/Array/*.p_hi
%{_libdir}/ghc-%{version}/dph-seq-*/libHSdph-seq-*_p.a
%{_libdir}/ghc-%{version}/extensible-exceptions-*/Control/Exception/*.p_hi
%{_libdir}/ghc-%{version}/extensible-exceptions-*/libHSextensible-exceptions-*_p.a
%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-*_p.a
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.p_hi
%{_libdir}/ghc-%{version}/filepath-*/System/*.p_hi
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-*_p.a
%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-%{version}/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Alpha/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/X86/*.p_hi
%{_libdir}/ghc-%{version}/ghc-binary-*/libHSghc-binary-*_p.a
%{_libdir}/ghc-%{version}/ghc-binary-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/ghc-binary-*/Data/Binary/*.p_hi
%{_libdir}/ghc-%{version}/haskell98-*/libHShaskell98-*_p.a
%{_libdir}/ghc-%{version}/haskell98-*/*.p_hi
%{_libdir}/ghc-%{version}/hpc-*/libHShpc-*_p.a
%{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/GMP/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/libHSinteger-*_p.a
%{_libdir}/ghc-%{version}/old-locale-*/libHSold-locale-*_p.a
%{_libdir}/ghc-%{version}/old-locale-*/System/*.p_hi
%{_libdir}/ghc-%{version}/old-time-*/libHSold-time-*_p.a
%{_libdir}/ghc-%{version}/old-time-*/System/*.p_hi
%{_libdir}/ghc-%{version}/pretty-*/libHSpretty-*_p.a
%{_libdir}/ghc-%{version}/pretty-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/*.p_hi
%{_libdir}/ghc-%{version}/process-*/libHSprocess-*_p.a
%{_libdir}/ghc-%{version}/process-*/System/*.p_hi
%{_libdir}/ghc-%{version}/process-*/System/Process/*.p_hi
%{_libdir}/ghc-%{version}/random-*/libHSrandom-*_p.a
%{_libdir}/ghc-%{version}/random-*/System/*.p_hi
%{_libdir}/ghc-%{version}/syb-*/Data/Generics/*.p_hi
%{_libdir}/ghc-%{version}/syb-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/syb-*/libHSsyb-*_p.a
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.p_hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.p_hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Syntax/*.p_hi
%{_libdir}/ghc-%{version}/template-haskell-*/libHStemplate-haskell-*_p.a
%{_libdir}/ghc-%{version}/time-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/*.p_hi
%{_libdir}/ghc-%{version}/time-*/libHStime-*_p.a
%{_libdir}/ghc-%{version}/unix-*/libHSunix-*_p.a
%{_libdir}/ghc-%{version}/unix-*/System/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Process/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals/*.p_hi
