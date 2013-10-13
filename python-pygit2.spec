#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python3 # CPython 3.x module
%bcond_without	docs	# documentation

%define 	module	pygit2
Summary:	Python bindings for libgit2 library
Name:		python-%{module}
Version:	0.19.1
Release:	2
License:	GPL v2 with linking exception
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/p//pygit2/%{module}-%{version}.tar.gz
# Source0-md5:	6c61833605bb52a483141780ad233584
Patch0:		%{name}-docbuild.patch
URL:		https://pypi.python.org/pypi/pygit2
BuildRequires:	libgit2-devel >= 0.19.0
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
%{?with_docs:BuildRequires:     sphinx-pdg}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
pygit2 is a set of Python bindings to the libgit2 shared library.

%package -n python3-%{module}
Summary:	Python bindings for libgit2 library

%description -n python3-%{module}
pygit2 is a set of Python bindings to the libgit2 shared library.

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
%patch0 -p0

%build
%{__python} setup.py build --build-base build-2
%if %{with python3}
%{__python3} setup.py build --build-base build-3
%endif

%{?with_tests:%{__python} setup.py build -b build-2 test}

%if %{with python3}
%{__python3} setup.py \
	build -b build-3

%if %{with tests}
%{__python3} setup.py build -b build-3 test
%endif
%endif

%if %{with docs}
cd docs
PACKAGE_BUILD=../build-2 %{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} -- setup.py \
	build -b build-2 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%endif

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.txt
%dir %{py_sitedir}/%{module}
%{py_sitedir}/pygit2/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/pygit2-*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING README.rst TODO.txt
%dir %{py3_sitedir}/%{module}
%attr(755,root,root) %{py3_sitedir}/*.so
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/__pycache__
%{py3_sitedir}/pygit2-*.egg-info
%endif

%if %{with docs}
%files apidoc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
