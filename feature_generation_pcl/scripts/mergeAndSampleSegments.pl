$DIR=shift;
%segE = ();
%segS = ();
%framemap = ();
%labelmap = ();
@files = ("$DIR/labeling.txt");
for $f (@files){
  #print $f."\n";
  open(F,$f);
  $count = 0;
  $flag = 1;
  $lid = 0;
  $e = 0;
  $le = 0;
  while(<F>){
    chomp;
    ($id,$s,$e,@r) = split/,/,$_;
    if($id ne $lid && $flag !=1){
      $count = 0;
    }
    $lid = $id;
    $flag++;
    $count++;
    for ($i = $s ; $i<=$e ; $i++){
     $framemap{$id}{$i} = $count;
     $labelmap{$id}{$count} = join( ',', @r);
    }
    $segS{$id}{$count} = $s;
    $segE{$id}{$count} = $e;
  }
  close(F);
}

#### Merging segments
open(OF,">Segmentation_merged.txt");

%segCount = ();
open (F,"Segmentation.txt");
while(<F>){
  chomp();
  %fmap = ();
  ($id, @a ) = split/;/, $_;
  print OF "$id;";
  $segCount{$id} = scalar @a;
  $maxsid = 0;
  for $s (@a){
    ($sid , $frames) = split/:/, $s;
    (@f) = split/,/, $frames;
    $fmap{$sid} = [@f];
    if($sid > $maxsid) {$maxsid = $sid;}
  }
  for ($k = 2; $k <= $maxsid; $k++){
    if(exists $fmap{$k}){
    if(scalar @{$fmap{$k}} < 4){
      # merge this segment to the previous segment
      $p = $k;
      do{ 
        $p = $p-1;
      } while ($p>0 && !exists $fmap{$p});
      if (exists $fmap{$p}){
         push (@{$fmap{$p}}, @{$fmap{$k}});
         delete $fmap{$k};
      }
 #     print "deleted : $id,$k\n";
       
    }
    }
  }
  # also merge segment 1 to later segment
  if(exists $fmap{1} && scalar @{$fmap{1}} < 4){
    $n = 1; 
    do{ 
      $n = $n+1;
    } while ($n<= $maxsid && !exists $fmap{$n});
    if (exists $fmap{$n}){
       unshift (@{$fmap{$n}}, @{$fmap{1}});
       delete $fmap{1};
    }
  }
  for $k (sort {$a<=>$b} keys %fmap ){
    print  OF "$k:$fmap{$k}[0]";
    @a = @{$fmap{$k}};
    for($i = 1; $i <= $#a; $i++ ){
      print OF ",$a[$i]";
    }
    print OF  ";"
  }
  
 print OF "\n";
}
close(F);
close(OF);

##### Sampling

%segCount = ();
$flag = 1;
open (OF2,">Segmentation_labeling.txt");
open (OF3,">Segmentation_merged_labeled.txt");
open (OF,">Segmentation_sampled.txt");
open (F,"Segmentation_merged.txt");
while(<F>){
  chomp();
  ($id, @a ) = split/;/, $_;
      print OF "$id;";
      print OF3 "$id;";
  $lastframe = 0;
  $count = 0; 
  $segCount{$id} = scalar @a;
  for $s (@a){
    ($sid , $frames) = split/:/, $s;
     #print "sid: $sid\n";
    (@f) = split/,/, $frames;
    $lfn  =0;
    $labeled = 0;
    %labelCount = ();
    for $fn ( @f ){
      #if(exists $framemap{$id}{$fn}) {$labeled = 1;}
      if(exists $framemap{$id}{$fn}) {$labeled = 1; $labelCount{$framemap{$id}{$fn}} ++ ;}
      if($fn < $lfn) {print "ERROR!! $fn, $lfn\n";}
      $lfn = $fn;
    }
    $lastframe = $f[$#f];
    if($labeled == 1){
    $count ++;

    @t = sort {$labelCount{$b}<=> $labelCount{$a}}  keys %labelCount;
    $label =  $labelmap{$id}{$t[0]};
    print OF2 "$id,$count,$label\n";

    print OF3 "$count:$f[0]";
    for($i = 1; $i < scalar (@f) ; $i ++ ) {print OF3 ",$f[$i]"}
    
    if(scalar @f <= 5){
      print OF "$count:$f[0]";
      for ($i = 1; $i < scalar (@f) ; $i ++ ) {print OF ",$f[$i]"}
    }
    elsif(scalar @f <= 10){
      print OF "$count:$f[0]";
      for ($i = 2; $i < scalar (@f) ; $i += 2 ) {print OF ",$f[$i]"}
    }
    elsif(scalar @f <= 15){
      print OF "$count:$f[0]";
      for ($i = 3; $i < scalar (@f) ; $i += 3 ) {print OF ",$f[$i]"}
    }
    else{
      print OF "$count:$f[0]";
      for ($i = 5; $i < scalar (@f) ; $i += 5) {print OF ",$f[$i]"}
    }
    print OF ";";
    print OF3 ";";
    }
  }
  $count ++;
  #$lastframe ++;
  print OF "$count:$lastframe;";
  print OF "\n";
  print OF3 "$count:$lastframe;";
  print OF3 "\n";
}
close(F);
close(OF);
close(OF2);
close(OF3);

