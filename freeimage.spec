%define debug_package	%nil

%define oname	FreeImage
%define oversion 3.15.3
%define major	3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Image library
Name:		freeimage
Version:	3.153
Release:	8
License:	GPLv2+
Group:		System/Libraries
Url:		http://freeimage.sourceforge.net/
Source0:	http://downloads.sourceforge.net/freeimage/FreeImage3153.zip
Patch0:		FreeImage-3.11.0-syslibs.patch
%if 0
BuildRequires:	png-devel
BuildRequires:	mng-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	openjpeg-devel
%endif

%description
FreeImage is an Open Source library project for developers who would
like to support popular graphics image formats like PNG, BMP, JPEG,
TIFF and others as needed by today's multimedia applications.
FreeImage is easy to use, fast, multithreading safe, compatible with
all 32-bit versions of Windows, and cross-platform (works both with
Linux and Mac OS X).

%package -n	%{libname}
Summary:	A library to Image library
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{devname}
Summary:	Development tools for programs using %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -qn %{oname}
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

sed -i -e 's/ -o root -g root//' Makefile.gnu
sed -i -e 's/\bldconfig//' Makefile.gnu

%build
sh ./gensrclist.sh
%setup_compile_flags CFLAGS="%optflags -fPIC"
%make LIBRARIES="-lstdc++ -lm"

%install
mkdir -p %{buildroot}%{_includedir} %{buildroot}%{_libdir}

%make install \
  INCDIR=%{buildroot}%{_includedir} \
  INSTALLDIR=%{buildroot}%{_libdir}

rm -f %{buildroot}%{_libdir}/*.a

%files -n %{libname}
%doc Whatsnew.txt license-*.txt Wrapper/FreeImagePlus/WhatsNew_FIP.txt README.linux
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}-%{oversion}.so

%files -n %{devname}
%{_includedir}/%{oname}*.h
%{_libdir}/lib%{name}.so

