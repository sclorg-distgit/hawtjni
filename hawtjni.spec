%{?scl:%scl_package hawtjni}
%{!?scl:%global pkg_name %{name}}

Name:             %{?scl_prefix}hawtjni
Version:          1.6
Release:          17%{?dist}
Summary:          Code generator that produces the JNI code
License:          ASL 2.0 and EPL and BSD
URL:              http://hawtjni.fusesource.org/
BuildArch:        noarch

# git clone git://github.com/fusesource/hawtjni.git
# cd hawtjni && git archive --format=tar --prefix=hawtjni-1.6/ hawtjni-project-1.6 | xz > hawtjni-1.6.tar.xz
Source0:          %{pkg_name}-%{version}.tar.xz
Patch0:           0001-Fix-shading-and-remove-unneeded-modules.patch
Patch1:           0002-Fix-xbean-compatibility.patch
Patch2:           0003-Remove-plexus-maven-plugin-dependency.patch
Patch3:           0004-Remove-eclipse-plugin.patch
# From upstream commit d9cd0ab
Patch4:           0005-Should-fix-issue-7.-We-now-do-a-write-barrier-before.patch
# From upstream commit 92c2661
Patch5:           0006-Simplify-shared-lib-extraction.patch
Patch6:           maven_hawtjni_plugin_configure.ac_fix.patch

BuildRequires:    maven30-maven-local
BuildRequires:    maven30-maven-plugin-plugin
BuildRequires:    maven30-maven-surefire-report-plugin
BuildRequires:    maven30-maven-project-info-reports-plugin
BuildRequires:    maven30-maven-plugin-jxr
BuildRequires:    maven30-plexus-containers-component-metadata
BuildRequires:    maven30-log4j
BuildRequires:    maven30-fusesource-pom
BuildRequires:    maven30-felix-parent
BuildRequires:    maven30-xbean
BuildRequires:    %{?scl_prefix}apache-commons-cli
BuildRequires:    %{?scl_prefix}mvn(asm:asm)
BuildRequires:    %{?scl_prefix}mvn(asm:asm-commons)

# Use manual requires since we would get a dep on
# SCL-ized xbean, which is only required by hawtjni-generators.
# However thermostat only uses hawtjni-runtime.
Requires:         %{?scl_prefix}mvn(asm:asm)
Requires:         %{?scl_prefix}mvn(asm:asm-commons)
Requires:         %{?scl_prefix}mvn(commons-cli:commons-cli)  
# jansi-native wants this provide
Provides:         %{?scl_prefix}mvn(org.fusesource.hawtjni:hawtjni-runtime) = %{version}
Requires:         java >= 1.5

%{?scl:Requires: %scl_runtime}

%description
HawtJNI is a code generator that produces the JNI code needed to
implement java native methods. It is based on the jnigen code generator
that is part of the SWT Tools project which is used to generate all the
JNI code which powers the eclipse platform.

%package javadoc
Summary:          Javadocs for %{name}
%{?scl:Requires: %scl_runtime}

%description javadoc
This package contains the API documentation for %{name}.

%package -n %{?scl_prefix}maven-%{pkg_name}-plugin
Summary:          Use HawtJNI from a maven plugin
%{?scl:Requires: %scl_runtime}

%description -n %{?scl_prefix}maven-%{pkg_name}-plugin
This package allows to use HawtJNI from a maven plugin.

%prep
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p2
%mvn_file ":{*}" @1
%mvn_package ":*{plugin}" @1
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc readme.md license.txt changelog.md

%files javadoc -f .mfiles-javadoc
%doc license.txt

%files -n %{?scl_prefix}maven-%{pkg_name}-plugin -f .mfiles-plugin
%doc license.txt

%changelog
* Wed Jun 25 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-17
- Add scl-runtime dependency to the hawtjni maven plugin
  package.

* Tue Jun 17 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-16
- Build against maven30 collection.

* Wed Nov 27 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-15
- Properly enable SCL.

* Wed Nov 20 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-14
- Add version to manual provides.

* Wed Nov 20 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-13
- Don't use auto-requires in order to avoid xbean
  runtime dependency.

* Mon Nov 18 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-12
- Fix configure.ac template in maven-hawtjni-plugin.

* Mon Nov 18 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-11
- Use SCL prefix for the maven plugin.

* Mon Nov 18 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.6-10
- Add macro for java auto-requires/provides.
- Use appropriate SCL-ized packages as BRs.

* Fri Nov 08 2013 Severin Gehwolf <sgehwolf@redhat.com> - 1.6-9
- SCL-ize package.

* Wed Sep 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-8
- Add missing barriers in cache initialization
- Simplify shared lib extraction, resolves: CVE-2013-2035

* Tue Aug 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-7
- Migrate away from mvn-rpmbuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-5
- Remove unneeded BR: maven-idea-plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.6-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-2
- Replace asm2 requires with objectweb-asm
- Resolves: rhbz#902674

* Fri Sep 07 2012 gil cattaneo <puntogil@libero.it> 1.6-1
- Upstream release 1.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-3
- Remove eclipse plugin from BuildRequires

* Thu Jan 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.5-2
- Replace plexus-maven-plugin with plexus-containers implementation

* Sun Jan 15 2012 Marek Goldmann <mgoldman@redhat.com> 1.5-1
- Upstream release 1.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Marek Goldmann <mgoldman@redhat.com> 1.3-1
- Upstream release 1.3

* Fri Jul 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.2-1
- Upstream release 1.2
- Moved to new depmap macro

* Mon May 30 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-4
- Removed maven-shade-plugin dependency

* Mon May 30 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-3
- Split maven-hawtjni-plugin into new package
- Fixed license
- Fixed summary
- Using xz to compress source code

* Sun May 29 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-2
- Added maven-hawtjni-plugin

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-1
- Initial packaging
