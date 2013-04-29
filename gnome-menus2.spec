%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname	gnome-menus
%define api	2.0
%define major	2
%define libname %mklibname gnome-menu %{major}
%define devname %mklibname -d gnome-menu %{api}

Summary:	GNOME menu library
Name:		gnome-menus2
Version:	2.30.5
Release:	5
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-menus/%{url_ver}/%{oname}-%{version}.tar.bz2
# (fc) 2.15.91-2mdv grab translation from menu-messages if not in upstream file
Patch0:		gnome-menus-2.27.92-l10n.patch
# (fc) 2.16.0-2mdv unclutter preferences/settings menu
Patch1:		gnome-menus-2.23.1-uncluttermenu.patch

BuildRequires:	python-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	intltool >= 0.40.0
Requires:	python-%{name}

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

Also contained here are the GNOME menu layout configuration files,
.directory files and assorted menu related utility programs.

%package -n python-%{name}
Group:		Development/Python
Summary:	Module to access XDG menu

%description -n python-%{name}
Python module to access XDG menu.

%package -n %{libname}
Group:		System/Libraries
Summary:	GNOME menu library

%description -n %{libname}
The package contains a shared library for %{name}.

%package -n %{devname}
Group:		Development/C
Summary:	GNOME menu library development files
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
The package contains the development files for %{name}.

%prep
%setup -qn %{oname}-%{version}
%apply_patches

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std
# gw these produce rpmlint errors:
rm -rf %{buildroot}%{_datadir}/locale/{io,be@latin,bn_IN,si,uz@cyrillic}

%find_lang %{oname}

mkdir -p %{buildroot}%{_sysconfdir}/xdg/gnome
mv %{buildroot}%{_sysconfdir}/xdg/menus %{buildroot}%{_sysconfdir}/xdg/gnome

chmod 755 %{buildroot}%{_libdir}/python*/site-packages/GMenuSimpleEditor/*.py

%files -f %{oname}.lang
%doc README NEWS HACKING AUTHORS ChangeLog
%{_datadir}/desktop-directories
%dir %{_sysconfdir}/xdg/gnome
%dir %{_sysconfdir}/xdg/gnome/menus
%config(noreplace) %{_sysconfdir}/xdg/gnome/menus/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/%{oname}

%files -n python-%{name}
%{_libdir}/python*/site-packages/*

%files -n %{libname}
%{_libdir}/libgnome-menu.so.%{major}*
%{_libdir}/girepository-1.0/GMenu-%{api}.typelib

%files -n %{devname}
%{_libdir}/lib*.so
%{_includedir}/gnome-menus/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/GMenu-%{api}.gir

