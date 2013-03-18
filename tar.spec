Summary:	A GNU file archiving program
Name:		tar
Version:	1.26
Release:	8
License:	GPLv3
Group:		Archiving/Backup
URL:		http://www.gnu.org/software/tar/tar.html
Source0:	ftp://ftp.gnu.org/gnu/tar/%{name}-%{version}.tar.bz2
Source2:	%{name}-help2man.bz2
Patch0:		tar-1.25-fix-buffer-overflow.patch
Patch1:		tar-1.24-lzma.patch
Patch2:		tar-1.26-glibc-2.16.patch
Patch3:		tar-aarch64.patch
BuildRequires:	bison
BuildRequires:	xz
Suggests:	/usr/bin/rsh
Conflicts:	rmt < 0.4b36

%description
The GNU tar program saves many files together into one archive and
can restore individual files (or all of the files) from the archive.
Tar can also be used to add supplemental files to an archive and to
update or list files in the archive.

Tar includes multivolume support, automatic archive compression/
decompression, the ability to perform remote archives and the
ability to perform incremental and full backups.

If you want to use Tar for remote backups, you'll also need to
install the rmt package.

You should install the tar package, because you'll find its
compression and decompression utilities essential for working
with files.

%prep

%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1

bzcat %{SOURCE2} > ./help2man
chmod +x ./help2man

xz -e ChangeLog

sed -i 's/.*sigpipe.at.*//' tests/testsuite.at

%build
RSH=/usr/bin/rsh \
%configure2_5x \
	--enable-backup-scripts \
	--bindir=/bin \
	--disable-rpath

%make

# thanks to diffutils Makefile rule
(echo '[NAME]' && sed 's@/\* *@@; s/-/\\-/; q' src/tar.c) | (./help2man -i - -S '%{name} %{version}' src/tar ) | sed 's/^\.B info .*/.B info %{name}/' > %{name}.1

%check
# Disabled due to buildsystem weirdness: tests are always fine if you
# do it with iurt on the cluster, but often fail when run through bs,
# randomly - AdamW 2008/04
# (misc, 02-11-2010, sigpipe test do not pass on iurt )
make check

%install
%makeinstall_std

ln -sf tar %{buildroot}/bin/gtar

install -D -m 644 tar.1 %{buildroot}%{_mandir}/man1/tar.1

# conflicts with coda-debug-backup
mv %{buildroot}%{_sbindir}/backup %{buildroot}%{_sbindir}/tar-backup
mv %{buildroot}%{_sbindir}/restore %{buildroot}%{_sbindir}/tar-restore

# rmt is provided by rmt ...
%define rmtrealname rmt-tar
mkdir -p %{buildroot}/sbin
mv %{buildroot}%{_libdir}/rmt %{buildroot}/sbin/%rmtrealname

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog.xz NEWS README THANKS TODO
/bin/*
%{_libexecdir}/backup.sh
%{_libexecdir}/dump-remind
%{_sbindir}/*
/sbin/%rmtrealname
%{_infodir}/*.info*
%{_mandir}/man?/*


%changelog
* Sat Mar 12 2011 Funda Wang <fwang@mandriva.org> 1.26-1mdv2011.0
+ Revision: 644080
- new version 1.26

* Sat Nov 27 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.25-1mdv2011.0
+ Revision: 601819
- update to 1-25
- remove patches applied upstream
- rediff patch (fix buffer overflow)

* Tue Nov 02 2010 Michael Scherer <misc@mandriva.org> 1.24-4mdv2011.0
+ Revision: 592108
- disable a test that do not work ( sigpipe, no time to look )
- fix for the device creation problem that broke iurt and the cluster
- re-enable tests
- reenable the tests suite, so unforeseen breakage do not pass

* Wed Oct 27 2010 Anssi Hannula <anssi@mandriva.org> 1.24-3mdv2011.0
+ Revision: 589646
- fix regression with -C and extracting directories (patch from upstream)

* Tue Oct 26 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.24-2mdv2011.0
+ Revision: 589451
- remove p0, merged upstream.
- new version 1.24
- rediff mdv lzma patch
- add a patch from gentoo to fix #61419 (thanks oden)
- bump release, for override last commit
- rever last commit.

* Mon Oct 25 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.24-1mdv2011.0
+ Revision: 589298
- remove p0, p1: merged upstream.
- new version 1.24

* Mon Jul 19 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.23-4mdv2011.0
+ Revision: 554994
- P1: fix mdvbug #60251

* Mon Mar 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1.23-3mdv2010.1
+ Revision: 526624
- rebuilt due to lack of space on n5 in the bs
- added br on rsh due to a long standing missing dep

* Wed Mar 10 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.23-1mdv2010.1
+ Revision: 517607
- rediff patch
- update to 1.23

* Fri Sep 25 2009 Thomas Backlund <tmb@mandriva.org> 1.22-2mdv2010.0
+ Revision: 448752
- We have had the -Y flag for lzma since atleast 2008.0
  Add back the flag so we dont break userspace on upgrades
  (added with note that it's depreceated)

* Thu Sep 24 2009 Olivier Blin <oblin@mandriva.com> 1.22-1mdv2010.0
+ Revision: 448165
- explicitely buildrequire xz (from Arnaud Patard)
- remove xz patch (merged upstream in 1.22)

  + Thierry Vignaud <tv@mandriva.org>
    - use upstream bz2 tarball
    - fix URL

  + Funda Wang <fwang@mandriva.org>
    - New version 1.22

* Thu Feb 26 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.21-2mdv2009.1
+ Revision: 345103
- since package is of GPLv3 license which comes with common-licenses package,
  we'll just drop shipping COPYING with the package
- might as well compress the changelog with xz in stead of bzip2 to save a few
  more kilobytes.. :p
- add xz support using -J switch which upstream seems plan on using, but
  prematurely introduced to support older revision of new format judging by
  magic used.. (replaces old lzma patch, P0)

* Sun Dec 28 2008 Oden Eriksson <oeriksson@mandriva.com> 1.21-1mdv2009.1
+ Revision: 320310
- 1.21
- fix the lzma patch; note that upstrean chose -J but mandriva use -Y,
  mandriva should adjust accordingly..., and then nuke the lzma patch

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.20-8mdv2009.1
+ Revision: 317662
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.20-7mdv2009.0
+ Revision: 265746
- rebuild early 2009.0 package (before pixel changes)

* Wed Apr 23 2008 Adam Williamson <awilliamson@mandriva.org> 1.20-6mdv2009.0
+ Revision: 196832
- disable tests as they randomly fail when building on the bs
- revert to the previous LZMA patch (rediffed) as the code merged upstream doesn't work right

* Thu Apr 17 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.20-2mdv2009.0
+ Revision: 195385
- add missing buildrequire on bison
- new version
- fix license
- drop patches 13 and 14, both were merged upstream

* Thu Feb 07 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.19-2mdv2008.1
+ Revision: 163377
- Fix compression of tar.bz2 files returning error code 2 (ubuntu)(Bug #35291 #37194)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - restore previous version

* Tue Oct 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.19-1mdv2008.1
+ Revision: 98756
- new version
- drop patch 15 (merged upstream)
- nuke rpath
- spec file clean

* Mon Sep 10 2007 Thierry Vignaud <tv@mandriva.org> 1.18-2mdv2008.0
+ Revision: 84081
- patch 15: security fix for CVE-2007-4131
- drop patch 11 which prevents patch 15 from working properly and isn't proper
  to begin with

* Sat Jun 30 2007 Funda Wang <fwang@mandriva.org> 1.18-1mdv2008.0
+ Revision: 46067
- New version


* Mon Feb 12 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.16-3mdv2007.1
+ Revision: 118886
- update to use 'lzma' over deprecated 'lzmash' wrapper script

* Wed Nov 29 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.16-2mdv2007.1
+ Revision: 88709
- bump release
- patch 14: security fix for MDKSA-2006:219 (#27379)

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.16-1mdv2007.1
+ Revision: 86832
- Import tar

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.16-1mdv2007.1
- new release

* Fri Jun 30 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.15.91-1mdv2007.0
- 1.15.91
- fix make-check-outside-check-section
- regenerate P13
- update url

* Sat May 13 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.15.90-2mdk
- patch 13: fix segfault (#22434)

* Fri May 12 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.15.90-1mdk
- new release
- kill patches 1, 7, 12 (uneeded)
- rediff patch 13

* Wed Feb 22 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.15.1-8mdk
- patch 14: security fix for CVE-2006-0300
- use %%mkrel

* Sun Jan 08 2006 Giuseppe Ghibò <ghibo@mandriva.cm> 1.15.1-7mdk
- Added supporto for lzmash compression (tar -Y).

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.15.1-6mdk
- Rebuild

* Thu Aug 25 2005 Pixel <pixel@mandriva.com> 1.15.1-5mdk
- get rid of ChangeLog.1 (ie prior to 1997)
- compress ChangeLog

* Wed Jul 20 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.15.1-4mdk
- Remove alternative install for rmt, use /sbin/rmt from dump

* Tue Jul 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.15.1-3mdk
- Fix postun alternative install for rmt
- Fix compilation with gcc 4 (patch 12)

* Tue Feb 22 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.15.1-2mdk
- fix packages ordering at install time (#13792)

* Wed Dec 22 2004 Abel Cheung <deaddog@mandrakesoft.com> 1.15.1-1mdk
- New release 1.15.1

* Wed Dec 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.15-1mdk
- 1.15
- regenerate P7

* Tue May 25 2004 Abel Cheung <deaddog@deaddog.org> 1.14-1mdk
- New version
- Drop P105 (-y/-I), since -j/--bzip2 is stabilized and well known now
- Drop P0, use help2man to generate manpage instead of bundling 4-yr-old one
- Drop P8, P10 (upstream)
- Rediff P1, P7, P11
- Install scripts as well
- Use alternative for rmt

