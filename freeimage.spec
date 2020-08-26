%define debug_package	%nil

%define oname	FreeImage
%define oversion 3.18.0
%define major	4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Image library
Name:		freeimage
Version:	3.180
Release:	2
License:	GPLv2+
Group:		System/Libraries
Url:		http://freeimage.sourceforge.net/
Source0:	http://downloads.sourceforge.net/freeimage/FreeImage3180.zip
# Unbundle bundled libraries
Patch0:         FreeImage_unbundle.patch
# Fix incorrect path in doxyfile
Patch1:         FreeImage_doxygen.patch
# Fix incorrect variable names in BIGENDIAN blocks
Patch2:         FreeImage_bigendian.patch
# Fixing permission issue (cannot change ownership of ...) MGA patch.
Patch10:        FreeImage-3.17.0-mga-makeinstall.patch
# Fix compiling with raw 0.20.0 https://bugs.gentoo.org/734724
Patch11:        fix-compiling-with-libraw-0.20.0.diff
BuildRequires:  doxygen
BuildRequires:  jxrlib-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libmng)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libraw)

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
%autosetup -p1 -n %{oname}

# remove all included libs to make sure these don't get used during compile
rm -r Source/Lib* Source/ZLib Source/OpenEXR

# clear files which cannot be built due to dependencies on private headers
# (see also unbundle patch)
> Source/FreeImage/PluginG3.cpp
> Source/FreeImageToolkit/JPEGTransform.cpp

# sanitize encodings / line endings
for file in `find . -type f -name '*.c' -or -name '*.cpp' -or -name '*.h' -or -name '*.txt' -or -name Makefile`; do
  iconv --from=ISO-8859-15 --to=UTF-8 $file > $file.new && \
  sed -i 's|\r||g' $file.new && \
  touch -r $file $file.new && mv $file.new $file
done

%build
sh ./gensrclist.sh
sh ./genfipsrclist.sh

#%ifarch %{armx}
#%make_build -f Makefile.gnu CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" LDFLAGS="%{_ldflags}"
#%make_build -f Makefile.fip CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" LDFLAGS="%{_ldflags}"
#%else
#%make_build -f Makefile.gnu CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{_ldflags}"
#%make_build -f Makefile.fip CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{_ldflags}"
#%endif

pushd Wrapper/FreeImagePlus/doc
doxygen FreeImagePlus.dox
popd
%make_build LIBRARIES="-std=c++11 -Wno-c++11-narrowing -lstdc++ -lm"

%install
%make_install \
 	  INCDIR=%{buildroot}%{_includedir} \
 	  INSTALLDIR=%{buildroot}%{_libdir}

# We don't package static libs
rm -f %{buildroot}%{_libdir}/lib%{name}.a

%files -n %{libname}
%doc Whatsnew.txt license-*.txt Wrapper/FreeImagePlus/WhatsNew_FIP.txt README.linux
%{_libdir}/lib%{name}.so.%{major}
%{_libdir}/lib%{name}-%{oversion}.so

%files -n %{devname}
%{_includedir}/%{oname}*.h
%{_libdir}/lib%{name}.so

