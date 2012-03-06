%define name freeimage
%define version 3.151
%define release 1
%define oname FreeImage
%define oversion 3.15.1
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
Source0: http://downloads.sourceforge.net/freeimage/FreeImage3151.zip
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

