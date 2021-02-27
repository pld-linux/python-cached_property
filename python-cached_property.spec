#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	cached_property
Summary:	A cached-property for decorating methods in Python classes
Name:		python-%{module}
Version:	1.3.0
Release:	5
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/pydanny/cached-property/archive/34b1caf8/cached-property-%{version}.tar.gz
# Source0-md5:	973727514d27e4f4a07358802c4943dc
URL:		https://github.com/pydanny/cached-property
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-freezegun
BuildRequires:	python-pytest
BuildRequires:	python-tox >= 1.7.2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-freezegun
BuildRequires:	python3-pytest
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cached_property allows properties in Python classes to be cached until
the cache is invalidated or expired.

%package -n python3-%{module}
Summary:	A cached-property for decorating methods in Python classes
Group:		Libraries/Python

%description -n python3-%{module}
cached_property allows properties in Python classes to be cached until
the cache is invalidated or expired.

%prep
%setup -qc
mv cached-property-*/* .

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with tests}
# FIXME: python3 tests do not run: it wants %{_bindir}/py.test but python3-pytest provides %{_bindir}/py.test-3.4
tox --sitepackages --skip-missing-interpreters
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
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
%doc AUTHORS.rst HISTORY.rst CONTRIBUTING.rst README.rst LICENSE
%{py_sitescriptdir}/%{module}.py[co]
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS.rst HISTORY.rst CONTRIBUTING.rst README.rst LICENSE
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.*.pyc
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
