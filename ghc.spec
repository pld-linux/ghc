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
%define		gpv_Cabal		3.6.3.0
%define		gpv_array		0.5.4.0
%define		gpv_base		4.16.4.0
%define		gpv_bin_package_db	0.0.0.0
%define		gpv_binary		0.8.9.0
%define		gpv_bytestring		0.11.4.0
%define		gpv_containers		0.6.5.1
%define		gpv_deepseq		1.4.6.1
%define		gpv_directory		1.3.6.2
%define		gpv_exceptions		0.10.4
%define		gpv_filepath		1.4.2.2
%define		gpv_ghc_bignum		1.2
%define		gpv_ghc_compact		0.1.0.0
%define		gpv_ghc_prim		0.8.0
%define		gpv_haskeline		0.8.2
%define		gpv_hpc			0.6.1.0
%define		gpv_integer_gmp		1.1
%define		gpv_mtl			2.2.2
%define		gpv_parsec		3.1.15.0
%define		gpv_pretty		1.1.3.6
%define		gpv_process		1.6.16.0
%define		gpv_stm			2.5.0.2
%define		gpv_template_haskell	2.18.0.0
%define		gpv_terminfo		0.4.1.5
%define		gpv_text		1.2.5.0
%define		gpv_time		1.11.1.1
%define		gpv_transformers	0.5.6.2
%define		gpv_unix		2.7.2.2
%define		gpv_xhtml		3000.2.2.1

%define		bootversion		8.10.7

# native code generator (-fasm) support
%ifarch %{ix86} %{x8664} aarch64 ppc ppc64 ppc64le sparc
%define		with_ncg	1
%endif

# archs with upstream support for which bootstrap binaries are provided
%define		official_archs		%{ix86} %{x8664} aarch64

Summary:	Glasgow Haskell Compilation system
Summary(pl.UTF-8):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	9.2.7
Release:	1
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	https://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.xz
# Source0-md5:	56b92670fa17c0c8a034e85782937d59
%if %{with bootstrap}
Source3:	https://downloads.haskell.org/~ghc/%{bootversion}/%{name}-%{bootversion}-i386-deb9-linux.tar.xz
# Source3-md5:	ed69fd3ed46efd9dcd954e54166712b5
Source4:	https://downloads.haskell.org/~ghc/%{bootversion}/%{name}-%{bootversion}-x86_64-deb9-linux.tar.xz
# Source4-md5:	e4905d2c51a144479c264d67108297fe
Source5:	http://ftp.ports.debian.org/debian-ports/pool-x32/main/g/ghc/ghc_8.8.3-1~exp2_x32.deb
# Source5-md5:	b912b87c8d9450d140ae773083edecb0
Source6:	https://downloads.haskell.org/~ghc/%{bootversion}/%{name}-%{bootversion}-aarch64-deb10-linux.tar.lz
# Source6-md5:	9ffb05a373de6b98daaab2176f208f31
%endif
Patch0:		%{name}-pld.patch
Patch1:		%{name}-pkgdir.patch
Patch3:		build.patch
Patch4:		buildpath-abi-stability.patch
Patch5:		x32-use-native-x86_64-insn.patch
Patch6:		llvm15.patch
URL:		http://haskell.org/ghc/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	bash
BuildRequires:	binutils >= 4:2.30
BuildRequires:	clang
BuildRequires:	freealut-devel
BuildRequires:	gmp-devel
%{?with_system_libffi:BuildRequires:	libffi-devel}
BuildRequires:	lzip
BuildRequires:	ncurses-devel >= 6.3.20211120-2
BuildRequires:	numactl-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.005
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with bootstrap}
%ifarch %{official_archs}
BuildRequires:	compat-ncurses5
%endif
%if %{without unregisterised} && %{without ncg}
BuildRequires:	llvm >= 9
%endif
BuildRequires:	numactl-libs
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
Requires:	gcc
Requires:	glibc-headers
Requires:	gmp-devel
%{?with_system_libffi:BuildRequires:	libffi-devel}
%if %{without unregisterised} && %{without ncg}
# targets without ncg use llvm backend by default which requires llc/opt
Requires:	llvm >= 9
%endif
Requires:	numactl-devel
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
Provides:	ghc-ghc-bignum = %{gpv_ghc_bignum}
Provides:	ghc-ghc-compact = %{gpv_ghc_compact}
Provides:	ghc-ghc-prim = %{gpv_ghc_prim}
Provides:	ghc-haskeline = %{gpv_haskeline}
Provides:	ghc-hpc = %{gpv_hpc}
Provides:	ghc-integer-gmp = %{gpv_integer_gmp}
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
%if %{without unregisterised} && %{with ncg}
Suggests:	llvm >= 9
%endif
Provides:	haddock
Obsoletes:	haddock
ExclusiveArch:	%{official_archs} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# There is nothing that may or should be compressed
%define		_noautocompressdoc	*

%define		_debugsource_packages	0

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
Provides:	ghc-ghc-bignum-prof = %{gpv_ghc_bignum}
Provides:	ghc-ghc-compact-prof = %{gpv_ghc_compact}
Provides:	ghc-ghc-prim-prof = %{gpv_ghc_prim}
Provides:	ghc-haskeline-prof = %{gpv_haskeline}
Provides:	ghc-hpc-prof = %{gpv_hpc}
Provides:	ghc-integer-gmp-prof = %{gpv_integer_gmp}
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
BuildArch:	noarch

%description doc
Documentation for GHC.

%description doc -l pl.UTF-8
Dokumentacja do GHC.

%prep
%setup -q
%if %{with bootstrap}

# official binaries
%ifarch %{official_archs}
%ifarch %{ix86}
%{__tar} -xf %{SOURCE3}
%endif
%ifarch %{x8664}
%{__tar} -xf %{SOURCE4}
%endif
%ifarch aarch64
%{__tar} -xf %{SOURCE6}
%endif
%{__mv} %{name}-%{bootversion} binsrc
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

bin/ghc-pkg recache --global
cd ..
%endif
%endif

%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

%build
LC_ALL=C.UTF-8; export LC_ALL
%{__bash} ./utils/llvm-targets/gen-data-layout.sh > llvm-targets

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
HADDOCK_DOCS        = YES
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

top=$(pwd)
%if %{with bootstrap}

# don't depend on ncurses and do minimal things for bootstrap
echo "libraries/haskeline_CONFIGURE_OPTS += --flag=-terminfo" >> mk/build.mk
echo "utils/ghc-pkg_HC_OPTS += -DBOOTSTRAPPING" >> mk/build.mk

%ifarch %{official_archs}
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
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} docs-root

# fix paths to docs in package list
sed -i -e 's|%{_datadir}/doc/%{name}|%{_docdir}/%{name}-%{version}|g' $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/package.conf.d/*.conf
%else
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
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
%attr(755,root,root) %{_bindir}/haddock
%attr(755,root,root) %{_bindir}/haddock-ghc-%{version}
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
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/haddock
%attr(755,root,root) %{_libdir}/ghc-%{version}/bin/hp2ps
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
%{_libdir}/ghc-%{version}/html
%dir %{_libdir}/ghc-%{version}/latex
%{_libdir}/ghc-%{version}/latex/haddock.sty
%{?with_doc:%{_mandir}/man1/ghc.1*}
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
%{_libdir}/ghc-%{version}/package.conf.d/ghc-bignum-%{gpv_ghc_bignum}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-boot-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-boot-th-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-compact-%{gpv_ghc_compact}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-heap-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghc-prim-%{gpv_ghc_prim}.conf
%{_libdir}/ghc-%{version}/package.conf.d/ghci-%{version}.conf
%{_libdir}/ghc-%{version}/package.conf.d/haskeline-%{gpv_haskeline}.conf
%{_libdir}/ghc-%{version}/package.conf.d/hpc-%{gpv_hpc}.conf
%{_libdir}/ghc-%{version}/package.conf.d/integer-gmp-%{gpv_integer_gmp}.conf
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
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/Macros
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/Macros/*.dyn_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/Macros/*.hi
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/PathsModule
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/PathsModule/*.dyn_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/PathsModule/*.hi
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
%dir %{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionInterval
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionInterval/*.dyn_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionInterval/*.hi
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
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Event/Internal
%{_libdir}/ghc-%{version}/base-*/GHC/Event/Internal/*.dyn_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Event/Internal/*.hi
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
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Integer
%{_libdir}/ghc-%{version}/base-*/GHC/Integer/*.dyn_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Integer/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/RTS
%{_libdir}/ghc-%{version}/base-*/GHC/RTS/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/RTS/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/Stack
%{_libdir}/ghc-%{version}/base-*/GHC/Stack/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/Stack/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr
%{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr/*.hi
%{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/TypeLits
%{_libdir}/ghc-%{version}/base-*/GHC/TypeLits/*.dyn_hi
%{_libdir}/ghc-%{version}/base-*/GHC/TypeLits/*.hi
%dir %{_libdir}/ghc-%{version}/base-*/GHC/TypeNats
%{_libdir}/ghc-%{version}/base-*/GHC/TypeNats/*.dyn_hi
%{_libdir}/ghc-%{version}/base-*/GHC/TypeNats/*.hi
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
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/RealFloat
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/RealFloat/*.dyn_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/RealFloat/*.hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Internal
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Internal/*.dyn_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Internal/*.hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Internal
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Internal/*.dyn_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Internal/*.hi
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
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Names
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Names/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Names/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Types
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Types/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Types/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/ByteCode
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/ByteCode/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/ByteCode/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Dataflow
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Dataflow/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Dataflow/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Info
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Info/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Info/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Parser
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Parser/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Parser/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Ppr
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Ppr/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Ppr/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Switch
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Switch/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Switch/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/AArch64
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/AArch64/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/AArch64/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/CFG
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/CFG/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/CFG/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Dwarf
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Dwarf/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Dwarf/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/PPC
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/PPC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/PPC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Graph
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Graph/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Graph/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Linear
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Linear/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Linear/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/CodeGen
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/CodeGen/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/CodeGen/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/X86
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/X86/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/X86/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToLlvm
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToLlvm/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToLlvm/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Foreign
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Foreign/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Foreign/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Match
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Match/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Match/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Llvm
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Llvm/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Llvm/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/SysTools
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/SysTools/*.hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/SysTools/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Coercion
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Coercion/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Coercion/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Map
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Map/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Map/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/Simplify
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/Simplify/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/Simplify/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/WorkWrap
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/WorkWrap/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/WorkWrap/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCo
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCo/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCo/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCon
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCon/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCon/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Unfold
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Unfold/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Unfold/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CoreToStg
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CoreToStg/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CoreToStg/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/FastString
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/FastString/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/FastString/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/Graph
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/Graph/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/Graph/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/List
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/List/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/List/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Backpack
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Backpack/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Backpack/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Env
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Env/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Env/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Pipeline
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Pipeline/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Pipeline/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/Solver
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/Solver/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/Solver/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Ext
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Ext/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Ext/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Recomp
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Recomp/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Recomp/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Tidy
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Tidy/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Tidy/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Linker
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Linker/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Linker/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/Errors
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/Errors/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/Errors/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/PostProcess
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/PostProcess/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/PostProcess/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/Reg
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/Reg/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/Reg/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Rename
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Rename/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Rename/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Eval
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Eval/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Eval/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Heap
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Heap/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Heap/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Interpreter
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Interpreter/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Interpreter/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Settings
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Settings/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Settings/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/Lift
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/Lift/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/Lift/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Deriv
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Deriv/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Deriv/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/Hole
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/Hole/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/Hole/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Gen
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Gen/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Gen/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Instance
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Instance/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Instance/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Solver
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Solver/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Solver/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/TyCl
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/TyCl/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/TyCl/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Types
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Types/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Types/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Utils
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Utils/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Utils/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/CostCentre
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/CostCentre/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/CostCentre/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Fixity
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Fixity/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Fixity/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Id
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Id/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Id/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Name
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Name/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Name/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/TyThing
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/TyThing/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/TyThing/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Unique
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Unique/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Unique/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Var
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Var/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Var/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Finder
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Finder/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Finder/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Home
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Home/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Home/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Module
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Module/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Module/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Binary
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Binary/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Binary/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/IO
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/IO/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/IO/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Monad
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Monad/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Monad/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Panic
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Panic/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Panic/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Ppr
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Ppr/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Ppr/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell
%{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/Syntax
%{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/Syntax/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/Syntax/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/HSghc-boot-%{version}.o
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/libHSghc-boot-%{version}.a
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/libHSghc-boot-%{version}-ghc*.so
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Data
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Data/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Data/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform/*.hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform/*.dyn_hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Settings
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Settings/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Settings/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Unit
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Unit/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Unit/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Utils
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Utils/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Utils/*.hi

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

%dir %{_libdir}/ghc-%{version}/ghc-bignum-*
%{_libdir}/ghc-%{version}/ghc-bignum-*/HSghc-bignum-%{gpv_ghc_bignum}.o
%{_libdir}/ghc-%{version}/ghc-bignum-*/libHSghc-bignum-%{gpv_ghc_bignum}.a
%{_libdir}/ghc-%{version}/ghc-bignum-*/libHSghc-bignum-%{gpv_ghc_bignum}-ghc*.so
%{_libdir}/ghc-%{version}/ghc-bignum-*/include
%dir %{_libdir}/ghc-%{version}/ghc-bignum-*/GHC
%dir %{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num
%{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/*.hi
%dir %{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/Backend
%{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/Backend/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/Backend/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-compact-*
%{_libdir}/ghc-%{version}/ghc-compact-*/HSghc-compact-%{gpv_ghc_compact}.o
%{_libdir}/ghc-%{version}/ghc-compact-*/libHSghc-compact-%{gpv_ghc_compact}.a
%{_libdir}/ghc-%{version}/ghc-compact-*/libHSghc-compact-%{gpv_ghc_compact}-ghc*.so
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
%dir %{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/ProfInfo
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/ProfInfo/*.dyn_hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/ProfInfo/*.hi

%dir %{_libdir}/ghc-%{version}/ghc-prim-*
%{_libdir}/ghc-%{version}/ghc-prim-*/HSghc-prim-%{gpv_ghc_prim}.o
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-%{gpv_ghc_prim}.a
%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-%{gpv_ghc_prim}-ghc*.so
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

%dir %{_libdir}/ghc-%{version}/integer-gmp-*
%{_libdir}/ghc-%{version}/integer-gmp-*/HSinteger-gmp-%{gpv_integer_gmp}.o
%{_libdir}/ghc-%{version}/integer-gmp-*/libHSinteger-gmp-%{gpv_integer_gmp}.a
%{_libdir}/ghc-%{version}/integer-gmp-*/libHSinteger-gmp-%{gpv_integer_gmp}-ghc*.so
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer
%dir %{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP/*.hi
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP/*.dyn_hi

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
%{_libdir}/ghc-%{version}/rts/libHSrts-ghc%{version}.so
%{_libdir}/ghc-%{version}/rts/libHSrts.a
%{_libdir}/ghc-%{version}/rts/libHSrts_debug-ghc%{version}.so
%{_libdir}/ghc-%{version}/rts/libHSrts_debug.a
%{_libdir}/ghc-%{version}/rts/libHSrts_l-ghc%{version}.so
%{_libdir}/ghc-%{version}/rts/libHSrts_l.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr-ghc%{version}.so
%{_libdir}/ghc-%{version}/rts/libHSrts_thr.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_debug-ghc%{version}.so
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_debug.a
%{_libdir}/ghc-%{version}/rts/libHSrts_thr_l-ghc%{version}.so
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
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/Macros/*.p_hi
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Simple/Build/PathsModule/*.p_hi
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
%{_libdir}/ghc-%{version}/Cabal-*/Distribution/Types/VersionInterval/*.p_hi
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
%{_libdir}/ghc-%{version}/base-*/GHC/Event/Internal/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Exception/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/ExecutionStack/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Fingerprint/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Float/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/GHCi/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Encoding/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/IO/Handle/Lock/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Integer/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/RTS/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/Stack/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/StaticPtr/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/TypeLits/*.p_hi
%{_libdir}/ghc-%{version}/base-*/GHC/TypeNats/*.p_hi
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
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Builder/RealFloat/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Internal/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/*.p_hi
%{_libdir}/ghc-%{version}/bytestring-*/Data/ByteString/Lazy/Internal/*.p_hi
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
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Names/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Builtin/Types/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/ByteCode/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Dataflow/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Info/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Parser/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Ppr/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Cmm/Switch/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/AArch64/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/CFG/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Dwarf/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/PPC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Graph/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/Reg/Linear/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/SPARC/CodeGen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToAsm/X86/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CmmToLlvm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Coercion/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Map/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/Simplify/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Opt/WorkWrap/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCo/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/TyCon/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Core/Unfold/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/CoreToStg/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/FastString/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/Graph/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Data/List/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Backpack/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Env/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Driver/Pipeline/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Hs/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Foreign/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Match/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/HsToCore/Pmc/Solver/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Ext/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Recomp/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Iface/Tidy/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Linker/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Llvm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/Errors/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Parser/PostProcess/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Platform/Reg/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Rename/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Eval/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Heap/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Runtime/Interpreter/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Settings/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Stg/Lift/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/StgToCmm/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/SysTools/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Deriv/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Errors/Hole/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Gen/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Instance/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Solver/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/TyCl/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Types/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Tc/Utils/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/CostCentre/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Fixity/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Id/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Name/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/TyThing/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Unique/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Types/Var/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Finder/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Home/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Unit/Module/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Binary/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/IO/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Monad/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Panic/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/GHC/Utils/Ppr/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/*.p_hi
%{_libdir}/ghc-%{version}/ghc-%{version}/Language/Haskell/Syntax/*.p_hi

%{_libdir}/ghc-%{version}/ghc-boot-%{version}/libHSghc-boot-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/HSghc-boot-%{version}.p_o
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Data/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Platform/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Settings/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Unit/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-%{version}/GHC/Utils/*.p_hi

%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/libHSghc-boot-th-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/HSghc-boot-th-%{version}.p_o
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/ForeignSrcLang/*.p_hi
%{_libdir}/ghc-%{version}/ghc-boot-th-%{version}/GHC/LanguageExtensions/*.p_hi

%{_libdir}/ghc-%{version}/ghc-bignum-*/libHSghc-bignum-%{gpv_ghc_bignum}_p.a
%{_libdir}/ghc-%{version}/ghc-bignum-*/HSghc-bignum-%{gpv_ghc_bignum}.p_o
%{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/*.p_hi
%{_libdir}/ghc-%{version}/ghc-bignum-*/GHC/Num/Backend/*.p_hi

%{_libdir}/ghc-%{version}/ghc-compact-*/libHSghc-compact-%{gpv_ghc_compact}_p.a
%{_libdir}/ghc-%{version}/ghc-compact-*/HSghc-compact-%{gpv_ghc_compact}.p_o
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-compact-*/GHC/Compact/*.p_hi

%{_libdir}/ghc-%{version}/ghc-heap-%{version}/libHSghc-heap-%{version}_p.a
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/HSghc-heap-%{version}.p_o
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/*.p_hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/*.p_hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/InfoTable/*.p_hi
%{_libdir}/ghc-%{version}/ghc-heap-%{version}/GHC/Exts/Heap/ProfInfo/*.p_hi

%{_libdir}/ghc-%{version}/ghc-prim-*/libHSghc-prim-%{gpv_ghc_prim}_p.a
%{_libdir}/ghc-%{version}/ghc-prim-*/HSghc-prim-%{gpv_ghc_prim}.p_o
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/*.p_hi
%{_libdir}/ghc-%{version}/ghc-prim-*/GHC/Prim/*.p_hi

%{_libdir}/ghc-%{version}/ghci-%{version}/libHSghci-%{version}_p.a
%{_libdir}/ghc-%{version}/ghci-%{version}/HSghci-%{version}.p_o
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

%{_libdir}/ghc-%{version}/integer-gmp-*/libHSinteger-gmp-%{gpv_integer_gmp}_p.a
%{_libdir}/ghc-%{version}/integer-gmp-*/HSinteger-gmp-%{gpv_integer_gmp}.p_o
%{_libdir}/ghc-%{version}/integer-gmp-*/GHC/Integer/GMP/*.p_hi

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
