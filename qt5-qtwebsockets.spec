#
# Conditional build:
%bcond_without	doc	# Documentation
%bcond_without	qm	# QM translations

%define		orgname		qtwebsockets
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 WebSockets library
Summary(pl.UTF-8):	Biblioteka Qt5 WebSockets
Name:		qt5-%{orgname}
Version:	5.15.17
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	9baed113b35ea6814f5247b68e2b76e9
Source1:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/qttranslations-everywhere-opensource-src-%{version}.tar.xz
# Source1-md5:	e20cfdef4f3088ca568f7e43ab5bba8c
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
# for examples
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
%{?with_qm:BuildRequires:	qt5-linguist >= 5.2}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
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
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Network >= %{qtbase_ver}
# for qml module
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
BuildArch:	noarch

%description doc
Qt5 WebSockets documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebSockets w formacie HTML.

%package doc-qch
Summary:	Qt5 WebSockets documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebSockets w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 WebSockets documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebSockets w formacie QCH.

%package examples
Summary:	Qt5 WebSockets examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 WebSockets
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 WebSockets examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 WebSockets.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version} %{?with_qm:-a1}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%if %{with qm}
cd qttranslations-everywhere-src-%{version}
%{qmake_qt5}
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%if %{with qm}
%{__make} -C qttranslations-everywhere-src-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
# keep only qtwebsockets
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt5/translations/{assistant,designer,linguist,qt,qtbase,qtconnectivity,qtdeclarative,qtlocation,qtmultimedia,qtquickcontrols,qtquickcontrols2,qtserialport,qtscript,qtwebengine,qtxmlpatterns}_*.qm
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
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

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_datadir}/locale/*/LC_MESSAGES layout
find_qt5_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt5/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtwebsockets.lang
%if %{with qm}
find_qt5_qm qtwebsockets >> qtwebsockets.lang
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5WebSockets -p /sbin/ldconfig
%postun	-n Qt5WebSockets -p /sbin/ldconfig

%files -n Qt5WebSockets -f qtwebsockets.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libQt5WebSockets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5WebSockets.so.5
%dir %{qt5dir}/qml/Qt/WebSockets
%{qt5dir}/qml/Qt/WebSockets/qmldir
%dir %{qt5dir}/qml/QtWebSockets
# R: Core Network Qml WebSockets
%attr(755,root,root) %{qt5dir}/qml/QtWebSockets/libdeclarative_qmlwebsockets.so
%{qt5dir}/qml/QtWebSockets/plugins.qmltypes
%{qt5dir}/qml/QtWebSockets/qmldir

%files -n Qt5WebSockets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5WebSockets.so
%{_libdir}/libQt5WebSockets.prl
%{_includedir}/qt5/QtWebSockets
%{_pkgconfigdir}/Qt5WebSockets.pc
%{_libdir}/cmake/Qt5WebSockets
%{qt5dir}/mkspecs/modules/qt_lib_websockets.pri
%{qt5dir}/mkspecs/modules/qt_lib_websockets_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebsockets

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebsockets.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
