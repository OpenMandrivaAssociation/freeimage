%define name freeimage
%define version 3.153
%define release 1
%define oname FreeImage
%define oversion 3.15.3
%define common_summary Image library
%define common_description FreeImage is an Open Source library project for developers who would\
like to support popular graphics image formats like PNG, BMP, JPEG,\
TIFF and others as needed by today's multimedia applications.\
FreeImage is easy to use, fast, multithreading safe, compatible with\
all 32-bit versions of Windows, and cross-platform (works both with\
Linux and Mac OS X).

%define major 3
%define lib_name %mklibname %{name} %{major}
%define devel_name %mklibname %{name} -d

Summary: %{common_summary}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://downloads.sourceforge.net/freeimage/FreeImage3153.zip
Patch0:	FreeImage-3.11.0-syslibs.patch
License: GPLv2+
Group: System/Libraries
URL: http://freeimage.sourceforge.net/
%if 0
BuildRequires:	png-devel
BuildRequires:	mng-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	openjpeg-devel
%endif
Obsoletes: %{oname}

%description
%{common_description}

%package -n	%{lib_name}
Summary:	A library to %{common_summary}
Group:		System/Libraries
Obsoletes:	%{_lib}%{oname}3 < 3.110

%description -n	%{lib_name}
%{common_description}

This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devel_name}
Summary:	Development tools for programs using %{name}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	lib%{name}3-devel
Obsoletes:	lib%{oname}3-devel
Obsoletes:	%{_lib}%{oname}3-devel < 3.110

%description -n	%{devel_name}
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q -n %{oname}
%if 0
%patch0 -p1 -b .syslibs

touch -r Source/FreeImage.h.syslibs Source/FreeImage.h

# remove all included libs to make sure these don't get used during compile
rm -r Source/Lib* Source/ZLib Source/OpenEXR

# some encoding / line ending cleanups
iconv -f ISO-8859-1 -t UTF-8 Whatsnew.txt > Whatsnew.txt.tmp
touch -r Whatsnew.txt Whatsnew.txt.tmp
mv Whatsnew.txt.tmp Whatsnew.txt
%endif
sed -i 's/\r//g' Whatsnew.txt license-*.txt gensrclist.sh \
  Wrapper/FreeImagePlus/WhatsNew_FIP.txt

perl -pi -e 's/ -o root -g root//' Makefile.gnu
perl -pi -e 's/\bldconfig//' Makefile.gnu

%build
sh ./gensrclist.sh
%setup_compile_flags CFLAGS="%optflags -fPIC"
%make LIBRARIES="-lstdc++ -lm"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir} %{buildroot}%{_libdir}

%make install \
  INCDIR=%{buildroot}%{_includedir} \
  INSTALLDIR=%{buildroot}%{_libdir}


%files -n %{lib_name}
%doc Whatsnew.txt license-*.txt Wrapper/FreeImagePlus/WhatsNew_FIP.txt README.linux
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}-%{oversion}.so

%files -n %{devel_name}
%{_includedir}/%{oname}*.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a



%changelog
* Sun Mar 18 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.153-1
+ Revision: 785480
- version update 3153

* Tue Mar 06 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.151-1
+ Revision: 782378
- version update  3151

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.110-9mdv2011.0
+ Revision: 610755
- rebuild

* Wed Mar 17 2010 Anssi Hannula <anssi@mandriva.org> 3.110-8mdv2010.1
+ Revision: 524741
- rediff syslibs.patch
- add more obsoletes

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Tue Sep 02 2008 Emmanuel Andry <eandry@mandriva.org> 3.110-6mdv2009.0
+ Revision: 279299
- fix P0 (initG3 was still present in Plugin.cpp)

* Tue Sep 02 2008 Emmanuel Andry <eandry@mandriva.org> 3.110-5mdv2009.0
+ Revision: 279259
- don't need freeimageplus
- use makeinstall macro, does a better job than a manual install

* Tue Sep 02 2008 Emmanuel Andry <eandry@mandriva.org> 3.110-4mdv2009.0
+ Revision: 279171
- add missing symlinks
- manually install files, makeinstall forget files
- package doc

* Tue Sep 02 2008 Emmanuel Andry <eandry@mandriva.org> 3.110-3mdv2009.0
+ Revision: 278766
- move file in the right package

* Mon Sep 01 2008 Emmanuel Andry <eandry@mandriva.org> 3.110-2mdv2009.0
+ Revision: 278487
- fix license
- use system libs with P0 from fedora (rediffed)
- BR openjpeg-devel

* Mon Aug 18 2008 Emmanuel Andry <eandry@mandriva.org> 3.110-1mdv2009.0
+ Revision: 273176
- New version
- fully apply libraries policy
- add missing BR

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 3.93-3mdv2009.0
+ Revision: 240722
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Apr 27 2007 Olivier Blin <blino@mandriva.org> 3.93-1mdv2008.0
+ Revision: 18678
- initial FreeImage package
- Create freeimage

