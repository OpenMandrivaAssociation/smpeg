%define	lib_name_orig	libsmpeg
# this is really the API, the major is 0
%define	lib_major	0.4
%define	lib_name	%mklibname %{name} %{lib_major}
%define	develname	%mklibname %{name} -d

Summary:	SDL MPEG Library
Name:		smpeg
Version:	0.4.4
Release:	56
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
Patch6:		smpeg-0.4.4-remove-gtk1.patch
Patch7:		smpeg-0.4.4-automake.patch
#BuildRequires:	pkgconfig(esound)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	libstdc++-static-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(slang)
BuildRequires:	zlib-devel

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder and SPLAY,
an mpeg audio decoder created by Woo-jae Jung. We have completed the
initial work to wed these two projects in order to create a general
purpose MPEG video/audio player for the Linux OS.

%package -n	%{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{lib_name}-devel
Obsoletes:	%{mklibname smpeg 0.4 -d} < 0.4.4-44
#gw smpeg-config calls sdl-config
Requires:	pkgconfig(sdl)

%description -n	%{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n	%{name}-player
Summary:	Simple MPEG player based on %{name} library
Group:		Video

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
%configure2_5x --disable-static
# (gc) this sucking rpath thing...
perl -pi -e 's/finalize_rpath="\$rpath"/finalize_rpath=/' libtool
make

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/smpeg-config

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
%{multiarch_bindir}/smpeg-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_datadir}/aclocal/smpeg.m4

%changelog
* Tue Oct 25 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.4.4-44
+ Revision: 707023
- rebuild
  dropped api from the devel pkg

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 0.4.4-43
+ Revision: 662077
- fix build

  + Oden Eriksson <oeriksson@mandriva.com>
    - multiarch fixes

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.4-42mdv2011.0
+ Revision: 607546
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.4.4-41mdv2010.0
+ Revision: 427199
- rebuild

* Fri Mar 20 2009 Michael Scherer <misc@mandriva.org> 0.4.4-40mdv2009.1
+ Revision: 359135
- completly remove gtk1 ( as we recreate the configure, the option was not enough )
- disable gtk1 player, so we can get ride of gtk1

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.4-39mdv2009.1
+ Revision: 317835
- fix build with -Werror=format-security (P5)

* Sun Aug 17 2008 Funda Wang <fwang@mandriva.org> 0.4.4-38mdv2009.0
+ Revision: 273025
- rebuild for new dfb

* Fri Jul 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.4-37mdv2009.0
+ Revision: 231787
- fix deps
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.4-35mdv2008.1
+ Revision: 179508
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Herton Ronaldo Krzesinski <herton@mandriva.com.br>
    - Updated URL field.


* Mon Feb 19 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.4.4-33mdv2007.0
+ Revision: 122860
- Rebuilt.

* Mon Feb 19 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.4.4-32mdv2007.1
+ Revision: 122825
- Rebuilt against latest rpm-mandriva-setup.

* Mon Feb 19 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.4.4-31mdv2007.1
+ Revision: 122700
- rebuilt again.

* Mon Feb 19 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.4.4-30mdv2007.1
+ Revision: 122658
- Rebuilt against latest libggi.

* Mon Jan 15 2007 Götz Waschk <waschk@mandriva.org> 0.4.4-29mdv2007.1
+ Revision: 109041
- patch to fix build with current gcc
- unpack patches

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Add XDG Menu
    - Remove old debian menu
    - Import smpeg

* Wed Jan 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.4.4-28mdk
- fix underquoted calls (P3)
- %%mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.4.4-27mdk
- Rebuild

* Mon Jan 31 2005 Olivier Blin <blino@mandrake.org> 0.4.4-26mdk
- multiarch support

* Fri Nov 12 2004 Götz Waschk <waschk@linux-mandrake.com> 0.4.4-25mdk
- rebuild

* Fri Jun 18 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.4.4-24mdk
- rebuild
- force use of automake1.4
- cosmetics

