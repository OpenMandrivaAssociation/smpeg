%global optflags %{optflags} -Wno-error=narrowing

%define lib_name_orig libsmpeg
# this is really the API, the major is 0
%define lib_major 0.4
%define lib_name %mklibname %{name} %{lib_major}
%define develname %mklibname %{name} -d

%define _disable_lto 1
%define _disable_rebuild_configure 1
%global optflags %{optflags} -Wno-c++11-narrowing

Summary:	SDL MPEG Library
Name:		smpeg
Version:	0.4.5
Release:	2
License:	LGPL
Group:		Video
URL:		http://icculus.org/smpeg/
Source0:	%{name}-%{version}.tar.xz
Patch0:		smpeg-0.4.5-libsupc++.patch
Patch1:		smpeg-0.4.5-fix-header.patch
Patch2:		smpeg-0.4.4-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		smpeg-0.4.5-link.patch
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	libstdc++-static-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(slang)
BuildRequires:	pkgconfig(zlib)

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder and SPLAY,
an mpeg audio decoder created by Woo-jae Jung. We have completed the
initial work to wed these two projects in order to create a general
purpose MPEG video/audio player for the Linux OS.

%package -n %{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{lib_name}-devel
Obsoletes:	%{mklibname smpeg 0.4 -d} < 0.4.4-44
#gw smpeg-config calls sdl-config
Requires:	pkgconfig(sdl)

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n %{name}-player
Summary:	Simple MPEG player based on %{name} library
Group:		Video

%description -n %{name}-player
This package contains a MPEG player based on %{name}.

%prep
%setup -q

%patch0 -p1 -b .libsupc++
%patch1 -p1 -b .header
%patch2 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch3 -p0 -b .link

touch NEWS AUTHORS ChangeLog
cd acinclude
rm -f lt*.m4 libtool.m4
cd -

autoreconf -fi -Iacinclude

%build
%configure \
%ifarch x86
	--disable-mmx \
%endif
	--disable-rpath

%make_build

%install
%make_install

%files -n %{name}-player
%doc README
%{_bindir}/plaympeg
%{_bindir}/glmovie
%{_mandir}/*/*

%files -n %{lib_name}
%doc README
%{_libdir}/lib*.so.*

%files -n %{develname}
%doc CHANGES COPYING README
%{_bindir}/smpeg-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_datadir}/aclocal/smpeg.m4
