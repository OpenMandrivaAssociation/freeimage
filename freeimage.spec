%define name freeimage
%define version 3.110
%define release %mkrel 5
%define oname FreeImage
%define oversion 3.11.0
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
Source0: %{oname}3110.zip
Patch0:	FreeImage-3.11.0-syslibs.patch
License: GPLv2+
Group: System/Libraries
URL: http://freeimage.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	png-devel
BuildRequires:	mng-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	openjpeg-devel
Obsoletes: %{oname}

%description
%{common_description}

%package -n	%{lib_name}
Summary:	A library to %{common_summary}
Group:		System/Libraries

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

%description -n	%{devel_name}
%{common_description}

This package contains the header files and libraries needed for
developing programs using the %{name} library.

%prep
%setup -q -n %{oname}
%patch0 -p1 -z .syslibs

touch -r Source/FreeImage.h.syslibs Source/FreeImage.h

# remove all included libs to make sure these don't get used during compile
rm -r Source/Lib* Source/ZLib Source/OpenEXR

# some encoding / line ending cleanups
iconv -f ISO-8859-1 -t UTF-8 Whatsnew.txt > Whatsnew.txt.tmp
touch -r Whatsnew.txt Whatsnew.txt.tmp
mv Whatsnew.txt.tmp Whatsnew.txt
sed -i 's/\r//g' Whatsnew.txt license-*.txt gensrclist.sh \
  Wrapper/FreeImagePlus/WhatsNew_FIP.txt

perl -pi -e 's/ -o root -g root//' Makefile.gnu
perl -pi -e 's/\bldconfig//' Makefile.gnu



%build
sh ./gensrclist.sh
#%make COMPILERFLAGS="$RPM_OPT_FLAGS -fPIC -fvisibility=hidden `pkg-config --cflags OpenEXR`"
%make

# build libfreeimageplus DIY, as the provided makefile makes libfreeimageplus
# contain a private copy of libfreeimage <sigh>
#FIP_OBJS=
#for i in Wrapper/FreeImagePlus/src/fip*.cpp; do
#  gcc -o $i.o $RPM_OPT_FLAGS -fPIC -fvisibility=hidden \
#    -ISource -IWrapper/FreeImagePlus -c $i
#  FIP_OBJS="$FIP_OBJS $i.o"
#done
#gcc -shared -LDist -o Dist/lib%{name}plus-%{oversion}.so \
#  -Wl,-soname,lib%{name}plus.so.%{major} $FIP_OBJS -lfreeimage-%{oversion}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir} %{buildroot}%{_libdir}

%make install \
  INCDIR=%{buildroot}%{_includedir} \
  INSTALLDIR=%{buildroot}%{_libdir}


#install -m 755 Dist/lib%{name}-%{oversion}.so %{buildroot}%{_libdir}
#ln -s lib%{name}-%{oversion}.so %{buildroot}%{_libdir}/lib%{name}.so.%{major}
#ln -s lib%{name}-%{oversion}.so %{buildroot}%{_libdir}/lib%{name}.so

#install -m 755 Dist/lib%{name}plus-%{oversion}.so %{buildroot}%{_libdir}
#ln -s lib%{name}plus-%{oversion}.so \
#  %{buildroot}%{_libdir}/lib%{name}plus.so.%{major}
#ln -s lib%{name}plus-%{oversion}.so %{buildroot}%{_libdir}/lib%{name}plus.so

#install -p -m 644 Source/FreeImage.h %{buildroot}%{_includedir}
#install -p -m 644 Wrapper/FreeImagePlus/FreeImagePlus.h \
#  %{buildroot}%{_includedir}


%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name}
%defattr(-,root,root)
%doc Whatsnew.txt license-*.txt Wrapper/FreeImagePlus/WhatsNew_FIP.txt README.linux
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}-%{oversion}.so

%files -n %{devel_name}
%defattr(-,root,root)
%{_includedir}/%{oname}*.h
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a



