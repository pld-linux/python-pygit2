#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	doc	# documentation
%bcond_with	tests	# unit tests

%define		module		pygit2
%define		egg_name	pygit2
%define		pypi_name	pygit2
Summary:	Python 2.x bindings for libgit2 library
Summary(pl.UTF-8):	Wiązania Pythona 2.x do biblioteki libgit2
Name:		python-%{module}
Version:	0.28.2
Release:	1
License:	GPL v2 with linking exception
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pygit2/
Source0:	https://files.pythonhosted.org/packages/source/p/pygit2/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	e5fad67c46e2ebf3391cb9650684923d
Patch0:		%{name}-docbuild.patch
URL:		https://pypi.org/project/pygit2/
BuildRequires:	libgit2-devel >= 0.27.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-cffi >= 1.8.1
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.8.1
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
%{?with_doc:BuildRequires:     sphinx-pdg-3}
Requires:	libgit2 >= 0.24.0
Requires:	python-cffi
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pygit2 is a set of Python bindings to the libgit2 shared library.

%description -l pl.UTF-8
pygit2 to zbiór wiązań Pythona do biblioteki współdzielonej libgit2.

%package -n python3-%{module}
Summary:	Python 3.x bindings for libgit2 library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki libgit2
Group:		Libraries/Python
Requires:	libgit2 >= 0.24.0
Requires:	python3-cffi

%description -n python3-%{module}
pygit2 is a set of Python bindings to the libgit2 shared library.

%description -n python3-%{module} -l pl.UTF-8
pygit2 to zbiór wiązań Pythona do biblioteki współdzielonej libgit2.

%package apidocs
Summary:	pygit2 module API documentation
Summary(pl.UTF-8):	Dokumentacja API modułu pygit2
Group:		Documentation
Obsoletes:	python-pygit2-apidoc < 0.24.0-2
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for pygit2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu pygit2.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%{?with_tests:PYTHONPATH=$(echo $(pwd)/build-2/lib.*) %{__python} -m pytest test}
%endif

%if %{with python3}
%py3_build

%{?with_tests:PYTHONPATH=$(echo $(pwd)/build-3/lib.*) %{__python3} -m pytest test}
%endif

%if %{with doc}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__make} -C docs -j1 html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if%{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.txt
%dir %{py_sitedir}/pygit2
%{py_sitedir}/pygit2/*.py[co]
%{py_sitedir}/pygit2/decl
%attr(755,root,root) %{py_sitedir}/pygit2/_libgit2.so
%attr(755,root,root) %{py_sitedir}/_pygit2.so
%{py_sitedir}/pygit2-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.txt
%dir %{py3_sitedir}/pygit2
%{py3_sitedir}/pygit2/decl
%{py3_sitedir}/pygit2/*.py
%{py3_sitedir}/pygit2/__pycache__
%attr(755,root,root) %{py3_sitedir}/pygit2/_libgit2.abi3.so
%attr(755,root,root) %{py3_sitedir}/_pygit2.cpython-*.so
%{py3_sitedir}/pygit2-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,recipes,*.html,*.js}
%endif
