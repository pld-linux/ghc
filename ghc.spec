#
# NOTE
# - happy, alex needed only when using darcs checkout or regenerating parsers
#   http://hackage.haskell.org/trac/ghc/wiki/Building/Prerequisites
#
# - http://hackage.haskell.org/trac/ghc/wiki/Building/Porting
#
# TODO:
#	- teach ghc toolchain to always use ld.bfd,
#		or fix ld.gold to be usable for anything else than c/c++
#
# Conditional build:
%bcond_with	bootstrap	# use foreign (non-rpm) ghc to bootstrap (extra 140MB to download)
%bcond_with	unregistered	# non-registerised interpreter (use for build problems/new arches)
%bcond_without	doc		# don't build documentation (requires haddock)

Summary:	Glasgow Haskell Compilation system
Summary(pl.UTF-8):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	7.6.3
Release:	1
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.bz2
# Source0-md5:	986d1f90ca30d60f7b2820d75c6b8ea7
%if %{with bootstrap}
Source3:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-i386-unknown-linux.tar.bz2
# Source3-md5:	37019b712ec6e5fb0732c27fb43667ee
Source4:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-x86_64-unknown-linux.tar.bz2
# Source4-md5:	5c142b86355cfd390cd36c292e416db5
%endif
Patch0:		%{name}-pld.patch
Patch1:		%{name}-pkgdir.patch
Patch2:		%{name}-winpaths.patch
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
%patch2 -p1

%build
# use ld.bfd
install -d our-ld
ln -s %{_bindir}/ld.bfd our-ld/ld
export PATH=$(pwd)/our-ld:$PATH

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
	--with-ld=ld \
	--with-nm=nm \
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

%install
rm -rf $RPM_BUILD_ROOT
rm -rf docs-root

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/doc/%{name} docs-root

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
%{_libdir}/ghc-%{version}/settings
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-pkg
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-split
%if %{with doc}
%attr(755,root,root) %{_libdir}/ghc-%{version}/haddock
%endif
%attr(755,root,root) %{_libdir}/ghc-%{version}/hsc2hs
%attr(755,root,root) %{_libdir}/ghc-%{version}/runghc
%attr(755,root,root) %{_libdir}/ghc-%{version}/unlit
%{_libdir}/ghc-%{version}/libHS*.a
%exclude %{_libdir}/ghc-%{version}/libHS*_p.a
%{_libdir}/ghc-%{version}/ghc*-usage.txt
%if %{with doc}
%{_libdir}/ghc-%{version}/html
%endif
%dir %{_libdir}/ghc-%{version}/package.conf.d
%{_libdir}/ghc-%{version}/package.conf.d/*.conf
%config %verify(not md5 mtime size) %{_libdir}/ghc-%{version}/package.conf.d/package.cache
%{_libdir}/ghc-%{version}/template-hsc.h
%if %{with doc}
%dir %{_libdir}/ghc-%{version}/latex
%{_libdir}/ghc-%{version}/latex/haddock.sty
%endif
%{_mandir}/man1/ghc.1*

%dir %{_libdir}/ghc-%{version}/array-*
%dir %{_libdir}/ghc-%{version}/array-*/Data
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/IO
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/MArray
%{_libdir}/ghc-%{version}/array-*/Data/Array/MArray/*.hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/ST
%{_libdir}/ghc-%{version}/array-*/Data/Array/ST/*.hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/Storable
%{_libdir}/ghc-%{version}/array-*/Data/Array/Storable/*.hi
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
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Data
%{_libdir}/ghc-%{version}/base-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/STRef
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/Typeable
%{_libdir}/ghc-%{version}/base-*/Data/Typeable/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Debug
%{_libdir}/ghc-%{version}/base-*/Debug/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign
%{_libdir}/ghc-%{version}/base-*/Foreign/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/C
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr
%{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/Marshal
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC
%{_libdir}/ghc-%{version}/base-*/GHC/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Conc
%{_libdir}/ghc-%{version}/base-*/GHC/Conc/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Event
%{_libdir}/ghc-%{version}/base-*/GHC/Event/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint
%{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Float
%{_libdir}/ghc-%{version}/base-*/GHC/Float/*.hi
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
%dir %{_libdir}/ghc-%{version}/base-*/System/Environment
%{_libdir}/ghc-%{version}/base-*/System/Environment/*.hi
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
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/*.hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/BasicEncoding
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/BasicEncoding/*.hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/BasicEncoding/Internal
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/BasicEncoding/Internal/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/HSbytestring-*.o
%{_libdir}/ghc-%{version}/bytestring-*/include
%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-*.a
%exclude %{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-*_p.a

%dir %{_libdir}/ghc-%{version}/Cabal-*
%{_libdir}/ghc-%{version}/Cabal-*/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/*.hi
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

%dir %{_libdir}/ghc-%{version}/binary-*
%dir %{_libdir}/ghc-%{version}/binary-*/Data
%{_libdir}/ghc-%{version}/binary-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/binary-*/Data/Binary
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/*.hi
%dir %{_libdir}/ghc-%{version}/binary-*/Data/Binary/Builder
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/Builder/*.hi
%{_libdir}/ghc-%{version}/binary-*/HSbinary-*.o
%{_libdir}/ghc-%{version}/binary-*/libHSbinary-*.a
%exclude %{_libdir}/ghc-%{version}/binary-*/libHSbinary-*_p.a

%dir %{_libdir}/ghc-%{version}/containers-*
%dir %{_libdir}/ghc-%{version}/containers-*/Data
%{_libdir}/ghc-%{version}/containers-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntMap
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/*.hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntSet
%{_libdir}/ghc-%{version}/containers-*/Data/IntSet/*.hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Map
%{_libdir}/ghc-%{version}/containers-*/Data/Map/*.hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Set
%{_libdir}/ghc-%{version}/containers-*/Data/Set/*.hi
%{_libdir}/ghc-%{version}/containers-*/HScontainers-*.o
%{_libdir}/ghc-%{version}/containers-*/libHScontainers-*.a
%exclude %{_libdir}/ghc-%{version}/containers-*/libHScontainers-*_p.a

%dir %{_libdir}/ghc-%{version}/deepseq-*
%dir %{_libdir}/ghc-%{version}/deepseq-*/Control
%{_libdir}/ghc-%{version}/deepseq-*/Control/*.hi
%{_libdir}/ghc-%{version}/deepseq-*/HSdeepseq-*.o
%{_libdir}/ghc-%{version}/deepseq-*/libHSdeepseq-*.a
%exclude %{_libdir}/ghc-%{version}/deepseq-*/libHSdeepseq-*_p.a

%dir %{_libdir}/ghc-%{version}/directory-*
%{_libdir}/ghc-%{version}/directory-*/HSdirectory-*.o
%{_libdir}/ghc-%{version}/directory-*/include
%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-*.a
%exclude %{_libdir}/ghc-%{version}/directory-*/libHSdirectory-*_p.a
%dir %{_libdir}/ghc-%{version}/directory-*/System
%{_libdir}/ghc-%{version}/directory-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/filepath-*
%{_libdir}/ghc-%{version}/filepath-*/HSfilepath-*.o
%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-*.a
%exclude %{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-*_p.a
%dir %{_libdir}/ghc-%{version}/filepath-*/System
%dir %{_libdir}/ghc-%{version}/filepath-*/System/FilePath
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.hi
%{_libdir}/ghc-%{version}/filepath-*/System/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-%{version}
%{_libdir}/ghc-%{version}/ghc-%{version}/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}.a
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl
%{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Llvm
%{_libdir}/ghc-%{version}/ghc-%{version}/Llvm/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen
%{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen/*.hi
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
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Builtins
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Builtins/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Generic
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Generic/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Monad
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Monad/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Type
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Type/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Utils
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Utils/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-prim-*
%dir %{_libdir}/ghc-%{version}/ghc-prim-*/GHC
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-prim-*/HSghc-prim-*.o
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-*.a
%exclude %{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-*_p.a

%dir %{_libdir}/ghc-%{version}/haskell2010-*
%{_libdir}/ghc-%{version}/haskell2010-*/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/Control
%{_libdir}/ghc-%{version}/haskell2010-*/Control/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/Data
%{_libdir}/ghc-%{version}/haskell2010-*/Data/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/Foreign
%{_libdir}/ghc-%{version}/haskell2010-*/Foreign/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/Foreign/C
%{_libdir}/ghc-%{version}/haskell2010-*/Foreign/C/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/Foreign/Marshal
%{_libdir}/ghc-%{version}/haskell2010-*/Foreign/Marshal/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/System
%{_libdir}/ghc-%{version}/haskell2010-*/System/*.hi
%dir %{_libdir}/ghc-%{version}/haskell2010-*/System/IO
%{_libdir}/ghc-%{version}/haskell2010-*/System/IO/*.hi
%{_libdir}/ghc-%{version}/haskell2010-*/HShaskell2010-*.o
%{_libdir}/ghc-%{version}/haskell2010-*/libHShaskell2010-*.a
%exclude %{_libdir}/ghc-%{version}/haskell2010-*/libHShaskell2010-*_p.a

%dir %{_libdir}/ghc-%{version}/haskell98-*
%{_libdir}/ghc-%{version}/haskell98-*/*.hi
%{_libdir}/ghc-%{version}/haskell98-*/HShaskell98-*.o
%{_libdir}/ghc-%{version}/haskell98-*/libHShaskell98-*.a
%exclude %{_libdir}/ghc-%{version}/haskell98-*/libHShaskell98-*_p.a

%dir %{_libdir}/ghc-%{version}/hoopl-*
%dir %{_libdir}/ghc-%{version}/hoopl-*/Compiler
%{_libdir}/ghc-%{version}/hoopl-*/Compiler/*.hi
%dir %{_libdir}/ghc-%{version}/hoopl-*/Compiler/Hoopl
%{_libdir}/ghc-%{version}/hoopl-*/Compiler/Hoopl/*.hi
%dir %{_libdir}/ghc-%{version}/hoopl-*/Compiler/Hoopl/Passes
%{_libdir}/ghc-%{version}/hoopl-*/Compiler/Hoopl/Passes/*.hi
%{_libdir}/ghc-%{version}/hoopl-*/HShoopl-*.o
%{_libdir}/ghc-%{version}/hoopl-*/libHShoopl-*.a
%exclude %{_libdir}/ghc-%{version}/hoopl-*/libHShoopl-*_p.a

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
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/Logarithms
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/Logarithms/*.hi
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

#%dir %{_libdir}/ghc-%{version}/random-*
#%{_libdir}/ghc-%{version}/random-*/HSrandom-*.o
#%{_libdir}/ghc-%{version}/random-*/libHSrandom-*.a
#%exclude %{_libdir}/ghc-%{version}/random-*/libHSrandom-*_p.a
#%dir %{_libdir}/ghc-%{version}/random-*/System
#%{_libdir}/ghc-%{version}/random-*/System/*.hi

#%dir %{_libdir}/ghc-%{version}/syb-*
#%dir %{_libdir}/ghc-%{version}/syb-*/Data
##%dir %{_libdir}/ghc-%{version}/syb-*/Data/Generics
#%{_libdir}/ghc-%{version}/syb-*/Data/Generics/*.hi
#%{_libdir}/ghc-%{version}/syb-*/Data/*.hi
#%{_libdir}/ghc-%{version}/syb-*/HSsyb-*.o
#%{_libdir}/ghc-%{version}/syb-*/libHSsyb-*.a
#%exclude %{_libdir}/ghc-%{version}/syb-*/libHSsyb-*_p.a

%dir %{_libdir}/ghc-%{version}/template-haskell-*
%{_libdir}/ghc-%{version}/template-haskell-*/HStemplate-haskell-*.o
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.hi
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.hi
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
%{_libdir}/ghc-%{version}/unix-*/System/Posix/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/ByteString
%{_libdir}/ghc-%{version}/unix-*/System/Posix/ByteString/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Directory
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Directory/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/Module
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/Module/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Env
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Env/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Files
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Files/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/IO
%{_libdir}/ghc-%{version}/unix-*/System/Posix/IO/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Process
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Process/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Temp
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Temp/*.hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Terminal
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Terminal/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/libHS*_p.a
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/MArray/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/ST/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/Storable/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/array-*/libHSarray-*_p.a
%{_libdir}/ghc-%{version}/base-*/Control/Concurrent/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Exception/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/Typeable/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Debug/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Conc/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Event/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Float/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/libHSbase-*_p.a
%{_libdir}/ghc-%{version}/base-*/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Console/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Environment/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Mem/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Posix/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/Read/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/Show/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Unsafe/*.p_hi
%{_libdir}/ghc-%{version}/binary-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/*.p_hi
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/Builder/*.p_hi
%{_libdir}/ghc-%{version}/binary-*/libHSbinary-*_p.a
%{_libdir}/ghc-%{version}/bin-package-db-*/Distribution/InstalledPackageInfo/*.p_hi
%{_libdir}/ghc-%{version}/bin-package-db-*/libHSbin-package-db-0.0.0.0_p.a
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/BasicEncoding/Internal/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/BasicEncoding/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-*_p.a
%{_libdir}/ghc-%{version}/Cabal-*/*.p_hi
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
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntSet/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Set/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/libHScontainers-*_p.a
%{_libdir}/ghc-%{version}/deepseq-*/libHSdeepseq-*_p.a
%{_libdir}/ghc-%{version}/deepseq-*/Control/*.p_hi
%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-*_p.a
%{_libdir}/ghc-%{version}/directory-*/System/*.p_hi
%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-*_p.a
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.p_hi
%{_libdir}/ghc-%{version}/filepath-*/System/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-%{version}/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Llvm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Builtins/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Generic/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Monad/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Type/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Vectorise/Utils/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/X86/*.p_hi
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-*_p.a
%{_libdir}/ghc-%{version}/haskell2010-*/Control/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/Foreign/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/Foreign/C/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/Foreign/Marshal/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/System/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/System/IO/*.p_hi
%{_libdir}/ghc-%{version}/haskell2010-*/libHShaskell2010-*_p.a
%{_libdir}/ghc-%{version}/haskell98-*/libHShaskell98-*_p.a
%{_libdir}/ghc-%{version}/haskell98-*/*.p_hi
%{_libdir}/ghc-%{version}/hoopl-*/Compiler/*.p_hi
%{_libdir}/ghc-%{version}/hoopl-*/Compiler/Hoopl/*.p_hi
%{_libdir}/ghc-%{version}/hoopl-*/Compiler/Hoopl/Passes/*.p_hi
%{_libdir}/ghc-%{version}/hoopl-*/libHShoopl-*_p.a
%{_libdir}/ghc-%{version}/hpc-*/libHShpc-*_p.a
%{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/GMP/*.p_hi
%{_libdir}/ghc-%{version}/integer-*/GHC/Integer/Logarithms/*.p_hi
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
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.p_hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.p_hi
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
%{_libdir}/ghc-%{version}/unix-*/System/Posix/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/ByteString/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Directory/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/Module/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Env/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Files/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/IO/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Process/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Temp/*.p_hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Terminal/*.p_hi
