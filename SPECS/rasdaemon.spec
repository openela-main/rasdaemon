Name:			rasdaemon
Version:		0.8.0
Release:		8%{?dist}
Summary:		Utility to receive RAS error tracings
Group:			Applications/System
License:		GPLv2
URL:			http://git.infradead.org/users/mchehab/rasdaemon.git
Source0:		http://www.infradead.org/~mchehab/rasdaemon/%{name}-%{version}.tar.bz2

# https://github.com/mchehab/rasdaemon/pull/96
# Add support for CXL poison and AER error events (4 patches)

# rasdaemon: Move definition for BIT and BIT_ULL to a common file
Patch0: d3836aa061f677232f99c514247d3dbf80812a1b.patch

# rasdaemon: Add support for the CXL poison events
Patch1: 75c8fec559641f843345ef8fbc36d124b60b914d.patch

# rasdaemon: Add support for the CXL AER uncorrectable errors
Patch2: a7524917befe7e67c02253cc27cb0c724e5992c0.patch

# rasdaemon: Add support for the CXL AER correctable errors
Patch3: a247baf7110ab6427259eb1421a103e2021a8735.patch

# https://github.com/mchehab/rasdaemon/pull/104
# rasdaemon: Process the generic CXL trace events (7 patches)

# rasdaemon: Add common function to convert timestamp in the CXL event records to the broken-down time format
Patch4: 2ff9bc453998ddb145c7bb8ba30a57c56bd18eab.patch

# rasdaemon: Add common function to get timestamp for the event
Patch5: 7be2edbf863b7acf7e1cab10c2b9f9bf51b3d513.patch

# rasdaemon: Add support for the CXL overflow events
Patch6: f73ed45b91244eb3986ac2574cd7d36ae1d4d22a.patch

# rasdaemon: Add support for the CXL generic events
Patch7: e0cde0edf073b939d345aeba0aed23e238dbc53b.patch

# rasdaemon: Add support for the CXL general media events
Patch8: 53c682fb45c2909c128be4ee8f51a3e42fe2f7fd.patch

# rasdaemon: Add support for the CXL dram events
Patch9: 9a2f6186db2622788f8868d8ec082684d6a06d4d.patch

# rasdaemon: Add support for the CXL memory module events
Patch10: f63b4c942e19a0da1e85a88783ed6e222ad4bdba.patch

# https://github.com/mchehab/rasdaemon/pull/149
# rasdaemon: generic fixes and ras-mc-ctl: add support for CXL error events (10 patches)

# rasdaemon: Fix build warnings unused variable if AMP RAS errors is not enabled
Patch11: 8f79833e3d78424f4a594985fbeb91890f4af81c.patch

# rasdaemon: ras-memory-failure-handler: update memory failure action page types
Patch12: 31c7578ddb0fc15aa7247f2b8885956540031221.patch

# rasdaemon: ras-mc-ctl: Add support for CXL AER uncorrectable trace events
Patch13: f8b6da812eddc063ea739970f941fdd24fb984ae.patch

# rasdaemon: ras-mc-ctl: Add support for CXL AER correctable trace events
Patch14: ae1647624486fca0070b297d0e2fd4e53443c10b.patch

# rasdaemon: ras-mc-ctl: Add support for CXL overflow trace events
Patch15: b22cb067755f4604770f9864a0babed8f93a1553.patch

# rasdaemon: ras-mc-ctl: Add support for CXL poison trace events
Patch16: 93ca96b66c917af37b2ae9295dc5df46a7d64dd2.patch

# rasdaemon: ras-mc-ctl: Add support for CXL generic trace events
Patch17: fd11670d2d35c5d939b03ba1ca80eb81c1f636b6.patch

# rasdaemon: ras-mc-ctl: Add support for CXL general media trace events
Patch18: 572de9d57691be9e630abee9ffa56a2fb155d558.patch

# rasdaemon: ras-mc-ctl: Add support for CXL DRAM trace events
Patch19: c38c14afc5d7bb6c8c52d1023271d755deb23008.patch

# rasdaemon: ras-mc-ctl: Add support for CXL memory module trace events
Patch20: aee13f74266382c64128bd7367a5eeb46277f490.patch

# ras-mc-ctl: add option to exclude old events from reports
Patch21: bd27251e3d52f57be1e245dff1cf221e09c5686f.patch

ExcludeArch:		s390 s390x
BuildRequires:		make
BuildRequires:		gcc
BuildRequires:		autoconf automake libtool
BuildRequires:		gettext-devel
BuildRequires:		perl-generators
BuildRequires:		sqlite-devel
BuildRequires:		systemd
BuildRequires:		libtraceevent-devel
Provides:		bundled(kernel-event-lib)
Requires:		hwdata
Requires:		perl-DBD-SQLite
Requires:		libtraceevent
%ifarch %{ix86} x86_64
Requires:		dmidecode
%endif

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

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
%patch0 -p1
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
autoreconf -vfi

%build
%ifarch %{arm} aarch64
%configure --enable-sqlite3 --enable-aer --enable-non-standard --enable-arm \
	   --enable-mce --enable-extlog --enable-devlink --enable-diskerror \
	   --enable-memory-failure --enable-abrt-report --enable-hisi-ns-decode \
	   --enable-memory-ce-pfa --enable-amp-ns-decode --enable-cpu-fault-isolation \
	   --enable-cxl \
	   --with-sysconfdefdir=%{_sysconfdir}/sysconfig
%else
%configure --enable-sqlite3 --enable-aer \
	   --enable-mce --enable-extlog --enable-devlink --enable-diskerror \
	   --enable-memory-failure --enable-abrt-report --enable-cpu-fault-isolation \
	   --enable-cxl \
	   --with-sysconfdefdir=%{_sysconfdir}/sysconfig
%endif
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -D -p -m 0644 misc/rasdaemon.service %{buildroot}%{_unitdir}/rasdaemon.service
install -D -p -m 0644 misc/ras-mc-ctl.service %{buildroot}%{_unitdir}/ras-mc-ctl.service
install -D -p -m 0655 misc/rasdaemon.env %{buildroot}%{_sysconfdir}/sysconfig/%{name}
rm INSTALL %{buildroot}/usr/include/*.h

%files
%doc AUTHORS ChangeLog COPYING README.md TODO
%{_sbindir}/rasdaemon
%{_sbindir}/ras-mc-ctl
%{_mandir}/*/*
%{_unitdir}/*.service
%{_sysconfdir}/ras/dimm_labels.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Thu Feb 13 2025 Joel Savitz <jsavitz@redhat.com> - 0.8.0-8
- Add option to exclude old events from reports
  Resolves: RHEL-79325

* Tue Jan 14 2025 Joel Savitz <jsavitz@redhat.com> - 0.8.0-7
- Add support for CXL memory failure event logging
  Resolves: RHEL-61233

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 0.8.0-6
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 0.8.0-5
- Bump release for June 2024 mass rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild


* Sat Feb 18 2023 Mauro Carvalho Chehab <mchehab@kernel.org>  0.8.0
- Bump to version 0.8.0 using libtraceevent.

* Sat Jan 21 2023 Mauro Carvalho Chehab <mchehab@kernel.org>  0.7.0
- Bump to version 0.7.0 with several fixes and additions

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 01 2022 Mauro Carvalho Chehab <mchehab@kernel.org>  0.6.8-1
- Fix sysconfdir issues and upgrade to version 0.6.8

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Mauro Carvalho Chehab <mchehab+huawei@kernel.org>  0.6.7-1
- Bump to version 0.6.7 with several fixes and additions

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 10 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.4-1
- Bump to version 0.6.4 with some DB changes for hip08 and some fixes

* Fri Aug 23 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.3-1
- Bump to version 0.6.3 with new ARM events, plus disk I/O and netlink support

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.2-1
- Bump to version 0.6.2 with improvements for PCIe AER parsing and at ras-mc-ctl tool

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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
