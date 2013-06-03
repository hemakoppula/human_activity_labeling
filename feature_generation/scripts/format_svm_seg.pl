
$activityfile = "../data/activityLabel.txt";
$labelfile = shift;
$dir = shift;
$binary = shift;
$data_obj = "./$dir/data_obj_feats.txt";
$data_obj_obj = "./$dir/data_obj_obj_feats.txt";
$data_skel = "./$dir/data_skel_feats.txt";
$data_skel_obj = "./$dir/data_skel_obj_feats.txt";
$data_obj_temporal = "./$dir/data_temporal_obj_feats.txt";
$data_skel_temporal = "./$dir/data_temporal_skel_feats.txt";

if ($binary == 1){
$data_obj = "./$dir/data_obj_feats.b.txt";
$data_obj_obj = "./$dir/data_obj_obj_feats.b.txt";
$data_skel = "./$dir/data_skel_feats.b.txt";
$data_skel_obj = "./$dir/data_skel_obj_feats.b.txt";
$data_obj_temporal = "./$dir/data_temporal_obj_feats.b.txt";
$data_skel_temporal = "./$dir/data_temporal_skel_feats.b.txt";
}
$outfile="out.txt";


%classmap = ();
open(F,"classmap.txt");
$count = 0;
while(<F>){
  chomp();
  $count ++;
  $classmap{$_} = $count;
}
close(F);
$numAct = keys(%classmap);

%affmap = ();;
open(F,"affmap.txt");
$count = 0;
while(<F>){
  chomp();
  $count++;
  $affmap{$_} = $count;
}
close(F);
$numAff = keys(%affmap) ;

%skelFeatMap=();
%objFeatMap=();
%objTFeatMap=();
%skelTFeatMap=();
%objObjFeatMap=();
%skelObjFeatMap=();



open(F,$data_skel);
while(<F>){
  chomp;
  ($sn,$fn,@feats) = split/,/,$_;
  if(length ($sn) < 10) {$sn = '0'.$sn;}
  #$f = join(',',@feats); 
  #$skelFeatMap{$sn}{$fn} = $f;
  push( @{$skelFeatMap{$sn}{$fn}} , @feats );
}
close(F);

open(F,$data_obj);
while(<F>){
  chomp;
  ($sn,$fn,$ob,$a,$b,@feats) = split/,/,$_;
  if(length ($sn) < 10) {$sn = '0'.$sn;}
  #if($binary == 1) {$sn = '0'.$sn;}
  #$f = join(',',@feats); 
  #$objFeatMap{$sn}{$fn}{$ob} = $f;
  push( @{$objFeatMap{$sn}{$fn}{$ob}} , @feats );
}
close(F);

open(F,$data_obj_temporal);
while(<F>){
  chomp;
  ($sn,$fn1,$fn2,$ob,@feats) = split/,/,$_;
  if(length ($sn) < 10) {$sn = '0'.$sn;}
  #if($binary == 1) {$sn = '0'.$sn;}
  push( @{$objTFeatMap{$sn}{$fn1}{$fn2}{$ob}} , @feats );
}
close(F);

open(F,$data_skel_temporal);
while(<F>){
  chomp;
  ($sn,$fn1,$fn2,@feats) = split/,/,$_;
  if(length ($sn) < 10) {$sn = '0'.$sn;}
  #if($binary == 1) {$sn = '0'.$sn;}
  push( @{$skelTFeatMap{$sn}{$fn1}{$fn2}} , @feats );
}
close(F);


open(F,$data_skel_obj);
while(<F>){
  chomp;
  ($sn,$fn,$ob,@feats) = split/,/,$_;
  if(length ($sn) < 10) {$sn = '0'.$sn;}
  #if($binary == 1) {$sn = '0'.$sn;}
  #$f = join(',',@feats); 
  #$skelObjFeatMap{$sn}{$fn}{$ob} = $f;
  push( @{$skelObjFeatMap{$sn}{$fn}{$ob}} , @feats );
}
close(F);

open(F,$data_obj_obj);
while(<F>){
  chomp;
  ($sn,$fn,$o1,$o2,@feats) = split/,/,$_;
  if(length ($sn) < 10) {$sn = '0'.$sn;}
  #if($binary == 1) {$sn = '0'.$sn;}
  #$f = join(',',@feats); 
  #$objObjFeatMap{$sn}{$fn}{$o1}{$o2} = $f;
  push( @{$objObjFeatMap{$sn}{$fn}{$o1}{$o2}} , @feats );
}
close(F);


%labelMap = ();
open(F,$labelfile);
while(<F>){
  chomp();
  ($sn,$fn,$act,@aff) = split/,/,$_;
  $labelMap{$sn}{$fn}{'act'} = $act;
  $size = @aff;
  for($i = 0; $i < $size; $i ++){
    $labelMap{$sn}{$fn}{$i+1} = $aff[$i];
  }
}
close(F);

for $sn (keys %objFeatMap)
{

  for $fn (keys %{$objFeatMap{$sn}})
  {
   if(exists $labelMap{$sn}{$fn}){
      $outfile = $sn."_$fn.txt";
      open(OF,">$outfile");
      $N1 = keys(%{$objFeatMap{$sn}{$fn}}); 
      $E1 = 0;
      for $o1 (keys %{$objObjFeatMap{$sn}{$fn}}){
       for $o2 (keys %{$objObjFeatMap{$sn}{$fn}{$o1}}){
        $E1++;
       }
      }
      $E2 = keys(%{$skelObjFeatMap{$sn}{$fn}});
      print OF "$N1 $E1 $E2 $numAff $numAct $fn\n";
      # print obj feats
      for $ob (keys %{$objFeatMap{$sn}{$fn}}){
        print OF "$affmap{$labelMap{$sn}{$fn}{$ob}} $ob";
        @feats = @{$objFeatMap{$sn}{$fn}{$ob}};
        for($i=0;$i<=$#feats;$i++){
          print OF " ".($i+1).":".$feats[$i];
          print  " ".($i+1).":".$feats[$i];
        }
        print OF "\n"; 
        print  "\n"; 
      }
    # print skel feats
      print OF "$classmap{$labelMap{$sn}{$fn}{'act'}} 1";
      @feats = @{$skelFeatMap{$sn}{$fn}};
      for($i=0;$i<=$#feats;$i++){
        print OF " ".($i+1).":".$feats[$i];
        print  " ".($i+1).":".$feats[$i];
      }
      print OF "\n"; 
      print "\n"; 
    # print obj obj feats
      for $o1 (keys %{$objObjFeatMap{$sn}{$fn}}){
      for $o2 (keys %{$objObjFeatMap{$sn}{$fn}{$o1}}){
        print OF "$affmap{$labelMap{$sn}{$fn}{$o1}} $affmap{$labelMap{$sn}{$fn}{$o2}} $o1 $o2";
        @feats = @{$objObjFeatMap{$sn}{$fn}{$o1}{$o2}};
        for($i=0;$i<=$#feats;$i++){
          print OF " ".($i+1).":".$feats[$i];
          print  " ".($i+1).":".$feats[$i];
        }
        print OF "\n";
        print  "\n";
      }
     }
 
    # print skel obj feats
     for $ob (keys %{$skelObjFeatMap{$sn}{$fn}}){
       print OF "$affmap{$labelMap{$sn}{$fn}{$ob}} $classmap{$labelMap{$sn}{$fn}{'act'}} $ob";
       @feats = @{$skelObjFeatMap{$sn}{$fn}{$ob}};
       for($i=0;$i<=$#feats;$i++){
         print OF " ".($i+1).":".$feats[$i];
         print  " ".($i+1).":".$feats[$i];
       }
       print OF "\n";
       print  "\n";
     }
     close(OF);

    }
  }

  for $fn1 (keys %{$objTFeatMap{$sn}})
  {
    for $fn2 (keys %{$objTFeatMap{$sn}{$fn1}})
    {
      $outfile = $sn."_$fn1"."_$fn2.txt";
       print "writing $outfile\n";
      open(OF,">$outfile");
      $e3 = keys( %{$objTFeatMap{$sn}{$fn1}{$fn2}} );
      $e4 = 1 ;# keys( %{$skelTFeatMap{$sn}{$fn1}{$fn2}} );
      print OF "$e3 $e4 $fn1 $fn2\n";
      # print obj obj temporal feats
      for $ob (keys %{$objTFeatMap{$sn}{$fn1}{$fn2}}){
        print OF "$affmap{$labelMap{$sn}{$fn1}{$ob}} $affmap{$labelMap{$sn}{$fn2}{$ob}} $ob";
        @feats = @{$objTFeatMap{$sn}{$fn1}{$fn2}{$ob}};
        for($i=0;$i<=$#feats;$i++){
          print OF " ".($i+1).":".$feats[$i];
          print  " ".($i+1).":".$feats[$i];
        }
        print OF "\n";
        print  "\n";
      }
      # print skel skel temporal feats
        print OF "$classmap{$labelMap{$sn}{$fn1}{'act'}} $classmap{$labelMap{$sn}{$fn2}{'act'}} 1";
        @feats = @{$skelTFeatMap{$sn}{$fn1}{$fn2}};
        for($i=0;$i<=$#feats;$i++){
          print OF " ".($i+1).":".$feats[$i];
          print  " ".($i+1).":".$feats[$i];
        }
        print OF "\n";
        print  "\n";
      

    }
  }


}

