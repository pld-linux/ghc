Summary:	Glasgow Haskell Compilation system
Summary(pl):	System kompilacji Glasgow Haskell
Name:		ghc
Version:	5.02.1
Release:	1
License:	BSD-like w/o adv. clause
Group:		Development/Languages
Source0:	http://haskell.org/ghc/dist/%{version}/%{name}-%{version}-src-1.tar.bz2
Patch0:		%{name}-sgml-CATALOG.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://haskell.org/ghc/
Provides:	haskell
BuildRequires:	gmp-devel
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	happy >= 1.9
BuildRequires:	ghc >= 4.0.8
BuildRequires:	sgml-common
BuildRequires:	openjade
BuildRequires:	jadetex
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
w tym konkurencjê, interfejs do innych jêzyków, rozszerzenia systemu
typów, wyj±tki itd. GHS zawiera garbage collector, profiler, obszerny
zestaw bibliotek. Ten pakiet zawiera wersje HTML i PS dokumentacji
bazowanej na SGML. S± one dostêpne tak¿e online pod
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
#%patch0 -p1
%patch1 -p1

# generate our own `build.mk'
#
# * this is a kludge
#
cat >mk/build.mk <<END
GhcLibWays = p
SRC_HAPPY_OPTS += -agc # useful from Happy 1.7 onwards
SRC_HAPPY_OPTS += -c
END

%build
%{__autoconf}
(cd ghc; autoconf)
%configure \
	--with-gcc=%{__cc}

%{__make} boot
%{__make} -C glafp-utils sgmlverb
%{__make} all
%{__make} -C docs ps html
%{__make} -C ghc/docs ps html
%{__make} -C ghc/docs/users_guide ps html
%{__make} -C hslibs/doc ps html
#%{__make} -C hslibs/graphics/doc ps
(cd ghc/docs/rts; latex rts.tex; dvips -o rts.dvi)

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-dirs \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf ghc/ANNOUNCE ghc/README hslibs/doc/*.ps \
	ghc/docs/set/*.ps ghc/docs/rts/rts.ps ghc/docs/users_guide/*.ps \
	hslibs/graphics/doc/*.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ghc/{ANNOUNCE,README}.gz
%doc ghc/docs/set/{*.ps.gz,set} ghc/docs/rts/*.ps.gz
%doc ghc/docs/users_guide/{*.ps.gz,users_guide}
%doc hslibs/doc/{*.ps.gz,hslibs}
#%doc hslibs/graphics/doc/*.ps.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/ghc-%{version}
%dir %{_libdir}/ghc-%{version}/icons
%dir %{_libdir}/ghc-%{version}/imports
%dir %{_libdir}/ghc-%{version}/imports/*
%dir %{_libdir}/ghc-%{version}/include
%{_libdir}/ghc-%{version}/icons/*
%{_libdir}/ghc-%{version}/include/*
%{_libdir}/ghc-%{version}/imports/*/*.hi
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

%files prof
%defattr(644,root,root,755)
%{_libdir}/ghc-%{version}/imports/*/*.p_hi
%{_libdir}/ghc-%{version}/libHS*_p.a
