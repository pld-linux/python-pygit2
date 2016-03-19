# TODO:
# building doc requires pygit2 installed in system
#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python3 # CPython 3.x module
%bcond_without	docs	# documentation

%define 	module	pygit2
Summary:	Python 2.x bindings for libgit2 library
Summary(pl.UTF-8):	Wiązania Pythona 2.x do biblioteki libgit2
Name:		python-%{module}
Version:	0.23.2
Release:	2
License:	GPL v2 with linking exception
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/pypi/pygit2
Source0:	https://pypi.python.org/packages/source/p/pygit2/%{module}-%{version}.tar.gz
# Source0-md5:	c4b00f2add53e17a98c0ebe558d4db80
Patch0:		%{name}-docbuild.patch
URL:		https://pypi.python.org/pypi/pygit2
BuildRequires:	libgit2-devel >= 0.23.0
BuildRequires:	python-cffi
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python3}
BuildRequires:	python3-cffi
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
%{?with_docs:BuildRequires:     sphinx-pdg}
Requires:	libgit2 >= 0.23.0
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
Requires:	libgit2 >= 0.23.0
Requires:	python3-cffi

%description -n python3-%{module}
pygit2 is a set of Python bindings to the libgit2 shared library.

%description -n python3-%{module} -l pl.UTF-8
pygit2 to zbiór wiązań Pythona do biblioteki współdzielonej libgit2.

%package apidoc
Summary:	pygit2 API documentation
Summary(pl.UTF-8):	Dokumentacja API pygit2
Group:		Documentation

%description apidoc
API documentation for %{module}.

%description apidoc -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

# these tests use network
%{__rm} test/test_{credentials,repository}.py

%build
%py_build
%{?with_tests:%py_build test}

%if %{with python3}
%py3_build
%{?with_tests:%py3_build test}
%endif

%if %{with docs}
cd docs
PACKAGE_BUILD=../build-2 \
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py_postclean

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.txt
%dir %{py_sitedir}/pygit2
%{py_sitedir}/pygit2/*.py[co]
%{py_sitedir}/pygit2/decl.h
%attr(755,root,root) %{py_sitedir}/pygit2/_libgit2.so
%attr(755,root,root) %{py_sitedir}/_pygit2.so
%{py_sitedir}/pygit2-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.txt
%dir %{py3_sitedir}/pygit2
%{py3_sitedir}/pygit2/decl.h
%{py3_sitedir}/pygit2/*.py
%{py3_sitedir}/pygit2/__pycache__
%attr(755,root,root) %{py3_sitedir}/pygit2/_libgit2.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/_pygit2.cpython-*.so
%{py3_sitedir}/pygit2-%{version}-py*.egg-info
%endif

%if %{with docs}
%files apidoc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
