Name: javax.inject
Version: 1
Release: 1
Group: Development/Java
Summary: An implementation of the javax.inject API defined in JSR-330
Source0: https://repo1.maven.org/maven2/javax/inject/javax.inject/%{version}/javax.inject-%{version}-sources.jar
Source1: https://repo1.maven.org/maven2/javax/inject/javax.inject/%{version}/javax.inject-%{version}.pom
License: Apache 2.0
BuildRequires: jdk-current
BuildRequires: javapackages-local
BuildArch: noarch

# This used to be in atinject
# http://code.google.com/p/atinject/
# before standardisation. The API is identical,
# so there is no need to keep atinject around.
%rename atinject

%description
This package specifies a means for obtaining objects in such a way
as to maximize reusability, testability and maintainability
compared to traditional approaches such as constructors, factories,
and service locators (e.g., JNDI).

This process, known as dependency injection, is beneficial to most
nontrivial applications.

%package javadoc
Summary: Javadoc documentation for javax.inject
Group: Development/Java

%description javadoc
Javadoc documentation for javax.inject

%prep
%autosetup -p1 -c %{name}-%{version}
# Fix up javadoc snippets
find . -name "*.java" |xargs sed -i -e 's,<tt>,<code>,g;s,</tt>,</code>,g'
# Not exactly nice, but this is only used inside <tt>, so it's ok
find . -name "*.java" |xargs sed -i -e 's,<blockquote [^>]*>,,g;s,</blockquote>,,g'
# And some more errors... Did anyone ever try to build those docs
# before?
find . -name "*.java" |xargs sed -i -e 's,Seat>,Seat\&gt;,g'

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

cat >module-info.java <<'EOF'
module java.inject {
	exports javax.inject;
}
EOF
find . -name "*.java" |xargs javac
find . -name "*.class" -o -name "*.properties" |xargs jar cf javax.inject-%{version}.jar
javadoc -d docs -sourcepath . javax.inject
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir} %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp javax.inject-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap javax.inject-%{version}.pom javax.inject-%{version}.jar
cp -a docs %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%{_javadir}/*.jar

%files javadoc
%{_javadocdir}/%{name}
