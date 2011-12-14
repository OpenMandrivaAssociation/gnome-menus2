%define major 2
%define libname %mklibname gnome-menu %major
%define libnamedev %mklibname -d gnome-menu
%define api 2.0

Summary: GNOME menu library
Name: gnome-menus
Version: 2.30.5
Release: %mkrel 2
Source0: http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
# (fc) 2.15.91-2mdv grab translation from menu-messages if not in upstream file
Patch0: gnome-menus-2.27.92-l10n.patch
# (fc) 2.16.0-2mdv unclutter preferences/settings menu
Patch1: gnome-menus-2.23.1-uncluttermenu.patch
License: LGPLv2+
Group: System/Libraries
Url: http://www.gnome.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: glib2-devel >= 2.5.6
BuildRequires: intltool >= 0.40.0
BuildRequires: python-devel
BuildRequires: gobject-introspection-devel
Requires: python-%{name}

%description
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

Also contained here are the GNOME menu layout configuration files,
.directory files and assorted menu related utility programs.

%package -n python-%{name}
Group: Development/Python
Summary: Module to access XDG menu

%description -n python-%{name}
Python module to access XDG menu.

%package -n %libname
Group: System/Libraries
Summary: GNOME menu library
Conflicts: gir-repository < 0.6.5-8

%description -n %libname
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

%package -n %libnamedev
Group: Development/C
Summary: GNOME menu library development files
Requires: %libname = %version
Provides: libgnome-menu-devel = %version-%release
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %mklibname -d gnome-menu 2
Conflicts: gir-repository < 0.6.5-8

%description -n %libnamedev
The package contains an implementation of the draft "Desktop Menu
Specification" from freedesktop.org:
http://www.freedesktop.org/Standards/menu-spec

%prep
%setup -q
%patch0 -p1 -b .l10n
%patch1 -p1 -b .uncluttermenu

%build
%configure2_5x 
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
# gw these produce rpmlint errors:
rm -rf %buildroot%_datadir/locale/{io,be@latin,bn_IN,si,uz@cyrillic}
%find_lang %name

mkdir -p $RPM_BUILD_ROOT%_sysconfdir/xdg/gnome
mv $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus $RPM_BUILD_ROOT%{_sysconfdir}/xdg/gnome

chmod 755 %buildroot%_libdir/python*/site-packages/GMenuSimpleEditor/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README NEWS HACKING AUTHORS ChangeLog
%_datadir/desktop-directories
%dir %_sysconfdir/xdg/gnome
%dir %_sysconfdir/xdg/gnome/menus
%config(noreplace) %_sysconfdir/xdg/gnome/menus/*
%_bindir/*
%_datadir/applications/*
%_datadir/%{name}

%files -n python-%{name}
%defattr(-,root,root)
%_libdir/python*/site-packages/*

%files -n %libname
%defattr(-,root,root)
%_libdir/libgnome-menu.so.%{major}*
%_libdir/girepository-1.0/GMenu-%api.typelib

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/lib*.so
%_libdir/lib*.la
%_libdir/lib*.a
%_includedir/gnome-menus/
%_libdir/pkgconfig/*.pc
%_datadir/gir-1.0/GMenu-%api.gir

