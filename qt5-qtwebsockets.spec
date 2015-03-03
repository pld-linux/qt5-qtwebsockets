#
# Conditional build:
%bcond_without	qch	# documentation in QCH format

%define		orgname		qtwebsockets
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 WebSockets library
Summary(pl.UTF-8):	Biblioteka Qt5 WebSockets
Name:		qt5-%{orgname}
Version:	5.4.1
Release:	1
License:	LGPL v2.1 with Digia Qt LGPL Exception v1.1 or GPL v3.0
Group:		X11/Libraries
Source0:	http://download.qt-project.org/official_releases/qt/5.4/%{version}/submodules/%{orgname}-opensource-src-%{version}.tar.xz
# Source0-md5:	308e1e9126e6fab8b06616db9810973e
URL:		http://qt-project.org/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Sql-devel >= %{qtbase_ver}
%if %{with qch}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpmbuild(macros) >= 1.654
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 WebSockets library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 WebSockets.

%package -n Qt5WebSockets
Summary:	The Qt5 WebSockets library
Summary(pl.UTF-8):	Biblioteka Qt5 WebSockets
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Network >= %{qtbase_ver}
Requires:	Qt5Sql >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}

%description -n Qt5WebSockets
Qt5 WebSockets library provides WebSockets communication classes.

%description -n Qt5WebSockets -l pl.UTF-8
Biblioteka Qt5 WebSockets dostarcza klasy do komunikacji przez
WebSockets.

%package -n Qt5WebSockets-devel
Summary:	Qt5 WebSockets library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 WebSockets - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}
Requires:	Qt5Sql-devel >= %{qtbase_ver}
Requires:	Qt5WebSockets = %{version}-%{release}

%description -n Qt5WebSockets-devel
Qt5 WebSockets library - development files.

%description -n Qt5WebSockets-devel -l pl.UTF-8
Biblioteka Qt5 WebSockets - pliki programistyczne.

%package doc
Summary:	Qt5 WebSockets documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebSockets w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Qt5 WebSockets documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebSockets w formacie HTML.

%package doc-qch
Summary:	Qt5 WebSockets documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebSockets w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-qch
Qt5 WebSockets documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebSockets w formacie QCH.

%package examples
Summary:	Qt5 WebSockets examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 WebSockets
Group:		X11/Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Qt5 WebSockets examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 WebSockets.

%prep
%setup -q -n %{orgname}-opensource-src-%{version}

%build
qmake-qt5
%{__make}
%{__make} %{!?with_qch:html_}docs

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install_%{!?with_qch:html_}docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.?
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/websockets

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5WebSockets -p /sbin/ldconfig
%postun	-n Qt5WebSockets -p /sbin/ldconfig

%files -n Qt5WebSockets
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libQt5WebSockets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5WebSockets.so.5
%dir %{qt5dir}/qml/Qt/WebSockets
%attr(755,root,root) %{qt5dir}/qml/Qt/WebSockets/libdeclarative_qmlwebsockets.so
%{qt5dir}/qml/Qt/WebSockets/plugins.qmltypes
%{qt5dir}/qml/Qt/WebSockets/qmldir

%files -n Qt5WebSockets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5WebSockets.so
%{_libdir}/libQt5WebSockets.prl
%{_includedir}/qt5/QtWebSockets
%{_pkgconfigdir}/Qt5WebSockets.pc
%{_libdir}/cmake/Qt5WebSockets
%{qt5dir}/mkspecs/modules/qt_lib_websockets.pri
%{qt5dir}/mkspecs/modules/qt_lib_websockets_private.pri

%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebsockets

%if %{with qch}
%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebsockets.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
