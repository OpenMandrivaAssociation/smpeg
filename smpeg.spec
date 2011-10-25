%define	lib_name_orig	libsmpeg
# this is really the API, the major is 0
%define	lib_major	0.4
%define	lib_name	%mklibname %name %{lib_major}
%define	develname	%mklibname %name -d

Summary:	SDL MPEG Library
Name:		smpeg
Version:	0.4.4
Release:	44
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
# (misc) since aclocal requires libgtk1-devel to regenerate the 
# configure script and others, we need to remove them from the file 
# with a axe. 
Patch6:     smpeg-0.4.4-remove-gtk1.patch
Patch7:		smpeg-0.4.4-automake.patch
BuildRequires:	esound-devel
BuildRequires:	Mesa-common-devel
BuildRequires:	libstdc++-static-devel
BuildRequires:	ncurses-devel
BuildRequires:	SDL-devel
BuildRequires:	slang-devel
BuildRequires:	zlib-devel

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

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{lib_name}-devel
Obsoletes:	%{mklibname %{name} %{lib_major} -d}
#gw smpeg-config calls sdl-config
Requires:	SDL-devel

%description -n	%{develname}
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
%patch6 -p0
%patch7 -p1

# needed by Patch1
touch NEWS AUTHORS ChangeLog
autoreconf -fi

%build
%configure2_5x
# (gc) this sucking rpath thing...
perl -pi -e 's/finalize_rpath="\$rpath"/finalize_rpath=/' libtool
make

%install
rm -rf %{buildroot}

%makeinstall_std

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

%files -n %{develname}
%defattr(-, root, root)
%doc CHANGES COPYING README
%{_bindir}/smpeg-config
%{multiarch_bindir}/smpeg-config
%{_includedir}/*
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_datadir}/aclocal/smpeg.m4
