%define	lib_name_orig	libsmpeg
%define	lib_major	0.4
%define	lib_name	%mklibname %name %{lib_major}

Summary:	SDL MPEG Library
Name:		smpeg
Version:	0.4.4
Release:	%mkrel 40
License:	LGPL
Group:		Video
URL:		http://icculus.org/smpeg/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		smpeg-remove-rpath-in-smpeg-config.patch
Patch1:		smpeg-0.4.4-libsupc++.patch
Patch2:		smpeg-0.4.4-fix-m4.patch
Patch3:		smpeg-0.4.4-fix-underquoted-calls.patch
Patch4:		smpeg-0.4.4-fix-header.patch
Patch5:		smpeg-0.4.4-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	automake1.4
BuildRequires:	esound-devel
BuildRequires:	Mesa-common-devel
BuildRequires:	ncurses-devel
BuildRequires:	SDL-devel
BuildRequires:	slang-devel
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder and SPLAY,
an mpeg audio decoder created by Woo-jae Jung. We have completed the
initial work to wed these two projects in order to create a general
purpose MPEG video/audio player for the Linux OS.

%package -n	%{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{lib_name}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
#gw smpeg-config calls sdl-config
Requires:	SDL-devel

%description -n	%{lib_name}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	%{name}-player
Summary:	Simple MPEG player based on %{name} library
Group:		Video
Obsoletes:	%{lib_name}-player
Provides:	%{lib_name}-player = %{version}-%{release}

%description -n	%{name}-player
This package contains a MPEG player based on %{name}.

%prep

%setup -q
%patch0 -p0
%patch1 -p1 -b .libsupc++
%patch2 -p0
%patch3 -p1 -b .underquoted
%patch4 -p1 -b .header
%patch5 -p0 -b .format_not_a_string_literal_and_no_format_arguments
# needed by Patch1
aclocal-1.4
automake-1.4 --foreign
autoconf

%build
%configure --disable-gtk-player
# (gc) this sucking rpath thing...
perl -pi -e 's/finalize_rpath="\$rpath"/finalize_rpath=/' libtool
make

%install
rm -rf %{buildroot}

#make prefix=%{buildroot}/%{_prefix} install

%makeinstall

%multiarch_binaries %{buildroot}%{_bindir}/smpeg-config

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{name}-player
%defattr(-, root, root)
%doc README
%{_bindir}/plaympeg
%{_bindir}/glmovie
%{_mandir}/*/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc README
%{_libdir}/lib*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc CHANGES COPYING README
%{_bindir}/smpeg-config
%multiarch %{multiarch_bindir}/smpeg-config
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_datadir}/aclocal/smpeg.m4
