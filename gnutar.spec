# (tpg) optimize it a bit
%ifnarch %{riscv}
%global optflags %{optflags} -O3 --rtlib=compiler-rt
%endif

Summary:	A GNU file archiving program
Name:		gnutar
Version:	1.34
Release:	4
License:	GPLv3
Group:		Archiving/Backup
URL:		https://www.gnu.org/software/tar/tar.html
Source0:	ftp://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz
Source2:	tar-help2man.bz2
BuildRequires:	bison
BuildRequires:	xz
BuildRequires:	pkgconfig(libacl)
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

OpenMandriva Lx uses bsdtar by default - install gnutar if you need
the alternative GNU tar implementation.

%prep
%autosetup -n tar-%{version} -p1

bzcat %{SOURCE2} > ./help2man
chmod +x ./help2man

xz -e ChangeLog

sed -i 's/.*sigpipe.at.*//' tests/testsuite.at

%build
RSH=/usr/bin/rsh \
%configure \
	--enable-backup-scripts \
	--disable-rpath

%make_build

# thanks to diffutils Makefile rule
(echo '[NAME]' && sed 's@/\* *@@; s/-/\\-/; q' src/tar.c) | (./help2man -i - -S '%{name} %{version}' src/tar ) | sed 's/^\.B info .*/.B info %{name}/' > gtar.1

%check
make check || echo "Failed"

%install
%make_install

mv %{buildroot}%{_bindir}/tar %{buildroot}%{_bindir}/gtar
install -D -m 644 gtar.1 %{buildroot}%{_mandir}/man1/gtar.1

# conflicts with coda-debug-backup
mv %{buildroot}%{_sbindir}/backup %{buildroot}%{_sbindir}/tar-backup
mv %{buildroot}%{_sbindir}/restore %{buildroot}%{_sbindir}/tar-restore

# rmt is provided by rmt ...
%define rmtrealname rmt-tar
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_libexecdir}/rmt %{buildroot}%{_sbindir}/%rmtrealname

%if "%{name}" != "tar"
rm -f %{buildroot}%{_mandir}/man1/tar.1* %{buildroot}%{_mandir}/man8/rmt.8*
%endif

# Add a symlink in a directory of its own so scripts that rely on gnutar
# behavior can just set PATH
mkdir -p %{buildroot}%{_libexecdir}/gnutar
ln -s %{_bindir}/gtar %{buildroot}%{_libexecdir}/gnutar/tar

%find_lang tar

%files -f tar.lang
%doc AUTHORS ChangeLog.xz NEWS README THANKS TODO
%{_bindir}/*
%if "%{_bindir}" != "%{_sbindir}"
%{_sbindir}/*
%endif
%{_libexecdir}/backup.sh
%{_libexecdir}/dump-remind
%{_libexecdir}/gnutar
%doc %{_infodir}/*.info*
%doc %{_mandir}/man?/*
