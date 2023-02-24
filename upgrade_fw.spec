%{?!python_module:%define python_module() python-%{**} python3-%{**}}

Name: upgrade_fw
Version:       1.0.0
Release:       1
Summary:       Firmware upgrade tool
License:       MIT
Source:        https://gitlab.com/nori/upgrade_fw/%{name}-%{version}.tar.xz
BuildRequires: %{python_module setuptools}
BuildRequires: python-setuptools
BuildRequires: python-rpm-macros
BuildRequires: python-rpm-generators
%{?python_enable_dependency_generator}
Requires:      python-yaml
BuildArch:     noarch
 
%description
Firmware upgrade tool
 
%build
%python_build

%install
%python_install

%files
%files %{python_files}
 
%changelog
* Tue AUG 28 2022 INDETAIL - 1.0.0
- Initial release
