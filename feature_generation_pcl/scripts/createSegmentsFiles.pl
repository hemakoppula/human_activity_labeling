$home=shift;
$method=shift;
$dir = "$home/object_affordance_detection/svm-python-v204/data-all/alldata-fixed/".$method;

#$r = `ls 1*.txt`;
$r = `ls *.txt | grep "^[1|0].*"`;

%framefiles = ();
%edgefiles  = ();
@files = split /\n/,$r;
print scalar @files;

for $f (@files){

  (@c) = split /_/,$f;
  if(scalar @c == 2) {
    ($fnum,$w) = split /\./,$c[1];
    $framefiles{$c[0]}{$fnum} = $f; 
  }
  if(scalar @c == 3) {
    ($fnum,$w) = split /\./,$c[2];
    $edgefiles{$c[0]}{$c[1]}{$fnum} = $f; 
  }

}

for $f (keys %framefiles){
  open(F,">segments/$f.txt");
  $s1 = keys %{$framefiles{$f}};
  $s2 = keys %{$edgefiles{$f}};
  print F "$s1 $s2\n";
  for $k ( sort {$a<=>$b}  keys %{$framefiles{$f}} ){
     print F "$dir/$framefiles{$f}{$k}\n";
     print  "$k $framefiles{$f}{$k}\n";
  }
  for $k ( sort {$a<=>$b}  keys %{$edgefiles{$f}} ){
    for $l ( sort {$a<=>$b}  keys %{$edgefiles{$f}{$k}} ){
     print F "$dir/$edgefiles{$f}{$k}{$l}\n";
    }
  }
  close(F); 
}
