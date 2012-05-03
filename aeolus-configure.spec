%global aeolushome /usr/share/aeolus-configure

Summary:  Aeolus Configure Puppet Recipe
Name:     aeolus-configure
Version:  2.5.3
Release:  1%{?dist}

Group:    Applications/Internet
License:  ASL 2.0
URL:      http://aeolusproject.org

Source0:  %{name}-%{version}.tar.gz
BuildArch:  noarch
Requires:   puppet >= 2.6.6
Requires:   rubygem(uuidtools)
BuildRequires: rubygem(rspec-core)
# To send a request to iwhd rest interface to
# create buckets, eventually replace w/ an
# iwhd client
Requires:  curl
Requires:  rubygem(curb)
Requires:  rubygem(highline)

%description
Aeolus Configure Puppet Recipe

%prep
%setup -q

%build

%install
%{__mkdir} -p %{buildroot}/%{_mandir}/man1
%{__mkdir} -p %{buildroot}/%{aeolushome}/modules/aeolus %{buildroot}/%{_sbindir}
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/aeolus-configure/nodes
%{__cp} -R conf/* %{buildroot}%{_sysconfdir}/aeolus-configure/nodes
%{__mv} %{buildroot}%{_sysconfdir}/aeolus-configure/nodes/custom_template.tdl %{buildroot}%{_sysconfdir}/aeolus-configure/
%{__cp} -R recipes/aeolus/* %{buildroot}/%{aeolushome}/modules/aeolus
%{__cp} -R recipes/apache/ %{buildroot}/%{aeolushome}/modules/apache
%{__cp} -R recipes/ntp/ %{buildroot}/%{aeolushome}/modules/ntp
%{__cp} -R recipes/openssl/ %{buildroot}/%{aeolushome}/modules/openssl
%{__cp} -R recipes/postgres/ %{buildroot}/%{aeolushome}/modules/postgres
%{__cp} -R bin/aeolus-node %{buildroot}/%{aeolushome}/modules/aeolus/
%{__cp} -R bin/aeolus-node-check %{buildroot}/%{aeolushome}/modules/aeolus/
%{__cp} -R bin/aeolus-check-services %{buildroot}/%{_bindir}/
%{__cp} -R bin/aeolus-restart-services %{buildroot}/%{_sbindir}/
%{__cp} -R bin/aeolus-configure %{buildroot}/%{_sbindir}/
%{__cp} -R bin/aeolus-cleanup %{buildroot}/%{_sbindir}/
%{__cp} docs/man1/* %{buildroot}/%{_mandir}/man1/

%files
%doc COPYING
%attr(0755, root, root) %{_sbindir}/aeolus-configure
%attr(0755, root, root) %{_sbindir}/aeolus-cleanup
%config(noreplace) %{_sysconfdir}/aeolus-configure/*
%attr(0600, root, root) %{_sysconfdir}/aeolus-configure/nodes/*
%attr(0755, root, root) %{_bindir}/aeolus-check-services
%attr(0755, root, root) %{_sbindir}/aeolus-restart-services
%doc %{_mandir}/man1/*
%{aeolushome}

%changelog
* Thu Apr 12 2012 John Eckersberg <jeckersb@redhat.com> 2.5.3-1
- dbe8dd8 BZ811373 - Add KeepAlive on to vhost in conductor.conf

* Tue Mar 20 2012 Steve Linabery <slinaber@redhat.com> 2.5.2-1
- 3d39608 BZ 803745 - Warn credentials are incorrect if authentication with RHEV fails when checking export type
- 1da2db5 BZ 803249 - Remove qpidd from configure
- fdb718e BZ 802847 - cleanup hardware profiles and fix provider ordering effects

* Fri Mar 16 2012 Steve Linabery <slinaber@redhat.com> 2.5.1-1
- 7312999 BZ #802871: added man pages for configure executables

* Tue Mar 06 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-18
- d2056aa BZ 794505: lower cost hwp for ec2
- c899572 BZ 795935 - put back username and password for conf/vsphere_configure
- 8badc62 BZ 795935 - remove username from rhevm.json

* Fri Mar 02 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-17
- 9c94d5a BZ 798440 - /etc/aeolus-configure/nodes/* should be not be world readable

* Wed Feb 29 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-16
- 10cfd49 BZ #796797: Fix Role string for sql statement
- 529d24c BZ 795935 - Remove passwords from /etc/imagefactory/.json files
- dfa0fcc BZ 788644 - remove confusing comments in cleanup config files

* Wed Feb 22 2012 John Eckersberg <jeckersb@redhat.com> 2.5.0-15
- 7076803 BZ 794755 - Static assets don't set Cache-Control headers
  https://bugzilla.redhat.com/show_bug.cgi?id=794755

* Thu Feb 16 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-14
- de97aa1 BZ 788644 - multiple RHEV providers with aeolus_cleanup

* Mon Feb 13 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-13
- 5c22f94 BZ 788397 - /var/lib/iwhd should not be removed to maintain consistency with mongodb

* Mon Feb  6 2012 John Eckersberg <jeckersb@redhat.com> - 2.5.0-12
- ca36312 BZ #783220 - change default admin email to 'root@localhost' (rev 2)
- 3ac179b BZ 746702 - Update the error message displayed when there is a problem with a config file

* Fri Jan 27 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-11
- db6407f BZ 785217 - check provider add success by inspecting the flash image alt text
- 32fc095 BZ #784833. -d param is positionally dependent
- 9ccb4f0 bz784978 - aeolus-configure is not properly settting the /etc/imagefactory/$provider.json file

* Fri Jan 27 2012 Steve Linabery <slinaber@redhat.com> 2.5.0-10
- Merge branch '1.0-staging' into 1.0-product (slinaber@redhat.com)
- bz784915 - aeolus-configure names vsphere provider "default", change to
  "vsphere-default" (jeckersb@redhat.com)
- BZ 773347 - rename redhat.com to example.org (rwsu@redhat.com)
- BZ 773347 - add a note in rhevm_configure on how to find the data center id
  (rwsu@redhat.com)

* Thu Jan 26 2012 John Eckersberg <jeckersb@redhat.com> 2.5.0-9
- Build with tito

* Wed Jan 25 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-8
- a7c67d3 BZ 783373 - Execute all provider configurations even if there are failures
- 22a1623 shebang comments are not valid JSON, so remove them
- 60ff5ac Update rhevm and vsphere to support multiple configured providers
- a52ac95 Use YAML format for parameterized classes
- fee6871 Pull in create_resources function from puppet 2.7 tree
- ecf8334 BZ 782210 - improved RHEV NFS export validation

* Tue Jan 24 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-7
- 1348210 BZ # 741947. RFE: add support for all ec2 regions

* Fri Jan 20 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-6
- 618b3e0 BZ# 769526 - handle invalid blank cloud provider entries
- aa7c527 BZ #771305 - fixes error found when using custom profiles
- 775dccd Bump release, add changelog 2.5.0-5

* Wed Jan 18 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-5
- c8f5c12 Merge branch '1.0-staging' into 1.0-product
- eebd68a BZ 758644 (part 2) - decrement login counter after aeolus-configure script
- cea160c BZ 758644 (part 1) - clean old cookies when doing a web request
- be20e0c BZ 746702 - improve whitepace checking in /etc/aeolus-configure/nodes configs
- 39de207 Bump release, add changelog, 2.5.0-4

* Wed Jan 11 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-4
- 5cd7786 BZ#773060 - do not add provider accounts for rhevm, vshpere in aeolus-configure
- 6f108fc Bump release, add changelog, 2.5.0-3

* Tue Jan 10 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-3
- e32ce7e BZ 773037 - update RHEVM configuration to support data centers
- caf1355 Set version in Rakefile to 2.5.0
- f1dbbad Set release number
- cc97b46 Fixing merge conflict
- e36cfec Correct versioning in changelog entry
- bcbbde2 Revert version bump
- 4dbabc3 Bump version, reset release
- fdce4e6 Bump release, add changelog

* Mon Jan 09 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-2
- f0043e8 Remove extra_release from spec.in
- c4d94bf Bump release
- 97295c9 Bring in changelog from 2.5.0 release specfile
- 196b80d BZ#766661 - more ec2 provider errors with aeolus-configure
- 6956414 BZ#766697 - running configure -p rhevm without updating rhevm config needs better error msg

* Wed Jan 04 2012 Steve Linabery <slinaber@redhat.com> - 2.5.0-1
- 17b704a Changes to build behavior in rpmtask.rb, Rakefile
- d030803 BZ #766661 - provide mechanism to log aeolus-configure web requests, responses, and errors
- d3ed726 BZ 746702 - Check node config files are in correct format before executing puppet - v3
- 5f58c68 BZ#740089: fix wording in interactive installer (rev2)
- 83993ba BZ 725596 - umount rhev export only if it is not in use
- 3d8c09b BZ 731863 - option to disable select components
- 87b9402 BZ 731863 - add --savedata (-s) option to aeolus-cleanup
- 161eb91 BZ# 768131: Configure should set owner of pg_hba.conf to postgres
- 3b61da5 BZ# 768123: Configure should not write /root/.aeolus-cli
- 990f43d added usage to aeolus-restart-services
- 05360db added usage to aeolus-check-services
- 876df0d BZ #761447: aeolus-configure-image returns (LoadError).
- 384600b Rename mock account from mockuser to mock
- aeeb579 Changed iwhd user.js mode to 600
- 4da2686 iwhd rest.c requires the users.js mode to be 700
- 8c7b96e BZ 758473 - aeolus-configure should check RHEVM export directory has correct type
- fd42729 RM 2879 - Fix adding provider accounts through aeolus-configure
- 78bebcc Remove relp dependency, this should be tracked in aeolus-all metapackage instead.
- 387f161 Bump version for ongoing development on master branch
- da3d340 Bump release and add changelog for 2.4.0 RC

* Thu Dec  1 2011 Steve Linabery <slinaber@redhat.com> - 2.4.0-1
- ffc966c Regenerate conductor secret_token.rb file each time configure is executed
- 4dfb1c3 Bump the version of aeolus-cli to 0.2.0
- d8e6c40 Fix the collision in the /conductor/images/ path
- fc84050 Log the image warehouse cleanup output
- 1337d60 Redmine #2807 - Add ability to flush out iwhd in aeolus-cleaup
- de3c009 Bump version following release of 2.3.0-1 on 2.3.x branch
- fa3f661 BZ753258 - aeolus-configure overwrites contents in /etc/imagefactory/imagefactory.conf every time its executed
- 43ad235 Ensure logout is called after all provider adds in ec2 profile.
- f365b00 BZ752975 - multiple executions of aeolus-cleanup/configure not working as expected
- 2b67daf Fix for Redmine #2680
- 32f555a Document how to specify multiple profiles in aeolus-configure -h.
- 7a0e110 Clean up rsyslog config file
- dc67269 BZ 753273 - rsyslog configuration causes messages log to grow rapidly.
- 0087203 BZ 753250: - aeolus-configure fails No such file or directory
- 0af7031 update aeolus check/restart services scripts for f16 (jlaska's fix for BZ #747762 rebased)

* Thu Nov 17 2011 Steve Linabery <slinaber@redhat.com> - 2.4.0-0
- Bump version following release of 2.3.0-1 from 2.3.x branch

* Wed Sep 14 2011 Richard Su <rwsu@redhat.com> 2.0.2-4
- single deltacloud-core
- rhevm and vsphere configurations moved to their own profiles
- wait 1 sec after deltacloud-core service startup before providers are added

* Tue Aug 30 2011 Maros Zatko <mzatko@redhat.com> 2.0.2-3
- Added script for restarting running services

* Tue Aug 16 2011 Maros Zatko <mzatko@redhat.com> 2.0.2-2
- Added script for listing running services

* Wed Aug 03 2011 Mo Morsi <mmorsi@redhat.com> 2.0.2-1
- update to include profiles, interactive installer

* Wed Jul 20 2011 Mo Morsi <mmorsi@redhat.com> 2.0.1-2
- updates to conform to Fedora package guidelines

* Tue Jul 19 2011 Mike Orazi <morazi@redhat.com> 2.0.1-1
- vSphere configuration
- RHEV configuration
- warehouse sync, solr, and factory connector services removed
- bug fixes

* Wed May 18 2011 Mike Orazi <morazi@redhat.com> 2.0.1-0
- Move using external nodes so changes to behavior can happen in etc

* Wed May 18 2011 Chris Lalancette <clalance@redhat.com> - 2.0.0-11
- Bump the release version

* Tue Mar 22 2011 Angus Thomas <athomas@redhat.com> 2.0.0-5
- Removed iwhd init script and config file

* Wed Feb 17 2011 Mohammed Morsi <mmorsi@redhat.com> 2.0.0-3
- renamed deltacloud-configure to aeolus-configure

* Tue Feb 15 2011 Mohammed Morsi <mmorsi@redhat.com> 2.0.0-3
- various fixes to recipe

* Thu Jan 14 2011 Mohammed Morsi <mmorsi@redhat.com> 2.0.0-2
- include openssl module


* Mon Jan 10 2011 Mike Orazi <morazi@redhat.com> 2.0.0-1
- Make this a drop in replacement for the old deltacloud-configure scripts

* Wed Dec 22 2010 Mohammed Morsi <mmorsi@redhat.com> 0.0.4-1
- Revamp deltacloud recipe to make it more puppetized,
  use general purpose firewall, postgres, ntp modules,
  and to fix many various things

* Wed Sep 29 2010 Mohammed Morsi <mmorsi@redhat.com> 0.0.3-1
- Renamed package from deltacloud appliance
- to deltacloud recipe

* Wed Sep 29 2010 Mohammed Morsi <mmorsi@redhat.com> 0.0.2-3
- Include curl-devel for typhoeus gem

* Wed Sep 29 2010 Mohammed Morsi <mmorsi@redhat.com> 0.0.2-2
- Updated to pull in latest git changes

* Fri Sep 17 2010 Mohammed Morsi <mmorsi@redhat.com> 0.0.2-1
- Updated packages pulled in to latest versions
- Various fixes
- Added initial image warehouse bits

* Thu Sep 02 2010 Mohammed Morsi <mmorsi@redhat.com> 0.0.1-1
- Initial package

