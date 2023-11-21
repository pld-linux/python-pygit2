#
# Conditional build:
%bcond_with	tests	# unit tests

%define		module		pygit2
%define		egg_name	pygit2
%define		pypi_name	pygit2
Summary:	Python bindings for libgit2 library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libgit2
Name:		python-%{module}
Version:	1.13.3
Release:	1
License:	GPL v2 with linking exception
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pygit2/
Source0:	https://files.pythonhosted.org/packages/source/p/pygit2/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	9363b49de112bd6648b4b1ffe7ac0f02
URL:		https://pypi.org/project/pygit2/
BuildRequires:	libgit2-devel >= 1.4
BuildRequires:	python3-cffi >= 1.16.0
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%{?with_tests:BuildRequires:	python3-pytest}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pygit2 is a set of Python bindings to the libgit2 shared library.

%description -l pl.UTF-8
pygit2 to zbiór wiązań Pythona do biblioteki współdzielonej libgit2.

%package -n python3-%{module}
Summary:	Python 3.x bindings for libgit2 library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki libgit2
Group:		Libraries/Python
Requires:	libgit2 >= 1.4

%description -n python3-%{module}
pygit2 is a set of Python bindings to the libgit2 shared library.

%description -n python3-%{module} -l pl.UTF-8
pygit2 to zbiór wiązań Pythona do biblioteki współdzielonej libgit2.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst README.rst SPONSORS.rst
%dir %{py3_sitedir}/pygit2
%{py3_sitedir}/pygit2/decl
%{py3_sitedir}/pygit2/*.py
%{py3_sitedir}/pygit2/*.pyi
%{py3_sitedir}/pygit2/__pycache__
%attr(755,root,root) %{py3_sitedir}/pygit2/_libgit2.abi3.so
%attr(755,root,root) %{py3_sitedir}/pygit2/_pygit2.cpython-*.so
%{py3_sitedir}/pygit2-%{version}-py*.egg-info
