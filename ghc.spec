Summary:	Glasgow Haskell Compilation system
Summary(pl):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	6.2.2
Release:	0.1
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src.tar.bz2
# Source0-md5:	42088bff4de30e7c3a277cfa55d5589e
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-debian.patch
Patch3:		%{name}-ar.patch
URL:		http://haskell.org/ghc/
BuildRequires:	autoconf
BuildRequires:	ghc >= 4.0.8
BuildRequires:	gmp-devel
BuildRequires:	happy >= 1.10
BuildRequires:	alex >= 2.0
BuildRequires:	jadetex
BuildRequires:	ncurses-devel
BuildRequires:	openjade
BuildRequires:	readline-devel
BuildRequires:	sgml-common
BuildRequires:	tetex-latex-bibtex
BuildRequires:	docbook-style-dsssl
Provides:	haskell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Glorious Glasgow Haskell Compilation System (GHC) is a robust,
fully-featured, optimising compiler for the functional programming
language Haskell 98. GHC compiles Haskell to either native code or C.
It implements numerous experimental language extensions to Haskell,
including concurrency, a foreign language interface, several
type-system extensions, exceptions, and so on. GHC comes with a
generational garbage collector, a space and time profiler, and a
comprehensive set of libraries. This package includes HTML and PS
versions of the SGML-based documentation for GHC. They are also
available online at http://www.haskell.org/ghc/.

Haskell 98 is "the" standard lazy functional programming language.
More info plus the language definition is at http://www.haskell.org/.

%description -l pl
S³awny Glasgow Haskell Compilation System (GHC) to mocny, w pe³ni
funkcjonalny, optymalizuj±cy kompilator funkcyjnego jêzyka
programowania Haskell 98. GHC kompiluje Haskella do kodu natywnego lub
do C. Ma zaimplementowanych wiele eksperymentalnych rozszerzeñ jêzyka,
w tym wspó³bie¿no¶æ, interfejs do innych jêzyków, rozszerzenia systemu
typów, wyj±tki itd. GHS zawiera garbage collector, profiler, obszerny
zestaw bibliotek. Ten pakiet zawiera wersje HTML i PostScriptow±
dokumentacji bazowanej na SGML-u. S± one dostêpne tak¿e online pod
http://www.haskell.org/ghc/ .

Haskell 98 to standardowy leniwy funkcyjny jêzyk programowania. Wiêcej
informacji oraz definicja jêzyka pod http://www.haskell.org/ .

%package prof
Summary:	Profiling libraries for GHC
Summary(pl):	Biblioteki profiluj±ce dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description prof
Profiling libraries for Glorious Glasgow Haskell Compilation System
(GHC). They should be installed when GHC's profiling subsystem is
needed.

%description prof -l pl
Biblioteki profiluj±ce dla GHC. Powinny byæ zainstalowane kiedy
potrzebujemy systemu profiluj±cego z GHC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1

# generate our own `build.mk'
#
# * this is a kludge
#
cat >mk/build.mk <<END
GhcLibWays = p
SRC_HAPPY_OPTS += -agc # useful from Happy 1.7 onwards
SRC_HAPPY_OPTS += -c
END
%ifarch amd64
cat >>mk/build.mk <<END 
GhcUnregisterised=YES
SplitObjs=NO
END
%endif

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure \
	--with-gcc=%{__cc}

%{__make} boot
%{__make} -C glafp-utils sgmlverb
%{__make} all
%{__make} -C docs ps html
%{__make} -C ghc/docs ps html
%{__make} -C ghc/docs/users_guide ps html
%{__make} -C hslibs/doc ps html
%{__make} -C hslibs/graphics/doc ps
(cd ghc/docs/rts; latex rts.tex; dvips -o rts.dvi)

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-dirs \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ghc/{ANNOUNCE,README}
%doc ghc/docs/rts/*.ps
%doc ghc/docs/users_guide/{*.ps,users_guide}
%doc hslibs/doc/{*.ps,hslibs}
%doc hslibs/graphics/doc/*.ps
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/ghc-%{version}
%dir %{_datadir}/ghc-%{version}/icons
%{_datadir}/ghc-%{version}/icons/*
%dir %{_libdir}/ghc-%{version}
%dir %{_libdir}/ghc-%{version}/hslibs-imports
%dir %{_libdir}/ghc-%{version}/hslibs-imports/*
%dir %{_libdir}/ghc-%{version}/imports
%dir %{_libdir}/ghc-%{version}/imports/*
%dir %{_libdir}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/include/*
%{_libdir}/ghc-%{version}/imports/*/*.hi
%{_libdir}/ghc-%{version}/imports/*/*/*.hi
%{_libdir}/ghc-%{version}/imports/*/*/*/*.hi
%{_libdir}/ghc-%{version}/hslibs-imports/*/*.hi
%attr(755,root,root) %{_libdir}/ghc-%{version}/cgprof
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-%{version}
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-asm
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-pkg.bin
%attr(755,root,root) %{_libdir}/ghc-%{version}/ghc-split
%attr(755,root,root) %{_libdir}/ghc-%{version}/hsc2hs-bin
%attr(755,root,root) %{_libdir}/ghc-%{version}/unlit
%{_libdir}/ghc-%{version}/*.prl
%{_libdir}/ghc-%{version}/libHS*[^p].a
%{_libdir}/ghc-%{version}/HS*.o
%{_libdir}/ghc-%{version}/package.conf
%{_libdir}/ghc-%{version}/*.h
%{_libdir}/ghc-%{version}/ghc*-usage.txt

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/imports/*/*.p_hi
%{_libdir}/ghc-%{version}/imports/*/*/*.p_hi
%{_libdir}/ghc-%{version}/imports/*/*/*/*.p_hi
%{_libdir}/ghc-%{version}/hslibs-imports/*/*.p_hi
%{_libdir}/ghc-%{version}/libHS*_p.a
