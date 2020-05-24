#
# NOTE
# - happy, alex needed only when using darcs checkout or regenerating parsers
#   http://hackage.haskell.org/trac/ghc/wiki/Building/Prerequisites
#
# - http://hackage.haskell.org/trac/ghc/wiki/Building/Porting
#
# Conditional build:
%bcond_with	bootstrap	# use foreign (non-rpm) ghc to bootstrap (extra 140MB to download)
%ifarch x32
%bcond_without	unregisterised	# non-registerised interpreter (use for build problems/new arches)
%else
%bcond_with	unregisterised	# non-registerised interpreter (use for build problems/new arches)
%endif
%bcond_without	system_libffi	# use bundled or system provided libffi
%bcond_without	doc		# don't build documentation (requires haddock)

# included ghc package versions:
%define		gpv_Cabal		3.2.0.0
%define		gpv_array		0.5.4.0
%define		gpv_base		4.14.0.0
%define		gpv_bin_package_db	0.0.0.0
%define		gpv_binary		0.8.8.0
%define		gpv_bytestring		0.10.10.0
%define		gpv_containers		0.6.2.1
%define		gpv_deepseq		1.4.4.0
%define		gpv_directory		1.3.6.0
%define		gpv_exceptions		0.10.4
%define		gpv_filepath		1.4.2.1
%define		gpv_compact		0.1.0.0
%define		gpv_prim		0.6.1
%define		gpv_haskeline		0.8.0.0
%define		gpv_hpc			0.6.1.0
%define		gpv_integer_gmp		1.0.3.0
%define		gpv_integer_simple	0.1.2.0
%define		gpv_mtl			2.2.2
%define		gpv_parsec		3.1.14.0
%define		gpv_pretty		1.1.3.6
%define		gpv_process		1.6.8.2
%define		gpv_stm			2.5.0.0
%define		gpv_template_haskell	2.16.0.0
%define		gpv_terminfo		0.4.1.4
%define		gpv_text		1.2.3.2
%define		gpv_time		1.9.3
%define		gpv_transformers	0.5.6.2
%define		gpv_unix		2.7.2.2
%define		gpv_xhtml		3000.2.2.1

%define		bootversion		8.6.5

Summary:	Glasgow Haskell Compilation system
Summary(pl.UTF-8):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	8.10.1
Release:	4
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.xz
# Source0-md5:	1368854e72bc69d7ef2377cffcfbce3b
%if %{with bootstrap}
Source3:	https://downloads.haskell.org/~ghc/%{bootversion}/%{name}-%{bootversion}-i386-deb9-linux.tar.xz
# Source3-md5:	1bc84d8d51d8b0411a13172070295617
Source4:	https://downloads.haskell.org/~ghc/%{bootversion}/%{name}-%{bootversion}-x86_64-deb9-linux.tar.xz
# Source4-md5:	8de779b73c1b2f1b7ab49030015fce3d
Source5:	http://ftp.ports.debian.org/debian-ports/pool-x32/main/g/ghc/ghc_8.8.3-1~exp2_x32.deb
# Source5-md5:	b912b87c8d9450d140ae773083edecb0
%endif
Patch0:		%{name}-pld.patch
Patch1:		%{name}-pkgdir.patch
Patch3:		build.patch
Patch4:		buildpath-abi-stability.patch
Patch5:		x32-use-native-x86_64-insn.patch
URL:		http://haskell.org/ghc/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	binutils >= 4:2.30
BuildRequires:	freealut-devel
BuildRequires:	gmp-devel
%{?with_system_libffi:BuildRequires:	libffi-devel}
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.607
BuildRequires:	sed >= 4.0
%if %{with bootstrap}
%ifarch %{x8664} %{ix86}
BuildRequires:	compat-ncurses5
%endif
%else
BuildRequires:	alex >= 2.0
BuildRequires:	ghc >= 8.6
BuildRequires:	happy >= 1.16
%endif
%if %{with doc}
BuildRequires:	dblatex
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	texlive
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-rsfs
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-bibtex
BuildRequires:	texlive-latex-other
BuildRequires:	texlive-makeindex
BuildRequires:	texlive-tex4ht
BuildRequires:	texlive-tex-xkeyval
BuildRequires:	texlive-xetex
#BuildRequires:	tetex-latex-ltxcmds
BuildRequires:	latexmk
#For generating documentation in PDF: fop or xmltex
BuildRequires:	sphinx-pdg-3
%endif
Provides:	ghc-array = %{gpv_array}
Provides:	ghc-base = %{gpv_base}
Provides:	ghc-binary = %{gpv_binary}
Provides:	ghc-bin_package_db = %{gpv_bin_package_db}
Provides:	ghc-bytestring = %{gpv_bytestring}
Provides:	ghc-Cabal = %{gpv_Cabal}
Provides:	ghc-containers = %{gpv_containers}
Provides:	ghc-deepseq = %{gpv_deepseq}
Provides:	ghc-directory = %{gpv_directory}
Provides:	ghc-exceptions = %{gpv_exceptions}
Provides:	ghc-filepath = %{gpv_filepath}
Provides:	ghc-compact = %{gpv_compact}
Provides:	ghc-prim = %{gpv_prim}
Provides:	ghc-haskeline = %{gpv_haskeline}
Provides:	ghc-hpc = %{gpv_hpc}
%ifnarch x32
Provides:	ghc-integer-gmp = %{gpv_integer_gmp}
%else
Provides:	ghc-integer-simple = %{gpv_integer_simple}
%endif
Provides:	ghc-mtl = %{gpv_mtl}
Provides:	ghc-parsec = %{gpv_parsec}
Provides:	ghc-pretty = %{gpv_pretty}
Provides:	ghc-process = %{gpv_process}
Provides:	ghc-stm = %{gpv_stm}
Provides:	ghc-template-haskell = %{gpv_template_haskell}
Provides:	ghc-terminfo = %{gpv_terminfo}
Provides:	ghc-text = %{gpv_text}
Provides:	ghc-time = %{gpv_time}
Provides:	ghc-transformers = %{gpv_transformers}
Provides:	ghc-unix = %{gpv_unix}
Provides:	ghc-xhtml = %{gpv_xhtml}
Suggests:	ghc-haskell-platform
Provides:	haddock
Obsoletes:	haddock
ExclusiveArch:	%{ix86} %{x8664} x32
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
Provides:	ghc-array-prof = %{gpv_array}
Provides:	ghc-base-prof = %{gpv_base}
Provides:	ghc-binary-prof = %{gpv_binary}
Provides:	ghc-bin_package_db-prof = %{gpv_bin_package_db}
Provides:	ghc-bytestring-prof = %{gpv_bytestring}
Provides:	ghc-Cabal-prof = %{gpv_Cabal}
Provides:	ghc-containers-prof = %{gpv_containers}
Provides:	ghc-deepseq-prof = %{gpv_deepseq}
Provides:	ghc-directory-prof = %{gpv_directory}
Provides:	ghc-exceptions-prof = %{gpv_exceptions}
Provides:	ghc-filepath-prof = %{gpv_filepath}
Provides:	ghc-compact-prof = %{gpv_compact}
Provides:	ghc-prim-prof = %{gpv_prim}
Provides:	ghc-haskeline-prof = %{gpv_haskeline}
Provides:	ghc-hpc-prof = %{gpv_hpc}
%ifnarch x32
Provides:	ghc-integer-gmp-prof = %{gpv_integer_gmp}
%else
Provides:	ghc-integer-simple-prof = %{gpv_integer_simple}
%endif
Provides:	ghc-mtl-prof = %{gpv_mtl}
Provides:	ghc-parsec-prof = %{gpv_parsec}
Provides:	ghc-pretty-prof = %{gpv_pretty}
Provides:	ghc-process-prof = %{gpv_process}
Provides:	ghc-stm-prof = %{gpv_stm}
Provides:	ghc-template-haskell-prof = %{gpv_template_haskell}
Provides:	ghc-terminfo-prof = %{gpv_terminfo}
Provides:	ghc-text-prof = %{gpv_text}
Provides:	ghc-time-prof = %{gpv_time}
Provides:	ghc-transformers-prof = %{gpv_transformers}
Provides:	ghc-unix-prof = %{gpv_unix}
Provides:	ghc-xhtml-prof = %{gpv_xhtml}

%description prof
Profiling libraries for Glorious Glasgow Haskell Compilation System
(GHC). They should be installed when GHC's profiling subsystem is
needed.

%description prof -l pl.UTF-8
Biblioteki profilujące dla GHC. Powinny być zainstalowane kiedy
potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	Documentation for GHC
Summary(pl.UTF-8):	Dokumentacja do GHC
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for GHC.

%description doc -l pl.UTF-8
Dokumentacja do GHC.

%prep
%setup -q
%if %{with bootstrap}

# official binaries
%ifarch %{ix86} %{x8664}
%ifarch %{ix86}
%{__tar} -xf %{SOURCE3}
%endif
%ifarch %{x8664}
%{__tar} -xf %{SOURCE4}
%endif
mv %{name}-%{bootversion} binsrc
%endif

# debian binaries for x32
%ifarch x32
install -d bindist
cd bindist
ar x %{SOURCE5}
tar xf data.tar.xz
ln -s usr/bin bin
sed -i -e "s#/usr#$(pwd)/usr#g" bin/{ghc,ghc-pkg,haddock,runghc} var/lib/ghc/*/*.conf
cp -a usr/lib/ghc/settings{,.org}
sed -i -e 's#x86_64.*-ld.gold#ld.gold#g' usr/lib/ghc/settings
sed -i -e 's#x86_64-linux-gnux32#%{_target_base_arch}-%{_target_vendor}-%{_target_os}%{?_gnu}#g' \
	-e 's#gnux32-ar#gnux32-gcc-ar#g' \
	-e 's#gnux32-ranlib#gnux32-gcc-ranlib#g' \
	usr/lib/ghc/settings
# make it relative
ln -sf ../../../var/lib/ghc/package.conf.d usr/lib/ghc/package.conf.d

# debian uses separate libtinfo, workaround
ln -s %{_libdir}/libncurses.so.6 usr/lib/libtinfo.so.6
LD_LIBRARY_PATH=$(pwd)/usr/lib; export LD_LIBRARY_PATH

bin/ghc-pkg recache --global
cd ..
%endif
%endif

%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
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
BUILD_SPHINX_HTML   = %{!?with_doc:NO}%{?with_doc:YES}
BUILD_SPHINX_PDF    = NO
XSLTPROC_OPTS       += --nonet
EOF

%if %{with unregisterised}
# An unregisterised build is one that compiles via vanilla C only
# http://hackage.haskell.org/trac/ghc/wiki/Building/Unregisterised
cat <<'EOF' >> mk/build.mk
GhcUnregisterised=YES
GhcWithNativeCodeGen=NO
SplitObjs=NO
EOF

%ifarch %{ix86} x32
# Virtual memory exhausted when trying to build unregisterised compiler on
# 32-bit targets. Disable optimizations for compiler/GHC/Hs/Instances.hs
# See https://bugs.debian.org/933968
# See https://gitlab.haskell.org/ghc/ghc/issues/17048
echo "compiler/GHC/Hs/Instances_HC_OPTS += -O0" >> mk/build.mk
%endif
%endif

%ifarch x32
echo "INTEGER_LIBRARY = integer-simple" >> mk/build.mk

# debian uses separate libtinfo, workaround
LD_LIBRARY_PATH=$(pwd)/bindist/usr/lib; export LD_LIBRARY_PATH
%endif

top=$(pwd)
%if %{with bootstrap}

# don't depend on ncurses and do minimal things for bootstrap
echo "libraries/haskeline_CONFIGURE_OPTS += --flag=-terminfo" >> mk/build.mk
echo "utils/ghc-pkg_HC_OPTS += -DBOOTSTRAPPING" >> mk/build.mk

%ifarch %{ix86} %{x8664}
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

PATH=$top/bindist/bin:$PATH:%{_prefix}/local/bin
%endif

%configure \
%if %{with bootstrap}
	CC_STAGE0="%{__cc}" \
	GHC=$PWD/bindist/bin/ghc \
%endif
%if %{with doc}
	SPHINXBUILD=/usr/bin/sphinx-build-3 \
%endif
	--target=%{_target_platform} \
	--prefix=%{_prefix} \
	--disable-ld-override \
	%{?with_system_libffi:--with-system-libffi} \
	%{?with_unregisterised:--enable-unregisterised} \
	%{nil}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf docs-root

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with doc}
mv -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} docs-root

# fix paths to docs in package list
sed -i -e 's|%{_datadir}/doc/%{name}|%{_docdir}/%{name}-%{version}|g' $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/package.conf.d/*.conf
%endif

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
%doc README.md
%attr(755,root,root) %{_bindir}/ghc
%attr(755,root,root) %{_bindir}/ghc-%{version}
%attr(755,root,root) %{_bindir}/ghc-pkg
%attr(755,root,root) %{_bindir}/ghc-pkg-%{version}
%attr(755,root,root) %{_bindir}/ghci
%attr(755,root,root) %{_bindir}/ghci-%{version}
%if %{with doc}
%attr(755,root,root) %{_bindir}/haddock
%attr(755,root,root) %{_bindir}/haddock-ghc-%{version}
%endif
%attr(755,root,root) %{_bindir}/hp2ps
%attr(755,root,root) %{_bindir}/hpc
%attr(755,root,root) %{_bindir}/hsc2hs
%attr(755,root,root) %{_bindir}/runghc
%attr(755,root,root) %{_bindir}/runghc-%{version}
%attr(755,root,root) %{_bindir}/runhaskell
%dir %{_libdir}/ghc-%{version}
%dir %{_libdir}/ghc-%{version}/bin
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/ghc
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/ghc-iserv
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/ghc-iserv-dyn
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/ghc-iserv-prof
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/ghc-pkg
%if %{with doc}
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/haddock
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/hp2ps
%endif
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/hpc
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/hsc2hs
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/runghc
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/unlit
%{_libdir}/ghc-%{version}/ghc*-usage.txt
%{_libdir}/ghc-%{version}/settings
%{_libdir}/ghc-%{version}/template-hsc.h
%{_libdir}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/llvm-passes
%{_libdir}/ghc-%{version}/llvm-targets
%{_libdir}/ghc-%{version}/platformConstants
%if %{with doc}
%{_libdir}/ghc-%{version}/html
%dir %{_libdir}/ghc-%{version}/latex
%{_libdir}/ghc-%{version}/latex/haddock.sty
%{_mandir}/man1/ghc.1*
%endif
%dir %{_libdir}/ghc-%{version}/package.conf.d
%ghost %{_libdir}/ghc-%{version}/package.conf.d/package.cache

%{_libdir}/ghc-%{version}/package.conf.d/array-%{gpv_array}.conf
%{_libdir}/ghc-%{version}/package.conf.d/base-%{gpv_base}.conf
%{_libdir}/ghc-%{version}/package.conf.d/binary-%{gpv_binary}.conf
%{_libdir}/ghc-%{version}/package.conf.d/bytestring-%{gpv_bytestring}.conf
%{_libdir}/ghc-%{version}/package.conf.d/Cabal-%{gpv_Cabal}.conf
%{_libdir}/ghc-%{version}/package.conf.d/containers-%{gpv_containers}.conf
%{_libdir}/ghc-%{version}/package.conf.d/deepseq-%{gpv_deepseq}.conf
%{_libdir}/ghc-%{version}/package.conf.d/directory-%{gpv_directory}.conf
%{_libdir}/ghc-%{version}/package.conf.d/exceptions-%{gpv_exceptions}.conf
%{_libdir}/ghc-%{version}/package.conf.d/filepath-%{gpv_filepath}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-boot-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-boot-th-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-compact-%{gpv_compact}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-heap-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-prim-%{gpv_prim}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghci-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/haskeline-%{gpv_haskeline}.conf
%{_libdir}/ghc-%{version}/package.conf.d/hpc-%{gpv_hpc}.conf
%ifnarch x32
%{_libdir}/ghc-%{version}/package.conf.d/integer-gmp-%{gpv_integer_gmp}.conf
%else
%{_libdir}/ghc-%{version}/package.conf.d/integer-simple-%{gpv_integer_simple}.conf
%endif
%{_libdir}/ghc-%{version}/package.conf.d/libiserv-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/mtl-%{gpv_mtl}.conf
%{_libdir}/ghc-%{version}/package.conf.d/package.cache.lock
%{_libdir}/ghc-%{version}/package.conf.d/parsec-%{gpv_parsec}.conf
%{_libdir}/ghc-%{version}/package.conf.d/pretty-%{gpv_pretty}.conf
%{_libdir}/ghc-%{version}/package.conf.d/process-%{gpv_process}.conf
%{_libdir}/ghc-%{version}/package.conf.d/rts.conf
%{_libdir}/ghc-%{version}/package.conf.d/stm-%{gpv_stm}.conf
%{_libdir}/ghc-%{version}/package.conf.d/template-haskell-%{gpv_template_haskell}.conf
%{_libdir}/ghc-%{version}/package.conf.d/terminfo-%{gpv_terminfo}.conf
%{_libdir}/ghc-%{version}/package.conf.d/text-%{gpv_text}.conf
%{_libdir}/ghc-%{version}/package.conf.d/time-%{gpv_time}.conf
%{_libdir}/ghc-%{version}/package.conf.d/transformers-%{gpv_transformers}.conf
%{_libdir}/ghc-%{version}/package.conf.d/unix-%{gpv_unix}.conf
%{_libdir}/ghc-%{version}/package.conf.d/xhtml-%{gpv_xhtml}.conf

%dir %{_libdir}/ghc-%{version}/Cabal-*
%{_libdir}/ghc-%{version}/Cabal-*/HSCabal-%{gpv_Cabal}.o
%{_libdir}/ghc-%{version}/Cabal-*/libHSCabal-%{gpv_Cabal}.a
%{_libdir}/ghc-%{version}/Cabal-*/libHSCabal-%{gpv_Cabal}-ghc*.so
%{_libdir}/ghc-%{version}/Cabal-*/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Backpack
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Backpack/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Backpack/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Internal
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Internal/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Prelude
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Prelude/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Prelude/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/FieldGrammar
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/FieldGrammar/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/FieldGrammar/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Fields
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Fields/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Fields/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Parsec
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Parsec/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Parsec/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/SPDX
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/SPDX/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/SPDX/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/InstallDirs
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/InstallDirs/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/InstallDirs/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Test
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Test/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Test/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Utils
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Utils/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Utils/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Benchmark
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Benchmark/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Benchmark/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/BuildInfo
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/BuildInfo/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/BuildInfo/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Executable
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Executable/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Executable/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/ForeignLib
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/ForeignLib/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/ForeignLib/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/GenericPackageDescription
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/GenericPackageDescription/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/GenericPackageDescription/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/InstalledPackageInfo
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/InstalledPackageInfo/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/InstalledPackageInfo/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Library
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Library/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Library/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageDescription
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageDescription/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageDescription/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageId
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageId/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageId/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageName
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageName/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageName/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SetupBuildInfo
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SetupBuildInfo/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SetupBuildInfo/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SourceRepo
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SourceRepo/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SourceRepo/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/TestSuite
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/TestSuite/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/TestSuite/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionRange
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionRange/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionRange/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Utils
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Utils/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Utils/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Verbosity
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Verbosity/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Verbosity/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Language
%dir %{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell
%{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell/*.hi
%{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/array-*
%{_libdir}/ghc-%{version}/array-*/HSarray-%{gpv_array}.o
%{_libdir}/ghc-%{version}/array-*/libHSarray-%{gpv_array}.a
%{_libdir}/ghc-%{version}/array-*/libHSarray-%{gpv_array}-ghc*.so
%dir %{_libdir}/ghc-%{version}/array-*/Data
%{_libdir}/ghc-%{version}/array-*/Data/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/IO
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/MArray
%{_libdir}/ghc-%{version}/array-*/Data/Array/MArray/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/MArray/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/ST
%{_libdir}/ghc-%{version}/array-*/Data/Array/ST/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/ST/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/array-*/Data/Array/Storable
%{_libdir}/ghc-%{version}/array-*/Data/Array/Storable/*.hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/Storable/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/base-*
%{_libdir}/ghc-%{version}/base-*/HSbase-%{gpv_base}.o
%{_libdir}/ghc-%{version}/base-*/libHSbase-%{gpv_base}.a
%{_libdir}/ghc-%{version}/base-*/libHSbase-%{gpv_base}-ghc*.so
%{_libdir}/ghc-%{version}/base-*/include
%{_libdir}/ghc-%{version}/base-*/*.hi
%{_libdir}/ghc-%{version}/base-*/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control
%{_libdir}/ghc-%{version}/base-*/Control/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Concurrent
%{_libdir}/ghc-%{version}/base-*/Control/Concurrent/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/Concurrent/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Exception
%{_libdir}/ghc-%{version}/base-*/Control/Exception/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/Exception/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad
%{_libdir}/ghc-%{version}/base-*/Control/Monad/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad/IO
%{_libdir}/ghc-%{version}/base-*/Control/Monad/IO/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/IO/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad/ST
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy/*.hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data
%{_libdir}/ghc-%{version}/base-*/Data/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/Functor
%{_libdir}/ghc-%{version}/base-*/Data/Functor/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/Functor/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/List
%{_libdir}/ghc-%{version}/base-*/Data/List/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/List/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/Semigroup
%{_libdir}/ghc-%{version}/base-*/Data/Semigroup/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/Semigroup/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/Type
%{_libdir}/ghc-%{version}/base-*/Data/Type/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/Type/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/STRef
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Data/Typeable
%{_libdir}/ghc-%{version}/base-*/Data/Typeable/*.hi
%{_libdir}/ghc-%{version}/base-*/Data/Typeable/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Debug
%{_libdir}/ghc-%{version}/base-*/Debug/*.hi
%{_libdir}/ghc-%{version}/base-*/Debug/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign
%{_libdir}/ghc-%{version}/base-*/Foreign/*.hi
%{_libdir}/ghc-%{version}/base-*/Foreign/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/C
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.hi
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr
%{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr/*.hi
%{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Foreign/Marshal
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.hi
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC
%{_libdir}/ghc-%{version}/base-*/GHC/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Conc
%{_libdir}/ghc-%{version}/base-*/GHC/Conc/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Conc/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Event
%{_libdir}/ghc-%{version}/base-*/GHC/Event/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Event/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Exception
%{_libdir}/ghc-%{version}/base-*/GHC/Exception/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Exception/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/ExecutionStack
%{_libdir}/ghc-%{version}/base-*/GHC/ExecutionStack/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/ExecutionStack/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint
%{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Float
%{_libdir}/ghc-%{version}/base-*/GHC/Float/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Float/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/GHCi
%{_libdir}/ghc-%{version}/base-*/GHC/GHCi/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/GHCi/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/Lock
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/Lock/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/Lock/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/RTS
%{_libdir}/ghc-%{version}/base-*/GHC/RTS/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/RTS/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Stack
%{_libdir}/ghc-%{version}/base-*/GHC/Stack/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Stack/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr
%{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System
%{_libdir}/ghc-%{version}/base-*/System/*.hi
%{_libdir}/ghc-%{version}/base-*/System/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/Console
%{_libdir}/ghc-%{version}/base-*/System/Console/*.hi
%{_libdir}/ghc-%{version}/base-*/System/Console/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/Environment
%{_libdir}/ghc-%{version}/base-*/System/Environment/*.hi
%{_libdir}/ghc-%{version}/base-*/System/Environment/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/IO
%{_libdir}/ghc-%{version}/base-*/System/IO/*.hi
%{_libdir}/ghc-%{version}/base-*/System/IO/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/Mem
%{_libdir}/ghc-%{version}/base-*/System/Mem/*.hi
%{_libdir}/ghc-%{version}/base-*/System/Mem/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Numeric
%{_libdir}/ghc-%{version}/base-*/Numeric/*.hi
%{_libdir}/ghc-%{version}/base-*/Numeric/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/CPUTime
%{_libdir}/ghc-%{version}/base-*/System/CPUTime/*.hi
%{_libdir}/ghc-%{version}/base-*/System/CPUTime/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/CPUTime/Posix
%{_libdir}/ghc-%{version}/base-*/System/CPUTime/Posix/*.hi
%{_libdir}/ghc-%{version}/base-*/System/CPUTime/Posix/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/System/Posix
%{_libdir}/ghc-%{version}/base-*/System/Posix/*.hi
%{_libdir}/ghc-%{version}/base-*/System/Posix/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Text
%{_libdir}/ghc-%{version}/base-*/Text/*.hi
%{_libdir}/ghc-%{version}/base-*/Text/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators
%{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators/*.hi
%{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Text/Read
%{_libdir}/ghc-%{version}/base-*/Text/Read/*.hi
%{_libdir}/ghc-%{version}/base-*/Text/Read/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Text/Show
%{_libdir}/ghc-%{version}/base-*/Text/Show/*.hi
%{_libdir}/ghc-%{version}/base-*/Text/Show/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Type
%{_libdir}/ghc-%{version}/base-*/Type/*.hi
%{_libdir}/ghc-%{version}/base-*/Type/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Type/Reflection
%{_libdir}/ghc-%{version}/base-*/Type/Reflection/*.hi
%{_libdir}/ghc-%{version}/base-*/Type/Reflection/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/Unsafe
%{_libdir}/ghc-%{version}/base-*/Unsafe/*.hi
%{_libdir}/ghc-%{version}/base-*/Unsafe/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/binary-*
%{_libdir}/ghc-%{version}/binary-*/HSbinary-%{gpv_binary}.o
%{_libdir}/ghc-%{version}/binary-*/libHSbinary-%{gpv_binary}.a
%{_libdir}/ghc-%{version}/binary-*/libHSbinary-%{gpv_binary}-ghc*.so
%dir %{_libdir}/ghc-%{version}/binary-*/Data
%{_libdir}/ghc-%{version}/binary-*/Data/*.hi
%{_libdir}/ghc-%{version}/binary-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/binary-*/Data/Binary
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/*.hi
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/binary-*/Data/Binary/Get
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/Get/*.hi
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/Get/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/bytestring-*
%{_libdir}/ghc-%{version}/bytestring-*/HSbytestring-%{gpv_bytestring}.o
%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-%{gpv_bytestring}.a
%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-%{gpv_bytestring}-ghc*.so
%{_libdir}/ghc-%{version}/bytestring-*/include
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/Internal
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/Internal/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Short
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Short/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Short/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/containers-*
%{_libdir}/ghc-%{version}/containers-*/HScontainers-%{gpv_containers}.o
%{_libdir}/ghc-%{version}/containers-*/libHScontainers-%{gpv_containers}.a
%{_libdir}/ghc-%{version}/containers-*/libHScontainers-%{gpv_containers}-ghc*.so
%dir %{_libdir}/ghc-%{version}/containers-*/Data
%{_libdir}/ghc-%{version}/containers-*/Data/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Containers
%{_libdir}/ghc-%{version}/containers-*/Data/Containers/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Containers/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntMap
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Internal
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Internal/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Merge
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Merge/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Merge/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Strict
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Strict/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Strict/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/IntSet
%{_libdir}/ghc-%{version}/containers-*/Data/IntSet/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntSet/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Map
%{_libdir}/ghc-%{version}/containers-*/Data/Map/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Map/Internal
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Internal/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Map/Merge
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Merge/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Merge/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Map/Strict
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Strict/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Strict/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Sequence
%{_libdir}/ghc-%{version}/containers-*/Data/Sequence/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Sequence/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Sequence/Internal
%{_libdir}/ghc-%{version}/containers-*/Data/Sequence/Internal/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Sequence/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Data/Set
%{_libdir}/ghc-%{version}/containers-*/Data/Set/*.hi
%{_libdir}/ghc-%{version}/containers-*/Data/Set/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/containers-*/Utils
%dir %{_libdir}/ghc-%{version}/containers-*/Utils/Containers
%dir %{_libdir}/ghc-%{version}/containers-*/Utils/Containers/Internal
%{_libdir}/ghc-%{version}/containers-*/Utils/Containers/Internal/*.hi
%{_libdir}/ghc-%{version}/containers-*/Utils/Containers/Internal/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/deepseq-*
%{_libdir}/ghc-%{version}/deepseq-*/HSdeepseq-%{gpv_deepseq}.o
%{_libdir}/ghc-%{version}/deepseq-*/libHSdeepseq-%{gpv_deepseq}.a
%{_libdir}/ghc-%{version}/deepseq-*/libHSdeepseq-%{gpv_deepseq}-ghc*.so
%dir %{_libdir}/ghc-%{version}/deepseq-*/Control
%{_libdir}/ghc-%{version}/deepseq-*/Control/*.hi
%{_libdir}/ghc-%{version}/deepseq-*/Control/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/deepseq-*/Control/DeepSeq
%{_libdir}/ghc-%{version}/deepseq-*/Control/DeepSeq/*.hi
%{_libdir}/ghc-%{version}/deepseq-*/Control/DeepSeq/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/directory-*
%{_libdir}/ghc-%{version}/directory-*/HSdirectory-%{gpv_directory}.o
%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-%{gpv_directory}.a
%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-%{gpv_directory}-ghc*.so
%dir %{_libdir}/ghc-%{version}/directory-*/System
%{_libdir}/ghc-%{version}/directory-*/System/*.hi
%{_libdir}/ghc-%{version}/directory-*/System/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/directory-*/System/Directory
%{_libdir}/ghc-%{version}/directory-*/System/Directory/*.hi
%{_libdir}/ghc-%{version}/directory-*/System/Directory/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/directory-*/System/Directory/Internal
%{_libdir}/ghc-%{version}/directory-*/System/Directory/Internal/*.hi
%{_libdir}/ghc-%{version}/directory-*/System/Directory/Internal/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/exceptions-*
%{_libdir}/ghc-%{version}/exceptions-*/HSexceptions-%{gpv_exceptions}.o
%{_libdir}/ghc-%{version}/exceptions-*/libHSexceptions-%{gpv_exceptions}.a
%{_libdir}/ghc-%{version}/exceptions-*/libHSexceptions-%{gpv_exceptions}-ghc*.so
%dir %{_libdir}/ghc-%{version}/exceptions-*/Control
%dir %{_libdir}/ghc-%{version}/exceptions-*/Control/Monad
%{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/*.hi
%{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/Catch
%{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/Catch/*.hi
%{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/Catch/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/filepath-*
%{_libdir}/ghc-%{version}/filepath-*/HSfilepath-%{gpv_filepath}.o
%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-%{gpv_filepath}.a
%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-%{gpv_filepath}-ghc*.so
%dir %{_libdir}/ghc-%{version}/filepath-*/System
%{_libdir}/ghc-%{version}/filepath-*/System/*.hi
%{_libdir}/ghc-%{version}/filepath-*/System/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/filepath-*/System/FilePath
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.hi
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghc-%{version}
%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}.a
%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}-ghc*.so
%{_libdir}/ghc-%{version}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/ghc-%{version}/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Dwarf
%{_libdir}/ghc-%{version}/ghc-%{version}/Dwarf/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Dwarf/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/PmCheck
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/PmCheck/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/PmCheck/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl
%{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Llvm
%{_libdir}/ghc-%{version}/ghc-%{version}/Llvm/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Llvm/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen
%{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/PPC
%{_libdir}/ghc-%{version}/ghc-%{version}/PPC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/PPC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/SPARC
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/X86
%{_libdir}/ghc-%{version}/ghc-%{version}/X86/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/X86/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86_64
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86_64/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86_64/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/StgLiftLams
%{_libdir}/ghc-%{version}/ghc-%{version}/StgLiftLams/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/StgLiftLams/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/SysTools
%{_libdir}/ghc-%{version}/ghc-%{version}/SysTools/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SysTools/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/HSghc-boot-%{version}.o
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/libHSghc-boot-%{version}.a
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/libHSghc-boot-%{version}-ghc*.so
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghc-boot-th-%{version}
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/HSghc-boot-th-%{version}.o
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/libHSghc-boot-th-%{version}.a
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/libHSghc-boot-th-%{version}-ghc*.so
%dir %{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/ForeignSrcLang
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/ForeignSrcLang/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/ForeignSrcLang/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/LanguageExtensions
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/LanguageExtensions/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/LanguageExtensions/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghc-compact-*
%{_libdir}/ghc-%{version}/ghc-compact-*/HSghc-compact-%{gpv_compact}.o
%{_libdir}/ghc-%{version}/ghc-compact-*/libHSghc-compact-%{gpv_compact}.a
%{_libdir}/ghc-%{version}/ghc-compact-*/libHSghc-compact-%{gpv_compact}-ghc*.so
%dir %{_libdir}/ghc-%{version}/ghc-compact-*/GHC
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-compact-*/GHC/Compact
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/Compact/*.hi
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/Compact/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghc-heap-%{version}
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/HSghc-heap-%{version}.o
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/libHSghc-heap-%{version}.a
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/libHSghc-heap-%{version}-ghc*.so
%dir %{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC
%dir %{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/*.hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/*.hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/InfoTable
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/InfoTable/*.hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/InfoTable/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghc-prim-*
%{_libdir}/ghc-%{version}/ghc-prim-*/HSghc-prim-%{gpv_prim}.o
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-%{gpv_prim}.a
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-%{gpv_prim}-ghc*.so
%dir %{_libdir}/ghc-%{version}/ghc-prim-*/GHC
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-prim-*/GHC/Prim
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/Prim/*.hi
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/Prim/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/ghci-%{version}
%{_libdir}/ghc-%{version}/ghci-%{version}/HSghci-%{version}.o
%{_libdir}/ghc-%{version}/ghci-%{version}/libHSghci-%{version}.a
%{_libdir}/ghc-%{version}/ghci-%{version}/libHSghci-%{version}-ghc*.so
%{_libdir}/ghc-%{version}/ghci-%{version}/*.hi
%{_libdir}/ghc-%{version}/ghci-%{version}/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghci-%{version}/GHCi
%{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/*.hi
%{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/TH
%{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/TH/*.hi
%{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/TH/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/haskeline-*
%{_libdir}/ghc-%{version}/haskeline-*/HShaskeline-%{gpv_haskeline}.o
%{_libdir}/ghc-%{version}/haskeline-*/libHShaskeline-%{gpv_haskeline}.a
%{_libdir}/ghc-%{version}/haskeline-*/libHShaskeline-%{gpv_haskeline}-ghc*.so
%dir %{_libdir}/ghc-%{version}/haskeline-*/System
%dir %{_libdir}/ghc-%{version}/haskeline-*/System/Console
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/*.hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/*.hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/*.hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/Posix
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/Posix/*.hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/Posix/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Command/
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Command/*.hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Command/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/hpc-*
%{_libdir}/ghc-%{version}/hpc-*/HShpc-%{gpv_hpc}.o
%{_libdir}/ghc-%{version}/hpc-*/libHShpc-%{gpv_hpc}.a
%{_libdir}/ghc-%{version}/hpc-*/libHShpc-%{gpv_hpc}-ghc*.so
%dir %{_libdir}/ghc-%{version}/hpc-*/Trace
%dir %{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc
%{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc/*.hi
%{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc/*.dyn_hi

%ifnarch x32
%dir %{_libdir}/ghc-%{version}/integer-gmp-*
%{_libdir}/ghc-%{version}/integer-gmp-*/HSinteger-gmp-%{gpv_integer_gmp}.o
%{_libdir}/ghc-%{version}/integer-gmp-*/libHSinteger-gmp-%{gpv_integer_gmp}.a
%{_libdir}/ghc-%{version}/integer-gmp-*/libHSinteger-gmp-%{gpv_integer_gmp}-ghc*.so
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/*.hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/*.hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP/*.hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/Logarithms
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/Logarithms/*.hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/Logarithms/*.dyn_hi
%{_libdir}/ghc-%{version}/integer-gmp-*/include
%else
%dir %{_libdir}/ghc-%{version}/integer-simple-*
%{_libdir}/ghc-%{version}/integer-simple-*/HSinteger-simple-%{gpv_integer_simple}.o
%{_libdir}/ghc-%{version}/integer-simple-*/libHSinteger-simple-%{gpv_integer_simple}-ghc*.so
%{_libdir}/ghc-%{version}/integer-simple-*/libHSinteger-simple-%{gpv_integer_simple}.a
%dir %{_libdir}/ghc-%{version}/integer-simple-*/GHC
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/*.hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/*.hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Logarithms
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Logarithms/*.hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Logarithms/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Simple
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Simple/*.hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Simple/*.dyn_hi
%endif

%dir %{_libdir}/ghc-%{version}/libiserv-%{version}
%{_libdir}/ghc-%{version}/libiserv-%{version}/HSlibiserv-%{version}.o
%{_libdir}/ghc-%{version}/libiserv-%{version}/libHSlibiserv-%{version}.a
%{_libdir}/ghc-%{version}/libiserv-%{version}/libHSlibiserv-%{version}-ghc*.so
%{_libdir}/ghc-%{version}/libiserv-%{version}/*.hi
%{_libdir}/ghc-%{version}/libiserv-%{version}/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/libiserv-%{version}/GHCi
%{_libdir}/ghc-%{version}/libiserv-%{version}/GHCi/*.hi
%{_libdir}/ghc-%{version}/libiserv-%{version}/GHCi/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/mtl-*
%{_libdir}/ghc-%{version}/mtl-*/HSmtl-%{gpv_mtl}.o
%{_libdir}/ghc-%{version}/mtl-*/libHSmtl-%{gpv_mtl}.a
%{_libdir}/ghc-%{version}/mtl-*/libHSmtl-%{gpv_mtl}-ghc*.so
%dir %{_libdir}/ghc-%{version}/mtl-*/Control
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Cont
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Cont/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Cont/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Error
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Error/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Error/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad/RWS
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/RWS/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/RWS/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Reader
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Reader/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Reader/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad/State
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/State/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/State/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Writer
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Writer/*.hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Writer/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/parsec-*
%{_libdir}/ghc-%{version}/parsec-*/HSparsec-%{gpv_parsec}.o
%{_libdir}/ghc-%{version}/parsec-*/libHSparsec-%{gpv_parsec}.a
%{_libdir}/ghc-%{version}/parsec-*/libHSparsec-%{gpv_parsec}-ghc*.so
%dir %{_libdir}/ghc-%{version}/parsec-*/Text
%{_libdir}/ghc-%{version}/parsec-*/Text/*.hi
%{_libdir}/ghc-%{version}/parsec-*/Text/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/parsec-*/Text/Parsec
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/*.hi
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/ByteString
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/ByteString/*.hi
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/ByteString/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/Text
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/Text/*.hi
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/Text/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators
%{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/*.hi
%{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/Parsec
%{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/Parsec/*.hi
%{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/Parsec/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/pretty-*
%{_libdir}/ghc-%{version}/pretty-*/HSpretty-%{gpv_pretty}.o
%{_libdir}/ghc-%{version}/pretty-*/libHSpretty-%{gpv_pretty}.a
%{_libdir}/ghc-%{version}/pretty-*/libHSpretty-%{gpv_pretty}-ghc*.so
%dir %{_libdir}/ghc-%{version}/pretty-*/Text
%{_libdir}/ghc-%{version}/pretty-*/Text/*.hi
%{_libdir}/ghc-%{version}/pretty-*/Text/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/*.hi
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/Annotated
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/Annotated/*.hi
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/Annotated/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/process-*
%{_libdir}/ghc-%{version}/process-*/HSprocess-%{gpv_process}.o
%{_libdir}/ghc-%{version}/process-*/libHSprocess-%{gpv_process}.a
%{_libdir}/ghc-%{version}/process-*/libHSprocess-%{gpv_process}-ghc*.so
%{_libdir}/ghc-%{version}/process-*/include
%dir %{_libdir}/ghc-%{version}/process-*/System
%{_libdir}/ghc-%{version}/process-*/System/*.hi
%{_libdir}/ghc-%{version}/process-*/System/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/process-*/System/Process
%{_libdir}/ghc-%{version}/process-*/System/Process/*.hi
%{_libdir}/ghc-%{version}/process-*/System/Process/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/rts
%if %{without system_libffi}
%{_libdir}/ghc-%{version}/rts/libCffi.a
%{_libdir}/ghc-%{version}/rts/libCffi_debug.a
%{_libdir}/ghc-%{version}/rts/libCffi_l.a
%{_libdir}/ghc-%{version}/rts/libCffi_thr.a
%{_libdir}/ghc-%{version}/rts/libCffi_thr_debug.a
%{_libdir}/ghc-%{version}/rts/libCffi_thr_l.a
%{_libdir}/ghc-%{version}/rts/libffi.so
%{_libdir}/ghc-%{version}/rts/libffi.so.7
%{_libdir}/ghc-%{version}/rts/libffi.so.7.1.0
%endif
%{_libdir}/ghc-%{version}/rts/libHSrts-ghc8.10.1.so
%{_libdir}/ghc-%{version}/rts/libHSrts.a
%{_libdir}/ghc-%{version}/rts/libHSrts_debug-ghc8.10.1.so
%{_libdir}/ghc-%{version}/rts/libHSrts_debug.a
%{_libdir}/ghc-%{version}/rts/libHSrts_l-ghc8.10.1.so
%{_libdir}/ghc-%{version}/rts/libHSrts_l.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr-ghc8.10.1.so
%{_libdir}/ghc-%{version}/rts/libHSrts_thr.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_debug-ghc8.10.1.so
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_debug.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_l-ghc8.10.1.so
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_l.a

%dir %{_libdir}/ghc-%{version}/stm-*
%{_libdir}/ghc-%{version}/stm-*/HSstm-%{gpv_stm}.o
%{_libdir}/ghc-%{version}/stm-*/libHSstm-%{gpv_stm}.a
%{_libdir}/ghc-%{version}/stm-*/libHSstm-%{gpv_stm}-ghc*.so
%dir %{_libdir}/ghc-%{version}/stm-*/Control
%dir %{_libdir}/ghc-%{version}/stm-*/Control/Concurrent
%{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/*.hi
%{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/STM
%{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/STM/*.hi
%{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/STM/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/stm-*/Control/Monad
%{_libdir}/ghc-%{version}/stm-*/Control/Monad/*.hi
%{_libdir}/ghc-%{version}/stm-*/Control/Monad/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/stm-*/Control/Sequential
%{_libdir}/ghc-%{version}/stm-*/Control/Sequential/*.hi
%{_libdir}/ghc-%{version}/stm-*/Control/Sequential/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/template-haskell-*
%{_libdir}/ghc-%{version}/template-haskell-*/HStemplate-haskell-%{gpv_template_haskell}.o
%{_libdir}/ghc-%{version}/template-haskell-*/libHStemplate-haskell-%{gpv_template_haskell}.a
%{_libdir}/ghc-%{version}/template-haskell-*/libHStemplate-haskell-%{gpv_template_haskell}-ghc*.so
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Lib
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Lib/*.hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Lib/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/terminfo-*
%{_libdir}/ghc-%{version}/terminfo-*/HSterminfo-%{gpv_terminfo}.o
%{_libdir}/ghc-%{version}/terminfo-*/libHSterminfo-%{gpv_terminfo}.a
%{_libdir}/ghc-%{version}/terminfo-*/libHSterminfo-%{gpv_terminfo}-ghc*.so
%dir %{_libdir}/ghc-%{version}/terminfo-*/System
%dir %{_libdir}/ghc-%{version}/terminfo-*/System/Console
%{_libdir}/ghc-%{version}/terminfo-*/System/Console/*.hi
%{_libdir}/ghc-%{version}/terminfo-*/System/Console/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/terminfo-*/System/Console/Terminfo
%{_libdir}/ghc-%{version}/terminfo-*/System/Console/Terminfo/*.hi
%{_libdir}/ghc-%{version}/terminfo-*/System/Console/Terminfo/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/text-*
%{_libdir}/ghc-%{version}/text-*/HStext-%{gpv_text}.o
%{_libdir}/ghc-%{version}/text-*/libHStext-%{gpv_text}.a
%{_libdir}/ghc-%{version}/text-*/libHStext-%{gpv_text}-ghc*.so
%dir %{_libdir}/ghc-%{version}/text-*/Data
%{_libdir}/ghc-%{version}/text-*/Data/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text
%{_libdir}/ghc-%{version}/text-*/Data/Text/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Encoding
%{_libdir}/ghc-%{version}/text-*/Data/Text/Encoding/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Encoding/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/Int
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/Int/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/Int/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/RealFloat
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/RealFloat/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/RealFloat/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/Fusion
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/Fusion/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/Fusion/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Fusion
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Fusion/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Fusion/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/Encoding
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/Encoding/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/Encoding/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Unsafe
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Unsafe/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Unsafe/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy
%{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/Builder
%{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/Builder/*.hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/Builder/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/time-*
%{_libdir}/ghc-%{version}/time-*/HStime-%{gpv_time}.o
%{_libdir}/ghc-%{version}/time-*/libHStime-%{gpv_time}.a
%{_libdir}/ghc-%{version}/time-*/libHStime-%{gpv_time}-ghc*.so
%{_libdir}/ghc-%{version}/time-*/include
%dir %{_libdir}/ghc-%{version}/time-*/Data
%{_libdir}/ghc-%{version}/time-*/Data/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time
%{_libdir}/ghc-%{version}/time-*/Data/Time/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar
%{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Clock
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/Internal
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/Internal/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/Internal/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Format
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Format
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Format/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Format/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Parse
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Parse/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Parse/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime/Internal
%{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime/Internal/*.hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime/Internal/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/transformers-*
%{_libdir}/ghc-%{version}/transformers-*/HStransformers-%{gpv_transformers}.o
%{_libdir}/ghc-%{version}/transformers-*/libHStransformers-%{gpv_transformers}.a
%{_libdir}/ghc-%{version}/transformers-*/libHStransformers-%{gpv_transformers}-ghc*.so
%dir %{_libdir}/ghc-%{version}/transformers-*/Control
%dir %{_libdir}/ghc-%{version}/transformers-*/Control/Applicative
%{_libdir}/ghc-%{version}/transformers-*/Control/Applicative/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Applicative/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/transformers-*/Control/Monad
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/RWS
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/RWS/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/RWS/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/State
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/State/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/State/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/Writer
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/Writer/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/Writer/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/transformers-*/Data
%dir %{_libdir}/ghc-%{version}/transformers-*/Data/Functor
%{_libdir}/ghc-%{version}/transformers-*/Data/Functor/*.hi
%{_libdir}/ghc-%{version}/transformers-*/Data/Functor/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/unix-*
%{_libdir}/ghc-%{version}/unix-*/HSunix-%{gpv_unix}.o
%{_libdir}/ghc-%{version}/unix-*/libHSunix-%{gpv_unix}.a
%{_libdir}/ghc-%{version}/unix-*/libHSunix-%{gpv_unix}-ghc*.so
%{_libdir}/ghc-%{version}/unix-*/include
%dir %{_libdir}/ghc-%{version}/unix-*/System
%{_libdir}/ghc-%{version}/unix-*/System/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix
%{_libdir}/ghc-%{version}/unix-*/System/Posix/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/ByteString
%{_libdir}/ghc-%{version}/unix-*/System/Posix/ByteString/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/ByteString/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Directory
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Directory/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Directory/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/Module
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/Module/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/DynamicLinker/Module/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Env
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Env/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Env/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Files
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Files/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Files/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/IO
%{_libdir}/ghc-%{version}/unix-*/System/Posix/IO/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/IO/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Process
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Process/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Process/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Signals/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Temp
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Temp/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Temp/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/unix-*/System/Posix/Terminal
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Terminal/*.hi
%{_libdir}/ghc-%{version}/unix-*/System/Posix/Terminal/*.dyn_hi

%dir %{_libdir}/ghc-%{version}/xhtml-*
%{_libdir}/ghc-%{version}/xhtml-*/HSxhtml-%{gpv_xhtml}.o
%{_libdir}/ghc-%{version}/xhtml-*/libHSxhtml-%{gpv_xhtml}.a
%{_libdir}/ghc-%{version}/xhtml-*/libHSxhtml-%{gpv_xhtml}-ghc*.so
%dir %{_libdir}/ghc-%{version}/xhtml-*/Text
%{_libdir}/ghc-%{version}/xhtml-*/Text/*.hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/*.hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Frameset
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Frameset/*.hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Frameset/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Strict
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Strict/*.hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Strict/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Transitional
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Transitional/*.hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Transitional/*.dyn_hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/Cabal-*/libHSCabal-%{gpv_Cabal}_p.a
%{_libdir}/ghc-%{version}/Cabal-*/HSCabal-%{gpv_Cabal}.p_o
%{_libdir}/ghc-%{version}/Cabal-*/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Backpack/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Internal/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Compat/Prelude/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/FieldGrammar/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Fields/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/PackageDescription/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Parsec/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/SPDX/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/GHC/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/InstallDirs/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/PreProcess/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Program/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Test/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Utils/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Benchmark/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/BuildInfo/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Executable/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/ForeignLib/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/GenericPackageDescription/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/InstalledPackageInfo/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/Library/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageDescription/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageId/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/PackageName/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SetupBuildInfo/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/SourceRepo/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/TestSuite/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionRange/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Utils/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Verbosity/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Language/Haskell/*.p_hi

%{_libdir}/ghc-%{version}/array-*/libHSarray-%{gpv_array}_p.a
%{_libdir}/ghc-%{version}/array-*/HSarray-%{gpv_array}.p_o
%{_libdir}/ghc-%{version}/array-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/IO/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/MArray/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/ST/*.p_hi
%{_libdir}/ghc-%{version}/array-*/Data/Array/Storable/*.p_hi

%{_libdir}/ghc-%{version}/base-*/libHSbase-%{gpv_base}_p.a
%{_libdir}/ghc-%{version}/base-*/HSbase-%{gpv_base}.p_o
%{_libdir}/ghc-%{version}/base-*/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Concurrent/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Exception/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/Monad/ST/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Control/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/Functor/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/List/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/Semigroup/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/STRef/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/Typeable/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Data/Type/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Debug/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/C/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/ForeignPtr/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Foreign/Marshal/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Conc/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Event/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Exception/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/ExecutionStack/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Float/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/GHCi/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/Lock/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/RTS/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Stack/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Numeric/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Console/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/CPUTime/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/CPUTime/Posix/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Environment/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Mem/*.p_hi
%{_libdir}/ghc-%{version}/base-*/System/Posix/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/ParserCombinators/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/Read/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Text/Show/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Type/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Type/Reflection/*.p_hi
%{_libdir}/ghc-%{version}/base-*/Unsafe/*.p_hi

%{_libdir}/ghc-%{version}/binar*y-*/libHSbinary-%{gpv_binary}_p.a
%{_libdir}/ghc-%{version}/binar*y-*/HSbinary-%{gpv_binary}.p_o
%{_libdir}/ghc-%{version}/binary-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/*.p_hi
%{_libdir}/ghc-%{version}/binary-*/Data/Binary/Get/*.p_hi

%{_libdir}/ghc-%{version}/bytestring-*/libHSbytestring-%{gpv_bytestring}_p.a
%{_libdir}/ghc-%{version}/bytestring-*/HSbytestring-%{gpv_bytestring}.p_o
%{_libdir}/ghc-%{version}/bytestring-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/Prim/Internal/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Builder/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Short/*.p_hi

%{_libdir}/ghc-%{version}/containers-*/libHScontainers-%{gpv_containers}_p.a
%{_libdir}/ghc-%{version}/containers-*/HScontainers-%{gpv_containers}.p_o
%{_libdir}/ghc-%{version}/containers-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Containers/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Internal/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Merge/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntMap/Strict/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/IntSet/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Internal/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Merge/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Map/Strict/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Sequence/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Sequence/Internal/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Data/Set/*.p_hi
%{_libdir}/ghc-%{version}/containers-*/Utils/Containers/Internal/*.p_hi

%{_libdir}/ghc-%{version}/deepseq-*/libHSdeepseq-%{gpv_deepseq}_p.a
%{_libdir}/ghc-%{version}/deepseq-*/HSdeepseq-%{gpv_deepseq}.p_o
%{_libdir}/ghc-%{version}/deepseq-*/Control/*.p_hi
%{_libdir}/ghc-%{version}/deepseq-*/Control/DeepSeq/*.p_hi

%{_libdir}/ghc-%{version}/directory-*/libHSdirectory-%{gpv_directory}_p.a
%{_libdir}/ghc-%{version}/directory-*/HSdirectory-%{gpv_directory}.p_o
%{_libdir}/ghc-%{version}/directory-*/System/*.p_hi
%{_libdir}/ghc-%{version}/directory-*/System/Directory/*.p_hi
%{_libdir}/ghc-%{version}/directory-*/System/Directory/Internal/*.p_hi

%{_libdir}/ghc-%{version}/exceptions-*/libHSexceptions-%{gpv_exceptions}_p.a
%{_libdir}/ghc-%{version}/exceptions-*/HSexceptions-%{gpv_exceptions}.p_o
%{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/exceptions-*/Control/Monad/Catch/*.p_hi

%{_libdir}/ghc-%{version}/filepath-*/libHSfilepath-%{gpv_filepath}_p.a
%{_libdir}/ghc-%{version}/filepath-*/HSfilepath-%{gpv_filepath}.p_o
%{_libdir}/ghc-%{version}/filepath-*/System/*.p_hi
%{_libdir}/ghc-%{version}/filepath-*/System/FilePath/*.p_hi

%{_libdir}/ghc-%{version}/ghc-%{version}/libHSghc-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-%{version}/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Dwarf/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/PmCheck/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Hoopl/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Llvm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/LlvmCodeGen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Graph/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/RegAlloc/Linear/X86_64/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SPARC/CodeGen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/StgLiftLams/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/SysTools/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/X86/*.p_hi

%{_libdir}/ghc-%{version}/ghc-boot-%{version}/libHSghc-boot-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/HSghc-boot-%{version}.p_o
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform/*.p_hi

%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/libHSghc-boot-th-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/HSghc-boot-th-%{version}.p_o
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/ForeignSrcLang/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/LanguageExtensions/*.p_hi

%{_libdir}/ghc-%{version}/ghc-compact-*/libHSghc-compact-%{gpv_compact}_p.a
%{_libdir}/ghc-%{version}/ghc-compact-*/HSghc-compact-%{gpv_compact}.p_o
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/Compact/*.p_hi

%{_libdir}/ghc-%{version}/ghc-heap-%{version}/libHSghc-heap-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/HSghc-heap-%{version}.p_o
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/*.p_hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/*.p_hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/InfoTable/*.p_hi

%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-%{gpv_prim}_p.a
%{_libdir}/ghc-%{version}/ghc-prim-*/HSghc-prim-%{gpv_prim}.p_o
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/Prim/*.p_hi

%{_libdir}/ghc-%{version}/ghci-%{version}/libHSghci-%{version}_p.a
%{_libdir}/ghc-%{version}/ghci-%{version}/HSghci-%{version}.p_o
%{_libdir}/ghc-%{version}/ghci-%{version}/*.p_hi
%{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/*.p_hi
%{_libdir}/ghc-%{version}/ghci-%{version}/GHCi/TH/*.p_hi

%{_libdir}/ghc-%{version}/haskeline-*/libHShaskeline-%{gpv_haskeline}_p.a
%{_libdir}/ghc-%{version}/haskeline-*/HShaskeline-%{gpv_haskeline}.p_o
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/*.p_hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/*.p_hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/*.p_hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Backend/Posix/*.p_hi
%{_libdir}/ghc-%{version}/haskeline-*/System/Console/Haskeline/Command/*.p_hi

%{_libdir}/ghc-%{version}/hpc-*/libHShpc-%{gpv_hpc}_p.a
%{_libdir}/ghc-%{version}/hpc-*/HShpc-%{gpv_hpc}.p_o
%{_libdir}/ghc-%{version}/hpc-*/Trace/Hpc/*.p_hi

%ifnarch x32
%{_libdir}/ghc-%{version}/integer-gmp-*/libHSinteger-gmp-%{gpv_integer_gmp}_p.a
%{_libdir}/ghc-%{version}/integer-gmp-*/HSinteger-gmp-%{gpv_integer_gmp}.p_o
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/*.p_hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP/*.p_hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/Logarithms/*.p_hi
%else
%{_libdir}/ghc-%{version}/integer-simple-*/HSinteger-simple-%{gpv_integer_simple}.p_o
%{_libdir}/ghc-%{version}/integer-simple-*/libHSinteger-simple-%{gpv_integer_simple}_p.a
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/*.p_hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Logarithms/*.p_hi
%{_libdir}/ghc-%{version}/integer-simple-*/GHC/Integer/Simple/*.p_hi
%endif

%{_libdir}/ghc-%{version}/libiserv-%{version}/libHSlibiserv-%{version}_p.a
%{_libdir}/ghc-%{version}/libiserv-%{version}/HSlibiserv-%{version}.p_o
%{_libdir}/ghc-%{version}/libiserv-%{version}/*.p_hi
%{_libdir}/ghc-%{version}/libiserv-%{version}/GHCi/*.p_hi

%{_libdir}/ghc-%{version}/mtl-*/libHSmtl-%{gpv_mtl}_p.a
%{_libdir}/ghc-%{version}/mtl-*/HSmtl-%{gpv_mtl}.p_o
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Cont/*.p_hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Error/*.p_hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/RWS/*.p_hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Reader/*.p_hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/State/*.p_hi
%{_libdir}/ghc-%{version}/mtl-*/Control/Monad/Writer/*.p_hi

%{_libdir}/ghc-%{version}/parsec-*/libHSparsec-%{gpv_parsec}_p.a
%{_libdir}/ghc-%{version}/parsec-*/HSparsec-%{gpv_parsec}.p_o
%{_libdir}/ghc-%{version}/parsec-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/*.p_hi
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/ByteString/*.p_hi
%{_libdir}/ghc-%{version}/parsec-*/Text/Parsec/Text/*.p_hi
%{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/*.p_hi
%{_libdir}/ghc-%{version}/parsec-*/Text/ParserCombinators/Parsec/*.p_hi

%{_libdir}/ghc-%{version}/pretty-*/libHSpretty-%{gpv_pretty}_p.a
%{_libdir}/ghc-%{version}/pretty-*/HSpretty-%{gpv_pretty}.p_o
%{_libdir}/ghc-%{version}/pretty-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/*.p_hi
%{_libdir}/ghc-%{version}/pretty-*/Text/PrettyPrint/Annotated/*.p_hi

%{_libdir}/ghc-%{version}/process-*/libHSprocess-%{gpv_process}_p.a
%{_libdir}/ghc-%{version}/process-*/HSprocess-%{gpv_process}.p_o
%{_libdir}/ghc-%{version}/process-*/System/*.p_hi
%{_libdir}/ghc-%{version}/process-*/System/Process/*.p_hi

%if %{without system_libffi}
%{_libdir}/ghc-%{version}/rts/libCffi_debug_p.a
%{_libdir}/ghc-%{version}/rts/libCffi_p.a
%{_libdir}/ghc-%{version}/rts/libCffi_thr_debug_p.a
%{_libdir}/ghc-%{version}/rts/libCffi_thr_p.a
%endif
%{_libdir}/ghc-%{version}/rts/libHSrts_debug_p.a
%{_libdir}/ghc-%{version}/rts/libHSrts_p.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_debug_p.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_p.a

%{_libdir}/ghc-%{version}/stm-*/libHSstm-%{gpv_stm}_p.a
%{_libdir}/ghc-%{version}/stm-*/HSstm-%{gpv_stm}.p_o
%{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/*.p_hi
%{_libdir}/ghc-%{version}/stm-*/Control/Concurrent/STM/*.p_hi
%{_libdir}/ghc-%{version}/stm-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/stm-*/Control/Sequential/*.p_hi

%{_libdir}/ghc-%{version}/template-haskell-*/libHStemplate-haskell-%{gpv_template_haskell}_p.a
%{_libdir}/ghc-%{version}/template-haskell-*/HStemplate-haskell-%{gpv_template_haskell}.p_o
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/*.p_hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/*.p_hi
%{_libdir}/ghc-%{version}/template-haskell-*/Language/Haskell/TH/Lib/*.p_hi

%{_libdir}/ghc-%{version}/terminfo-*/libHSterminfo-%{gpv_terminfo}_p.a
%{_libdir}/ghc-%{version}/terminfo-*/HSterminfo-%{gpv_terminfo}.p_o
%{_libdir}/ghc-%{version}/terminfo-*/System/Console/*.p_hi
%{_libdir}/ghc-%{version}/terminfo-*/System/Console/Terminfo/*.p_hi

%{_libdir}/ghc-%{version}/text-*/libHStext-%{gpv_text}_p.a
%{_libdir}/ghc-%{version}/text-*/HStext-%{gpv_text}.p_o
%{_libdir}/ghc-%{version}/text-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/Int/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Builder/RealFloat/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Encoding/Fusion/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Fusion/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Lazy/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Internal/Unsafe/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/text-*/Data/Text/Lazy/Builder/*.p_hi

%{_libdir}/ghc-%{version}/time-*/libHStime-%{gpv_time}_p.a
%{_libdir}/ghc-%{version}/time-*/HStime-%{gpv_time}.p_o
%{_libdir}/ghc-%{version}/time-*/Data/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Calendar/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Clock/Internal/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Format/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/Format/Parse/*.p_hi
%{_libdir}/ghc-%{version}/time-*/Data/Time/LocalTime/Internal/*.p_hi

%{_libdir}/ghc-%{version}/transformers-*/libHStransformers-%{gpv_transformers}_p.a
%{_libdir}/ghc-%{version}/transformers-*/HStransformers-%{gpv_transformers}.p_o
%{_libdir}/ghc-%{version}/transformers-*/Control/Applicative/*.p_hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/*.p_hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/*.p_hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/RWS/*.p_hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/State/*.p_hi
%{_libdir}/ghc-%{version}/transformers-*/Control/Monad/Trans/Writer/*.p_hi
%{_libdir}/ghc-%{version}/transformers-*/Data/Functor/*.p_hi

%{_libdir}/ghc-%{version}/unix-*/libHSunix-%{gpv_unix}_p.a
%{_libdir}/ghc-%{version}/unix-*/HSunix-%{gpv_unix}.p_o
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

%{_libdir}/ghc-%{version}/xhtml-*/libHSxhtml-%{gpv_xhtml}_p.a
%{_libdir}/ghc-%{version}/xhtml-*/HSxhtml-%{gpv_xhtml}.p_o
%{_libdir}/ghc-%{version}/xhtml-*/Text/*.p_hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/*.p_hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Frameset/*.p_hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Strict/*.p_hi
%{_libdir}/ghc-%{version}/xhtml-*/Text/XHtml/Transitional/*.p_hi

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs-root/html
%endif
