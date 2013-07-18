sub average{
        my ($data) = @_;
        if (not @$data) {
                die("Empty array\n");
        }
         $total = 0;
        foreach (@$data) {
                $total += $_;
        }
         $average = $total / @$data;
        return $average;
}
sub stdev{
        ($data) = @_;
        if(@$data == 1){
                return 0;
        }
         $average = &average($data);
         $sqtotal = 0;
        foreach(@$data) {
                $sqtotal += ($average-$_) ** 2;
        }
         #$std = ($sqtotal / (@$data-1)) ** 0.5;
         $std = ($sqtotal / (@$data)) ** 0.5;
		$stder = $std /((@$data) ** 0.5);
        return $stder;

}



#$labelmapfile = shift;
#$labelsfile = shift;
#$outFile=`cat fold$i/lastout.txt`;
$outFile= shift;
$dir = shift;
$d = shift; 
$labelmapfile = "./$dir/labelmap.txt";
$labelsfile = '../../scene_processing/labels.txt';
$c = 1;
%lmap=();
%LabelNums = ();
%labels= ();

#### labels
%actLables = ();
open(F,'classmap.txt');
$count = 0;
while(<F>){
  chomp();
  $count ++;
  $actLabels{$count} = $_; 
}
close(F);

$numAct = keys(%actLabels);

%objLabels = ();
open(F,'affmap.txt');
$count = 0;
while(<F>){
  chomp();
  $count++;
  $objLabels{$count} = $_;
}
close(F);

$numAff = keys(%objLabels);

my %avgP = ();
my %avgLP = ();
my %avgLR = ();
my %LTC = ();
my %TC = ();
my %avgR = ();
#### object results 
{
  %pr = ();
  %lpr = ();
  %tc = ();
  %ltc = ();
  %pc = ();
  %lpc = ();
  %tp = ();
  %ltp = ();
  %rc = ();
  %lrc = ();
  # read all info
  for ( $i = 1; $i<= 4; $i++) 
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
    $line =  `grep "^prec: " objfile`   ;
    chomp ($line);

    #print "\n$line\n";
    $line =~ s/(prec:  )(.*)( recall:  )(.*)( tp:  )(.*)(  pc:  )(.*)( tc:  )(.*)/\1/; 
     #print "$2,$4,$6,$8,$10\n";
    if ($line eq ""){print "WARN: fold $i not present\n";}
    $pr{$i} = $2;
    $rc{$i} = $4;
    $tp{$i} = $6;
    $tc{$i} = $10;
    $pc{$i} = $8;
    $labellines = `grep "^label " objfile`; 
    @labells = split/\n/,$labellines;
    foreach $label (@labells){
     chomp($label);
     #print "$label\n";
     $label =~ s/([^\d]*)(\d+)(  .*)/\2/;  
     #print "$label\n";
     $LabelNums{$label} =1; 
     $rest = $3;
     #print "\n$rest\n";
     $rest =~ s/(  prec:  )(.*)(  recall:  )(.*)(  tp:  )(.*)(  tc:  )(.*)(  pc:  )(.*)/\1/; 
     
     #print "$2,$4,$6,$8,$10\n";
     $lpr{$i}{$label} = $2;
     $lrc{$i}{$label} = $4;
     $ltp{$i}{$label} = $6;
     $ltc{$i}{$label} = $8;
     $lpc{$i}{$label} = $10;
     #print "$label $lpr $lrc\n"; 
    }
  }
  
  $tc_a = 0;
  $tp_a = 0;
  $pc_a = 0;
  @pr_values = ();
  @rc_values = ();
   
  # compute micro averaged precision recall 
  for  ( $i = 1; $i<= 4; $i++) 
  {
     $tc_a+= $tc{$i}; 
     $tp_a+= $tp{$i};
     $pc_a+= $pc{$i};
     push(@pr_values,$pr{$i});
     push(@rc_values,$rc{$i});

  }
  print "Micro avg pr = ".&average(\@pr_values)." stdev: " .&stdev(\@pr_values) . "\n";
  print "Micro avg rc = ".&average(\@rc_values). " stdev: " .&stdev(\@rc_values) ."\n";

  @pr_values = ();
  @rc_values = ();
  for  ( $i = 1; $i<= 4; $i++)
  {
    @lpr_values = ();
    @lrc_values = ();

    for $l (keys %LabelNums)
    {
       if($ltc{$i}{$l} != 0){
       push(@lpr_values,$lpr{$i}{$l});
       push(@lrc_values,$lrc{$i}{$l});}
    }
    push(@pr_values,&average(\@lpr_values));
    push(@rc_values,&average(\@lrc_values));
  }
  print "Macro avg pr = ".&average(\@pr_values)." stdev: " .&stdev(\@pr_values) . "\n";
  print "Macro avg rc = ".&average(\@rc_values). " stdev: " .&stdev(\@rc_values) ."\n";



  # 
  # precision = tp/pc
  # recall = tp/tc 
  $TC{$c} = $tc_a;
  if($pc_a !=0 ) {  $avgP{$c} =  $tp_a*100/$pc_a; } else {$avgP{$c} = 0;}
  if($tc_a !=0) { $avgR{$c} = $tp_a*100/$tc_a; } else { $avgR{$c} = 0;}
  for $l (keys %LabelNums){
    #print "$labels{$lmap{$l}}:\n";
    $tc_a = 0;
    $tp_a = 0;
    $pc_a = 0; 
    # compute micro averaged precision recall 
    for  ( $i = 1; $i<= 4; $i++) 
    {
       #print "$i\t$ltp{$i}{$l}\t$ltc{$i}{$l}\t$lpc{$i}{$l}\n";
       $tc_a+= $ltc{$i}{$l}; 
       $tp_a+= $ltp{$i}{$l};
       $pc_a+= $lpc{$i}{$l};
    }
    $LTC{$c}{$l} = $tc_a;
    print "$objLabels{$l}\t$tp_a\t$tc_a\t$pc_a\n";
    if($pc_a !=0) { $avgLP{$c}{$l} =  $tp_a*100/$pc_a; } else {$avgLP{$c}{$l} =0;}
    if($tc_a !=0) { $avgLR{$c}{$l} = $tp_a*100/$tc_a; } else {$avgLR{$c}{$l} = 0;}

  }  

}

print "Micro Averaged Precision Recall:\n";

for $c (sort {$avgP{$a} <=> $avgP{$b} }  keys %avgP)
{
  printf "%.2f\tprec: %.2f\trecall: %.2f\ttc: %d\n",$c,$avgP{$c},$avgR{$c},$TC{$c};
}
print "\n\n---------\n\n";
for $c (sort {$a<=> $b} keys %avgLP)
{
  for $l (sort {$avgLP{$c}{$b} <=> $avgLP{$c}{$a} }  keys %{$avgLP{$c}})
  {
    printf ("%-20s\tprec: %.2f\trecall: %.2f\ttc: %d\n" , $objLabels{$l} , $avgLP{$c}{$l}, $avgLR{$c}{$l}, $LTC{$c}{$l}) ;
    #print "$l\t\t\tprec: $avgLP{$c}{$l}\trecall: $avgLR{$c}{$l}\n";
  }
  print "\n\n";
}


print "Macro Averaged Precision Recall:\n";
{
  $p = 0;
  $r = 0;
  $count = 0;
  for $l (keys %{$avgLP{$c}})
  {
     $count++;
     $p += $avgLP{$c}{$l};
     $r+= $avgLR{$c}{$l};
  }
  printf "%.2f\tprec: %.2f\trecall: %.2f\n",$c,$p/$count,$r/$count;
}
# activity results:
%LabelNums = ();
my %avgP = ();
my %avgLP = ();
my %avgLR = ();
my %LTC = ();
my %TC = ();
my %avgR = ();
{
  %pr = ();
  %lpr = ();
  %tc = ();
  %ltc = ();
  %pc = ();
  %lpc = ();
  %tp = ();
  %ltp = ();
  %rc = ();
  %lrc = ();

  for ( $i = 1; $i<= 4; $i++) 
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
    $cmd = "sed -n \'$linenum2,$totalnum p\' ./$dir/fold$i/pred/$outFile > actfile"  ;
    system($cmd);
    $line =  `grep "^prec: " actfile`   ;
    chomp ($line);

    #print "\n$line\n";
    $line =~ s/(prec:  )(.*)( recall:  )(.*)( tp:  )(.*)(  pc:  )(.*)( tc:  )(.*)/\1/; 
     #print "$2,$4,$6,$8,$10\n";
    if ($line eq ""){print "WARN: fold $i not present\n";}
    $pr{$i} = $2;
    $rc{$i} = $4;
    $tp{$i} = $6;
    $tc{$i} = $10;
    $pc{$i} = $8;
    $labellines = `grep "^label " actfile`; 
    @labells = split/\n/,$labellines;
    foreach $label (@labells){
     chomp($label);
     #print "$label\n";
     $label =~ s/([^\d]*)(\d+)(  .*)/\2/;  
     #print "$label\n";
     $LabelNums{$label} =1; 
     $rest = $3;
     #print "\n$rest\n";
     $rest =~ s/(  prec:  )(.*)(  recall:  )(.*)(  tp:  )(.*)(  tc:  )(.*)(  pc:  )(.*)/\1/; 
     
     #print "$2,$4,$6,$8,$10\n";
     $lpr{$i}{$label} = $2;
     $lrc{$i}{$label} = $4;
     $ltp{$i}{$label} = $6;
     $ltc{$i}{$label} = $8;
     $lpc{$i}{$label} = $10;
     #print "$label $lpr $lrc\n"; 
    }
  }
  
  $tc_a = 0;
  $tp_a = 0;
  $pc_a = 0;
  @pr_values = ();
  @rc_values = ();
   
  # compute micro averaged precision recall 
  for  ( $i = 1; $i<= 4; $i++) 
  {
     $tc_a+= $tc{$i}; 
     $tp_a+= $tp{$i};
     $pc_a+= $pc{$i};
     push(@pr_values,$pr{$i});
     push(@rc_values,$rc{$i});
  }
  print "Micro avg pr = ".&average(\@pr_values)." stdev: " .&stdev(\@pr_values) . "\n";
  print "Micro avg rc = ".&average(\@rc_values). " stdev: " .&stdev(\@rc_values) ."\n";

  @pr_values = ();
  @rc_values = ();
  for  ( $i = 1; $i<= 4; $i++)
  {
    @lpr_values = ();
    @lrc_values = ();

    for $l (keys %LabelNums)
    {
       push(@lpr_values,$lpr{$i}{$l});
       push(@lrc_values,$lrc{$i}{$l});
    }
    push(@pr_values,&average(\@lpr_values));
    push(@rc_values,&average(\@lrc_values));
  }
  print "Macro avg pr = ".&average(\@pr_values)." stdev: " .&stdev(\@pr_values) . "\n";
  print "Macro avg rc = ".&average(\@rc_values). " stdev: " .&stdev(\@rc_values) ."\n";


  # 
  # precision = tp/pc
  # recall = tp/tc 
  $TC{$c} = $tc_a;
  if($pc_a !=0 ) {  $avgP{$c} =  $tp_a*100/$pc_a; } else {$avgP{$c} = 0;}
  if($tc_a !=0) { $avgR{$c} = $tp_a*100/$tc_a; } else { $avgR{$c} = 0;}
  for $l (keys %LabelNums){
    #print "$labels{$lmap{$l}}:\n";
    $tc_a = 0;
    $tp_a = 0;
    $pc_a = 0; 
    # compute micro averaged precision recall 
    for  ( $i = 1; $i<= 4; $i++) 
    {
       #print "$i\t$ltp{$i}{$l}\t$ltc{$i}{$l}\t$lpc{$i}{$l}\n";
       $tc_a+= $ltc{$i}{$l}; 
       $tp_a+= $ltp{$i}{$l};
       $pc_a+= $lpc{$i}{$l};
    }
    $LTC{$c}{$l} = $tc_a;
    print "$actLabels{$l}\t$tp_a\t$tc_a\t$pc_a\n";
    if($pc_a !=0) { $avgLP{$c}{$l} =  $tp_a*100/$pc_a; } else {$avgLP{$c}{$l} =0;}
    if($tc_a !=0) { $avgLR{$c}{$l} = $tp_a*100/$tc_a; } else {$avgLR{$c}{$l} = 0;}

  }  

}

print "Micro Averaged Precision Recall:\n";

for $c (sort {$avgP{$a} <=> $avgP{$b} }  keys %avgP)
{
  printf "%.2f\tprec: %.2f\trecall: %.2f\ttc: %d\n",$c,$avgP{$c},$avgR{$c},$TC{$c};
}
print "\n\n---------\n\n";
for $c (sort {$a<=> $b} keys %avgLP)
{
  for $l (sort {$avgLP{$c}{$b} <=> $avgLP{$c}{$a} }  keys %{$avgLP{$c}})
  {
    printf ("%-20s\tprec: %.2f\trecall: %.2f\ttc: %d\n" , $actLabels{$l} , $avgLP{$c}{$l}, $avgLR{$c}{$l}, $LTC{$c}{$l}) ;
    #print "$l\t\t\tprec: $avgLP{$c}{$l}\trecall: $avgLR{$c}{$l}\n";
  }
  print "\n\n";
}


print "Macro Averaged Precision Recall:\n";
{
  $p = 0;
  $r = 0;
  $count = 0;
  for $l (keys %{$avgLP{$c}})
  {
     $count++;
     $p += $avgLP{$c}{$l};
     $r+= $avgLR{$c}{$l};
  }
  printf "%.2f\tprec: %.2f\trecall: %.2f\n",$c,$p/$count,$r/$count;
}

