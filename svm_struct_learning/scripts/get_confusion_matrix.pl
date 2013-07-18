#$outFile=`cat fold$i/lastout.txt`;
$outFile = "out.model.c0.1.e0.01.w3";
$actlabelmapfile ="../classmap.txt";
$afflabelmapfile ="../affmap.txt";
$dir = shift;
$numfold=4;

%actlabels= ();
$count  =0;
open(F,$actlabelmapfile);
while(<F>)
{
  chomp();
  $count++;
  $actlabels{$count} = $_; 
}
close (F);
$numActClasses = keys(%actlabels);

%afflabels= ();
$count  =0;
open(F,$afflabelmapfile);
while(<F>)
{
  chomp();
  $count++;
  $afflabels{$count} = $_; 
}
close (F);
$numAffClasses = keys(%afflabels);
{
$c = 1;  
# read all info
  %mat = ();  
  %m = ();
  for ( $i = 1; $i<= $numfold; $i++) 
  {

	print "outputfile=./$dir/fold$i/pred/$outFile\n";
    $ls = `ls -l ./$dir/fold$i/pred/$outFile`;
    print "$ls\n";
    $linenum1 = `grep -n "Object" ./$dir/fold$i/pred/$outFile | cut -f1 -d':'`;
    chomp($linenum1);
    $linenum2 = `grep -n "Activity" ./$dir/fold$i/pred/$outFile | cut -f1 -d':'`;
    chomp($linenum2);
    $totalnum = `wc -l ./$dir/fold$i/pred/$outFile | cut -f1 -d' ' `;
    chomp($totalnum);
    print "total num = $totalnum\n";
    $cmd = "sed -n \'$linenum1,$linenum2 p\' ./$dir/fold$i/pred/$outFile > objfile"  ;
    system($cmd);
    $cmd = "sed -n \'$linenum2,$totalnum p\' ./$dir/fold$i/pred/$outFile > actfile"  ;
    system($cmd);
    $flag = 0; 
    $count = 0;
    #open(F,"actfile")   ;
    #$numClasses = $numActClasses;
    open(F,"objfile")   ;
    $numClasses = $numAffClasses;
    while(<F>){
      chomp ;
      $line = $_;
      if($line =~ m/confusion matrix:/){
#       print "\n$line\n";
       $flag = 1;
       $count = 1;
       next;
      }
      if($flag ==1 && $count <=$numClasses )
      {
        $line =~ s/([ \[]*)([^\]]*)(\]*)/\2/;
 #       print $line."\n";
        @{$mat{$c}{$i}{$count}} = split/\s+/,$line;
  #      print join(",",@{$mat{$c}{$i}{$count}})."\n";
        $count++;
      }
    }
  }

  for($i =1 ; $i<= $numfold; $i++)
  {
     for ( $k = 1; $k<= $numClasses; $k++) 
     {
       for ( $l = 0; $l< $numClasses; $l++) 
       { 
     #    print "$i\t$k\t$l\t$mat{$c}{$i}{$k}[$l]\t$m{$c}{$k}{$l+1}\n";
         $m{$c}{$k}{$l+1} += $mat{$c}{$i}{$k}[$l];
       }
     }
  }
   

}



 $c =1;
{
  #open(F,">confusionM.subact.csv");
  open(F,">confusionM.affordance.csv");
  @ll = ();
  print $c."\n\n";
  printf "%-16s", $blank;
  for ( $k = 1; $k<= $numClasses; $k++) {
    printf "%-5d\t",  $k ; 
    #push(@ll,$actlabels{$k});
    push(@ll,$afflabels{$k});
  }
  print F join(",",@ll)."\n";

  print "\n\n";
  for ( $k = 1; $k<= $numClasses; $k++)
  {
    @r = ();
    printf "%d:%-12s",  $k,$labels{$k} ; 
    for ( $l = 1; $l<= $numClasses; $l++) 
    {
      printf "\t%-5s",$m{$c}{$k}{$l};
      push(@r,$m{$c}{$k}{$l})
    }
    print F join(",",@r)."\n";
    print "\n";
  }
  close(F);
}


