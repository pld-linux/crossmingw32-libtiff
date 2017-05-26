# TODO: jbigkit support
Summary:	Library for handling TIFF files - cross MinGW32 version
Summary(pl.UTF-8):	Biblioteka do manipulacji plikami w formacie TIFF - wersja skrośna MinGW32
%define		realname   libtiff
Name:		crossmingw32-%{realname}
Version:	4.0.8
Release:	1
License:	BSD-like
Group:		Development/Libraries
Source0:	http://download.osgeo.org/libtiff/tiff-%{version}.tar.gz
# Source0-md5:	2a7d1c1318416ddf36d5f6fa4600069b
Patch0:		%{realname}-glut.patch
URL:		http://www.remotesensing.org/libtiff/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-zlib
BuildRequires:	libtool >= 2:2.2
Requires:	crossmingw32-libjpeg
Requires:	crossmingw32-xz
Requires:	crossmingw32-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

%description
This package is a library of functions that manipulate TIFF images
(cross MinGW32 version).

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę pozwalającą manipulować plikami w
formacie TIFF (w wersji skrośnej MinGW32).

%package static
Summary:	Static libtiff library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libtiff (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libtiff library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libtiff (wersja skrośna MinGW32).

%package dll
Summary:	DLL libtiff library for Windows
Summary(pl.UTF-8):	Biblioteka DLL libtiff dla Windows
Group:		Applications/Emulators
Requires:	wine
Requires:	crossmingw32-libjpeg-dll
Requires:	crossmingw32-xz-dll
Requires:	crossmingw32-zlib-dll

%description dll
DLL libtiff library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL libtiff dla Windows.

%package cxx
Summary:	libtiff C++ streams library (cross MinGW32 version)
Summary(pl.UTF-8):	Biblioteka strumieni C++ dla libtiff (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description cxx
libtiff C++ streams library (cross MinGW32 version).

%description cxx -l pl.UTF-8
Biblioteka strumieni C++ dla libtiff (wersja skrośna MinGW32).

%package cxx-static
Summary:	Static libtiff C++ streams library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka strumieni C++ dla libtiff (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name}-cxx = %{version}-%{release}

%description cxx-static
Static libtiff C++ streams library (cross MinGW32 version).

%description cxx-static -l pl.UTF-8
Statyczna biblioteka strumieni C++ dla libtiff (wersja skrośna
MinGW32).

%package cxx-dll
Summary:	DLL libtiff C++ streams library for Windows
Summary(pl.UTF-8):	Biblioteka DLL strumieni C++ libtiff dla Windows
Group:		Applications/Emulators
Requires:	%{name}-dll = %{version}-%{release}

%description cxx-dll
DLL libtiff C++ streams library for Windows.

%description cxx-dll -l pl.UTF-8
Biblioteka DLL strumieni C++ libtiff dla Windows.

%prep
%setup -q -n tiff-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	lt_cv_deplibs_check_method=pass_all \
	--target=%{target} \
	--host=%{target} \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{doc,man}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.exe

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README TODO
%{_libdir}/libtiff.dll.a
%{_libdir}/libtiff.la
%{_includedir}/tiff*.h
%{_pkgconfigdir}/libtiff-4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtiff.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libtiff-*.dll

%files cxx
%defattr(644,root,root,755)
%{_libdir}/libtiffxx.dll.a
%{_libdir}/libtiffxx.la
%{_includedir}/tiffio.hxx

%files cxx-static
%defattr(644,root,root,755)
%{_libdir}/libtiffxx.a

%files cxx-dll
%defattr(644,root,root,755)
%{_dlldir}/libtiffxx-*.dll
