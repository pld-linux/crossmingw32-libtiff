#
# Conditional build:
%bcond_without opengl # do not build OpenGL viewer
#
Summary:	Library for handling TIFF files - cross Mingw32 version
Summary(de.UTF-8):Library zum Verwalten von TIFF-Dateien
Summary(fr.UTF-8):Bibliothèque de gestion des fichiers TIFF - wersja skrośna Mingw32
Summary(pl.UTF-8):Bibliteka do manipulacji plikami w formacie TIFF
Summary(tr.UTF-8):TIFF dosyalarını işleme kitaplığı
%define		_realname   libtiff
Name:		crossmingw32-%{_realname}
Version:	3.8.2
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	ftp://ftp.remotesensing.org/pub/libtiff/tiff-%{version}.tar.gz
# Source0-md5:	fbb6f446ea4ed18955e2714934e5b698
Patch0:		%{_realname}-sec.patch
URL:		http://www.remotesensing.org/libtiff/
%{?with_opengl:BuildRequires:  OpenGL-glut-devel}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-zlib
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
This package is a library of functions that manipulate TIFF images.

%description -l de.UTF-8
Eine Library von Funktionen zur Manipulation von TIFFs.

%description -l fr.UTF-8
Bibliothèque de fonctions pour manipuler des images TIFF.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę pozwalającą manipulować plikami w
formacie TIFF.

%description -l tr.UTF-8
Bu paket TIFF resimlerini işleyen fonksiyonlardan oluşan bir
kitaplıktır.

%package cxx
Summary:	libtiff C++ streams library
Summary(pl.UTF-8):Biblioteka strumieni C++ dla libtiff
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description cxx
libtiff C++ streams library.

%description cxx -l pl.UTF-8
Biblioteka strumieni C++ dla libtiff.

%prep
%setup -q -n tiff-%{version}

%patch0 -p1

rm -f m4/{libtool,lt*}.m4

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	AR="%{target}-ar" \
	RANLIB="%{target}-ranlib" \
	--target=%{target} \
	--host=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_bindir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf html{,/*}/Makefile* $RPM_BUILD_ROOT%{_docdir}/tiff-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README TODO
%{_libdir}/libtiff.la
%{_libdir}/libtiff.a
%{_includedir}/tiff*.h

%files cxx
%defattr(644,root,root,755)
%{_libdir}/libtiffxx.la
%{_libdir}/libtiffxx.a
%{_includedir}/tiffio.hxx
