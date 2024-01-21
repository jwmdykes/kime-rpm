Name:			kime
Version:		3.0.2
Release:		%autorelease
Summary:		Korean IME
License:		GPLv3
URL:			https://github.com/Riey/kime
Source:			https://github.com/Riey/kime/archive/refs/tags/v3.0.2.tar.gz
BuildRequires:	rust
BuildRequires:	cargo
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	llvm-devel
BuildRequires:	clang-devel
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel

%define kime_conf_dir /etc/xdg/%{name}
%define kime_inc_dir %{_includedir}
%define kime_lib_dir %{_libdir}
%define kime_gtk3_dir %{_libdir}/gtk-3.0/3.0.0/immodules
%define kime_qt5_dir %{_libdir}/qt5/plugins/platforminputcontexts
%define kime_icons_dir %{_datadir}/%{name}/icons/64x64
%define kime_build_dir build/out

%description
GTK및 QT5 대부분 프로그램에서 한글을 입력할 수 있는 새로운 한글 입력기

%prep
%autosetup

%build
scripts/build.sh -ar

%install
rm -rf %{buildroot}
install -d -p  %{buildroot}%{_bindir}
install -d -p  %{buildroot}%{kime_qt5_dir}
install -d -p  %{buildroot}%{kime_gtk3_dir}
install -d -p  %{buildroot}%{kime_inc_dir}
install -d -p  %{buildroot}%{kime_icons_dir}
install -d -p  %{buildroot}%{kime_conf_dir}

# Install executables
install -Dm 0755 %{kime_build_dir}/kime %{buildroot}%{_bindir}
install -Dm 0755 %{kime_build_dir}/kime-candidate-window %{buildroot}%{_bindir}
install -Dm 0755 %{kime_build_dir}/kime-check %{buildroot}%{_bindir}
install -Dm 0755 %{kime_build_dir}/kime-indicator %{buildroot}%{_bindir}
install -Dm 0755 %{kime_build_dir}/kime-wayland %{buildroot}%{_bindir}
install -Dm 0755 %{kime_build_dir}/kime-xim %{buildroot}%{_bindir}

# Install shared libraries
install -Dm 0755 %{kime_build_dir}/libkime_engine.so %{buildroot}%{_libdir}
install -Dm 0755 %{kime_build_dir}/libkime-gtk3.so %{buildroot}%{kime_gtk3_dir}/im-kime.so
install -Dm 0755 %{kime_build_dir}/libkime-qt5.so %{buildroot}%{kime_qt5_dir}/libkimeplatforminputcontextplugin.so
install -Dm 0755 %{kime_build_dir}/libkime-qt6.so %{buildroot}%{kime_qt6_dir}/libkimeplatforminputcontextplugin.so

# Install icons
install -Dm 0644 %{kime_build_dir}/icons/* %{buildroot}%{kime_icons_dir}/

# Install configuration
install -Dm 0644 %{kime_build_dir}/default_config.yaml %{buildroot}%{kime_conf_dir}/config.yaml

# Install header files
install -Dm 0644 %{kime_build_dir}/kime_engine.hpp %{buildroot}%{kime_inc_dir}
install -Dm 0644 %{kime_build_dir}/kime_engine.h %{buildroot}%{kime_inc_dir}

# install desktop file
desktop-file-install --vendor "" \
			--dir %{buildroot}%{_desktopdir} %{buildroot}%/kime.desktop

%clean
rm -rf %{buildroot}

%post
gtk-query-immodules-3.0-64 --update-cache

%postun
gtk-query-immodules-3.0-64 --update-cache

%files
%defattr(-,root,root)
%doc %{kime_build_dir}/LICENSE %{kime_build_dir}/NOTICE.md
%{buildroot}%{_bindir}/kime
%{buildroot}%{_bindir}/kime-*
%{buildroot}%{_libdir}/libkime_engine.so
%{buildroot}%{_libdir}/libkime-gtk3.so
%{buildroot}%{_libdir}/libkime_engine.so
%{buildroot}%{_libdir}/libkime_engine.so


%changelog
%autochangelog