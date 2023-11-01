Name:			rasdaemon
Version:		0.6.1
Release:		13%{?dist}
Summary:		Utility to receive RAS error tracings
Group:			Applications/System
License:		GPLv2
URL:			http://git.infradead.org/users/mchehab/rasdaemon.git
Source0:		http://www.infradead.org/~mchehab/rasdaemon/%{name}-%{version}.tar.bz2

ExcludeArch:		s390 s390x
BuildRequires:		gettext-devel
BuildRequires:		perl-generators
BuildRequires:		sqlite-devel
BuildRequires:		systemd
BuildRequires:		libtool
Provides:		bundled(kernel-event-lib)
Requires:		hwdata
Requires:		perl-DBD-SQLite
%ifarch %{ix86} x86_64
Requires:		dmidecode
%endif

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

Patch1: 60a91e4da4f2daf2b10143fc148a8043312b61e5.patch
Patch2: a16ca0711001957ee98f2c124abce0fa1f801529.patch
Patch3: add_upstream_labels.patch
Patch4: b22be68453b2497e86cbd273b9cd56fadc5859e3.patch
Patch5: 2a1d217660351c08eb2f8bccebf939abba2f7e69.patch
Patch6: 8704a85d8dc3483423ec2934fee8132f85f8fdb6.patch
Patch7: cc2ce5c65ed5a42eaa97aa3659854add6d808da5.patch
Patch8: 854364ba44aee9bc5646f6537fc744b0b54aff37.patch
Patch9: 9acef39f13833f7d53ef96abc5a72e79384260f4.patch
Patch10: 28ea956acc2dab7c18b4701f9657afb9ab3ddc79.patch
Patch11: aecf33aa70331670c06db6b652712b476e24051c.patch
Patch12: 7937f0d6c2aaaed096f3a3d306416743c0dcb7a4.patch
Patch13: rasdaemon-ras-mc-ctl-Fix-script-to-parse-dimm-sizes.patch
Patch14: 0862a096c3a1d0f993703ab3299f1ddfadf53d7f.patch
Patch15: 546cf713f667437fb6e283cc3dc090679eb47d08.patch
Patch16: 2290d65b97311dd5736838f1e285355f7f357046.patch
Patch17: 16d929b024c31d54a7f8a72eab094376c7be27f5.patch
Patch18: b497a3d6a39d402c41065e9284d49114b97e3bfe.patch
Patch19: ce6e7864f11f709c4f803828fbc8e507d115d03b.patch
Patch20: a8c776ed94f68ae31d7b5f74e19545698898c13c.patch
Patch21: 899fcc2cf21c86b5462c8f4441cd9c92b3d75f7d.patch
Patch22: e8b97ec14a11764fedfea50bd4d96ddda43c7fc1.patch
Patch23: ce33041e0abfa20054ff5d6874ffbd1ab592558d.patch

%description
%{name} is a RAS (Reliability, Availability and Serviceability) logging tool.
It currently records memory errors, using the EDAC tracing events.
EDAC is drivers in the Linux kernel that handle detection of ECC errors
from memory controllers for most chipsets on i386 and x86_64 architectures.
EDAC drivers for other architectures like arm also exists.
This userspace component consists of an init script which makes sure
EDAC drivers and DIMM labels are loaded at system startup, as well as
an utility for reporting current error counts from the EDAC sysfs files.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

# The tarball is locked in time the first time aclocal was ran and will keep
# requiring an older version of automake
autoreconf -vfi

%build
%ifarch %{arm} aarch64
%configure --enable-aer --enable-sqlite3 --enable-abrt-report --enable-non-standard --enable-hisi-ns-decode --enable-arm
%else
%configure --enable-mce --enable-aer --enable-sqlite3 --enable-extlog --enable-abrt-report --enable-memory-failure
%endif
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -D -p -m 0644 misc/rasdaemon.service %{buildroot}/%{_unitdir}/rasdaemon.service
install -D -p -m 0644 misc/ras-mc-ctl.service %{buildroot}%{_unitdir}/ras-mc-ctl.service
install -D -p -m 0655 labels/* %{buildroot}%{_sysconfdir}/ras/dimm_labels.d
rm INSTALL %{buildroot}/usr/include/*.h

%files
%doc AUTHORS ChangeLog COPYING README TODO
%{_sbindir}/rasdaemon
%{_sbindir}/ras-mc-ctl
%{_mandir}/*/*
%{_unitdir}/*.service
%{_sharedstatedir}/rasdaemon
%{_sysconfdir}/ras/dimm_labels.d

%changelog
* Mon Jan 23 2023 Aristeu Rozanski <aris@redhat.com> 0.6.1-13
- Fixing covscan issues [2073516]

* Tue Oct 12 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-12
- Adding missing bits from b497a3d6a39d402c41065e9284d49114b97e3bfe [1923254]

* Tue Oct 12 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-11
- Removed bits from devlink and diskerrors that aren't used yet [1923254]

* Tue Oct 12 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-10
- Add miscellaneous patches required by customer [1923254]

* Wed Oct 06 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-9
- Prevent ras-mc-ctl trying to access extlog and mce tables if rasdaemon was built without support for them [2011404]

* Thu Aug 26 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-8
- Disable MCE and extlog in arm packages [2009499]

* Thu Aug 26 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-7
- Add support for AMD SMCA banks for family 19 [1991955]

* Wed May 26 2021 Aristeu Rozanski <aris@redhat.com> 0.6.1-6
- Add support for AMD SMCA [1965011]

* Wed Apr 08 2020 Aristeu Rozanski <aris@redhat.com> 0.6.1-5
- Fix high CPU usage when CPUs are offline [1683420]

* Wed Apr 08 2020 Aristeu Rozanski <aris@redhat.com> 0.6.1-4
- Include upstream labels [1665418]

* Thu Jul 11 2019 Aristeu Rozanski <aris@redhat.com> 0.6.1-3
- Add support for AMD scalable MCA [1725488]

* Mon Aug 20 2018 Aristeu Rozanski <aris@redhat.com> 0.6.1-2
- Add support for error count display [1573685]

* Wed Apr 25 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.1-1
- Bump to version 0.6.1 adding support for Skylake Xeon MSCOD, a bug fix and some new DELL labels

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 14 2017 Mauro Carvalho Chehab <mchehab@osg.samsung.com>  0.6.0-1
- Bump to version 0.6.0 adding support for Arm and Hisilicon events and update Dell Skylate labels

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.8-3
- Add a virtual provide, per BZ#104132

* Fri Apr 15 2016 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.8-2
- Bump to version 0.5.8 with support for Broadwell EP/EX MSCOD/DE MSCOD

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 03 2015 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.6-1
- Bump to version 0.5.6 with support for LMCE and some fixes

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.5-1
- Bump to version 0.5.5 with support for newer Intel platforms & some fixes

* Tue Sep 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.4-3
- aarch64/ppc64 have edac capabilities
- spec cleanups
- No need to run autoreconf

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.4-1
- Bump to version 0.5.4 with some fixes, mainly for amd64

* Sun Aug 10 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.3-1
- Bump to version 0.5.3 and enable ABRT and ExtLog

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.2-1
- fix and enable ABRT report support

* Fri Mar 28 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.1-1
- Do some fixes at the service files and add some documentation for --record

* Sun Feb 16 2014  Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.0-1
- Add experimental ABRT support

* Tue Sep 10 2013 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.4.2-1
- Fix ras-mc-ctl layout filling
 
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.4.1-4
- Perl 5.18 rebuild

* Sun Jun  2 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.1-3
- ARM has EDMA drivers (currently supported in Calxeda highbank)

* Wed May 29 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.4.1-2
- Fix the name of perl-DBD-SQLite package
 
* Wed May 29 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.4.1-1
- Updated to version 0.4.1 with contains some bug fixes

* Tue May 28 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.4.0-1
- Updated to version 0.4.0 and added support for mce, aer and sqlite3 storage

* Mon May 20 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.3.0-1
- Package created
