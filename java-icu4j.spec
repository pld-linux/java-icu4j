#
# Conditional build:
%bcond_with	eclipse		# build eclipse

%if %{with eclipse}
%define	debug_package %{nil}
%endif

%define		srcname icu4j
Summary:	International Components for Unicode for Java
Name:		java-%{srcname}
Version:	52.1
Release:	1
License:	MIT and EPL
Group:		Libraries/Java
URL:		http://site.icu-project.org/
# CAUTION
# to create a tarball use following procedure
# svn co http://source.icu-project.org/repos/icu/icu4j/tags/release-52-eclipse-20140218 icu4j-<version>
# tar caf icu4j-<version>.tar.xz icu4j-<version>/
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/icu4j/icu4j-%{version}.tar.xz/e52729889dafc60a25b2a8d3a82725be/icu4j-%{version}.tar.xz
# Source0-md5:	e52729889dafc60a25b2a8d3a82725be
Patch0:		crosslink.patch
BuildRequires:	ant >= 1.7.0
BuildRequires:	jdk >= 1.7
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zip
%if %{with eclipse}
BuildRequires:	eclipse-pde >= 3.2.1
%endif
Requires:	jpackage-utils
Requires:	jre >= 1.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Note:  this next section looks weird having an arch specified in a
# noarch specfile but the parts of the build
# All arches line up between Eclipse and Linux kernel names except i386 -> x86
%ifarch %{ix86}
%define	eclipse_arch	x86
%else
%define	eclipse_arch	%{_arch}
%endif

%description
The International Components for Unicode (ICU) library provides robust
and full-featured Unicode services on a wide variety of platforms. ICU
supports the most current version of the Unicode standard, and
provides support for supplementary characters (needed for GB 18030
repertoire support).

Java provides a very strong foundation for global programs, and IBM
and the ICU team played a key role in providing globalization
technology into Sun's Java. But because of its long release schedule,
Java cannot always keep up-to-date with evolving standards. The ICU
team continues to extend Java's Unicode and internationalization
support, focusing on improving performance, keeping current with the
Unicode standard, and providing richer APIs, while remaining as
compatible as possible with the original Java text and
internationalization API design.

%package charset
Summary:	Charset sublibrary of %{srcname}
Group:		Libraries/Java
Requires:	jpackage-utils

%description charset
Charset sublibrary of %{srcname}.

%package javadoc
Summary:	Javadoc for %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{srcname}.

%package eclipse
Summary:	Eclipse plugin for %{srcname}
Group:		Development/Libraries
Requires:	jpackage-utils

%description eclipse
Eclipse plugin support for %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}

%{__sed} -i 's/\r//' APIChangeReport.html
%{__sed} -i 's/\r//' readme.html

sed -i -e "s/ .*bootclasspath=.*//g" build.xml
sed -i -e "s/<date datetime=.*when=\"after\"\/>//" build.xml
sed -i -e "/javac1.3/d" build.xml
sed -i -e "s:/usr/lib:%{_datadir}:g" build.xml

%build
%ant jar docs \
	-Dicu4j.javac.source=1.5 \
	-Dicu4j.javac.target=1.5 \
	-Dj2se.apidoc=%{_javadocdir}/java

%if %{with eclipse}
ECLIPSE_BASE=`more %{_bindir}/eclipse-pdebuild  | grep datadir= | sed -e "s/datadir=//"`/eclipse
cd eclipse-build
%ant \
	-Dj2se.apidoc=%{_javadocdir}/java \
	-Declipse.home=${ECLIPSE_BASE} \
	-Djava.rt=%{_jvmdir}/jre/lib/rt.jar \
	-Declipse.basews=gtk -Declipse.baseos=linux \
	-Declipse.pde.dir=${ECLIPSE_BASE}/dropins/sdk/plugins/`ls ${ECLIPSE_BASE}/dropins/sdk/plugins/|grep org.eclipse.pde.build_`
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -ap %{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar
cp -ap %{srcname}-charset.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-charset.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}
cp -pr doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}

%if %{with eclipse}
install -d $RPM_BUILD_ROOT%{_javadir}/icu4j-eclipse
unzip -qq -d $RPM_BUILD_ROOT%{_javadir}/icu4j-eclipse \
	eclipse-build/out/projects/ICU4J.com.ibm.icu/com.ibm.icu-com.ibm.icu.zip
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.html APIChangeReport.html
%{_javadir}/%{srcname}.jar

%files charset
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-charset.jar

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/*

%if %{with eclipse}
%files eclipse
%defattr(644,root,root,755)
%doc readme.html
%dir %{_javadir}/icu4j-eclipse/
%dir %{_javadir}/icu4j-eclipse/features
%dir %{_javadir}/icu4j-eclipse/plugins
%{_javadir}/icu4j-eclipse/features/*
%{_javadir}/icu4j-eclipse/plugins/*
%endif
