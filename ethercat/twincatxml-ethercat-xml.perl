#!/usr/bin/perl

use 5.010;
use strict;
use warnings;

use XML::LibXML;

my $num_args = $#ARGV+1;
if ($num_args != 1) {
    print "\nUsage: script.pl <xml file name>\n";
    exit;
}

#my $filename = '/media/barn/Documents/7-Projects/1-Electronics/cnc/Beckhoff/canopen/Term%209%20EL6751%20good%202.xml';
my $filename = $ARGV[0];

my $dom = XML::LibXML->load_xml(location => $filename);

foreach my $InitCmd ($dom->findnodes('TreeItem/EtherCAT/Slave/Mailbox/CoE/InitCmds/InitCmd')) {
#    say 'Index:    ', $InitCmd->findvalue('./Index');
#    say 'Complete: ', $InitCmd->findvalue('./@CompleteAccess');
#    say 'SubIndex: ', $InitCmd->findvalue('./SubIndex');
#    say 'data:     ', $InitCmd->findvalue('./Data');


		say '<sdoConfig idx="',sprintf("%X", $InitCmd->findvalue('./Index')),'" subIdx="', $InitCmd->findvalue('./@CompleteAccess') eq 'true' ? 'complete' : $InitCmd->findvalue('./SubIndex'),'">';
    my $data = $InitCmd->findvalue('./Data');
    $data =~ s/(..)/$1 /g; 
    $data =~ s/\s+$//;
		say '	<sdoDataRaw data="',$data,'"/>';
		say '</sdoConfig>';
}

say '<syncManager idx="0" dir="out"> </syncManager>';
say '<syncManager idx="1" dir="in">	</syncManager>';
say '<syncManager idx="2" dir="out">';
foreach my $pdo ($dom->findnodes('TreeItem/EtherCAT/Slave/ProcessData/RxPdo')) {
    my $pdosm=$pdo->findvalue('./@Sm');
    if  ($pdosm eq 2) {
      my $pdoidx=$pdo->findvalue('./Index');
      $pdoidx =~ s/#x//;
      say '  <pdo idx="', $pdoidx, '">';
      foreach my $pdoentry ($pdo->findnodes('./Entry')) {
        my $pdoentryidx=$pdoentry->findvalue('./Index');
        $pdoentryidx =~ s/#x//;
        my $pdoentrysubidx=$pdoentry->findvalue('./SubIndex');
        my $pdoentrylen=$pdoentry->findvalue('./BitLen');
        my $pdoentryname=$pdoentry->findvalue('./Name');
        $pdoentryname =~ s/\s+/_/g;
        if ($pdoentryidx eq 0) {
          printf "    <pdoEntry idx=\"0000\" subIdx=\"00\" bitLen=\"%02d\"/>\n",$pdoentrylen;
        } else {
          printf "    <pdoEntry idx=\"%04s\" subIdx=\"%02x\" bitLen=\"%02d\" halType=\"s32-todo\"/>\n",$pdoentryidx, $pdoentrysubidx, $pdoentrylen;
        }
      }
      say '  </pdo>';
    }
}
say '</syncManager>';
say '<syncManager idx="3" dir="in">';
foreach my $pdo ($dom->findnodes('TreeItem/EtherCAT/Slave/ProcessData/TxPdo')) {
    my $pdosm=$pdo->findvalue('./@Sm');
    if  ($pdosm eq 3) {
      my $pdoidx=$pdo->findvalue('./Index');
      $pdoidx =~ s/#x//;
      say '  <pdo idx="', $pdoidx, '">';
      foreach my $pdoentry ($pdo->findnodes('./Entry')) {
        my $pdoentryidx=$pdoentry->findvalue('./Index');
        $pdoentryidx =~ s/#x//;
        my $pdoentrysubidx=$pdoentry->findvalue('./SubIndex');
        my $pdoentrylen=$pdoentry->findvalue('./BitLen');
        my $pdoentryname=$pdoentry->findvalue('./Name');
        $pdoentryname =~ s/\s+/_/g;
        if ($pdoentryidx eq 0) {
          printf "    <pdoEntry idx=\"0000\" subIdx=\"00\" bitLen=\"%02d\"/>\n",$pdoentrylen;
        } else {
          printf "    <pdoEntry idx=\"%04s\" subIdx=\"%02x\" bitLen=\"%02d\" halType=\"s32-todo\"/>\n",$pdoentryidx, $pdoentrysubidx, $pdoentrylen;
        }
      }
      say '  </pdo>';
    }
}
say '</syncManager>';


my $dc = $dom->findnodes('TreeItem/EtherCAT/Slave/DC');
  say '<!..><dcConf assignActivate="700" sync0Cycle="*1" sync0Shift="-250000"/> <-->';

say '<watchdog divider="2498" intervals="5000"/>';
