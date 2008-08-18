%define name freeimage
%define version 3.110
%define release %mkrel 1
%define oname FreeImage
%define oversion %(echo %{version} | sed -e 's/\\.//g')
%define distname %{oname}%{oversion}
%define common_summary Image library
%define common_description FreeImage is an Open Source library project for developers who would\
like to support popular graphics image formats like PNG, BMP, JPEG,\
TIFF and others as needed by today's multimedia applications.\
FreeImage is easy to use, fast, multithreading safe, compatible with\
all 32-bit versions of Windows, and cross-platform (works both with\
Linux and Mac OS X).

%define lib_major 3
%define lib_name %mklibname %{name} %{lib_major}
%define devel_name %mklibname %{name} -d

Summary: %{common_summary}
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{distname}.zip
License: GPL
Group: System/Libraries
Url: http://freeimage.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	png-devel
BuildRequires:	mng-devel
BuildRequires:	jpeg-devel
BuildRequires:	tiff-devel
BuildRequires:	OpenEXR-devel
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
perl -pi -e 's/ -o root -g root//' Makefile.gnu
perl -pi -e 's/\bldconfig//' Makefile.gnu

%build
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir} %{buildroot}%{_libdir}
%make install \
  INCDIR=%{buildroot}%{_includedir} \
  INSTALLDIR=%{buildroot}%{_libdir}

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
%doc README.linux
%{_libdir}/*.so.%{lib_major}*

%files -n %{devel_name}
%defattr(-,root,root)
%{_includedir}/%{oname}.h
%{_libdir}/*.a
%{_libdir}/*.so
