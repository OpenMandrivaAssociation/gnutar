Summary:	A GNU file archiving program
Name:		tar
Version:	1.27
Release:	2
License:	GPLv3
Group:		Archiving/Backup
URL:		http://www.gnu.org/software/tar/tar.html
Source0:	ftp://ftp.gnu.org/gnu/tar/%{name}-%{version}.tar.bz2
Source2:	%{name}-help2man.bz2
Patch0:		tar-1.25-fix-buffer-overflow.patch
Patch1:		tar-1.24-lzma.patch
#BuildRequires:	bison
#BuildRequires:	xz
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
