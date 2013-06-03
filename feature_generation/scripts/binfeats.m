dataN = load('data_obj_feats.txt');
offset=5
numFeats=size(dataN,2)-offset;
numFeatsBinned=numFeats*10;
dataNB=zeros(size(dataN,1),offset+numFeatsBinned);
dataNB(:,1:offset) = dataN(:,1:offset);
binStumps=zeros(10,numFeats);
for f = offset+1:size(dataN,2)
  binv=getBinStumps(dataN(:,f),10);
  binStumps(:,f-offset)=binv;
  
  for b =1:10
    dataNB(:,offset+b+(f-offset-1)*10) = (dataN(:,f)<=binv(b));
  end
  
end
dlmwrite('binStumpsObj.txt',binStumps','\t')
dlmwrite('data_obj_feats.b.txt',dataNB,'delimiter',',','precision','%d')


dataN = load('data_obj_obj_feats.txt');
offset=4
numFeats=size(dataN,2)-offset;
numFeatsBinned=numFeats*10;
dataNB=zeros(size(dataN,1),offset+numFeatsBinned);
dataNB(:,1:offset) = dataN(:,1:offset);
binStumps=zeros(10,numFeats);
for f = offset+1:size(dataN,2)
  binv=getBinStumps(dataN(:,f),10);
  binStumps(:,f-offset)=binv;
  
  for b =1:10
    dataNB(:,offset+b+(f-offset-1)*10) = (dataN(:,f)<=binv(b));
  end
  
end
dlmwrite('binStumpsObjObj.txt',binStumps','\t')
dlmwrite('data_obj_obj_feats.b.txt',dataNB,'delimiter',',','precision','%d')


dataN = load('data_skel_feats.txt');
offset=2
numFeats=size(dataN,2)-offset;
numFeatsBinned=numFeats*10;
dataNB=zeros(size(dataN,1),offset+numFeatsBinned);
dataNB(:,1:offset) = dataN(:,1:offset);
binStumps=zeros(10,numFeats);
for f = offset+1:size(dataN,2)
  binv=getBinStumps(dataN(:,f),10);
  binStumps(:,f-offset)=binv;
  
  for b =1:10
    dataNB(:,offset+b+(f-offset-1)*10) = (dataN(:,f)<=binv(b));
  end
  
end
dlmwrite('binStumpsSkel.txt',binStumps','\t')
dlmwrite('data_skel_feats.b.txt',dataNB,'delimiter',',','precision','%d')


dataN = load('data_skel_obj_feats.txt');
offset=3
numFeats=size(dataN,2)-offset;
numFeatsBinned=numFeats*10;
dataNB=zeros(size(dataN,1),offset+numFeatsBinned);
dataNB(:,1:offset) = dataN(:,1:offset);
binStumps=zeros(10,numFeats);
for f = offset+1:size(dataN,2)
  binv=getBinStumps(dataN(:,f),10);
  binStumps(:,f-offset)=binv;
  
  for b =1:10
    dataNB(:,offset+b+(f-offset-1)*10) = (dataN(:,f)<=binv(b));
  end
  
end
dlmwrite('binStumpsSkelObj.txt',binStumps','\t')
dlmwrite('data_skel_obj_feats.b.txt',dataNB,'delimiter',',','precision','%d')


dataN = load('data_temporal_obj_feats.txt');
offset=4
numFeats=size(dataN,2)-offset;
numFeatsBinned=numFeats*10;
dataNB=zeros(size(dataN,1),offset+numFeatsBinned);
dataNB(:,1:offset) = dataN(:,1:offset);
binStumps=zeros(10,numFeats);
for f = offset+1:size(dataN,2)
  binv=getBinStumps(dataN(:,f),10);
  binStumps(:,f-offset)=binv;
  
  for b =1:10
    dataNB(:,offset+b+(f-offset-1)*10) = (dataN(:,f)<=binv(b));
  end
  
end
dlmwrite('binStumpsTemporalObj.txt',binStumps','\t')
dlmwrite('data_temporal_obj_feats.b.txt',dataNB,'delimiter',',','precision','%d')


dataN = load('data_temporal_skel_feats.txt');
offset=3
numFeats=size(dataN,2)-offset;
numFeatsBinned=numFeats*10;
dataNB=zeros(size(dataN,1),offset+numFeatsBinned);
dataNB(:,1:offset) = dataN(:,1:offset);
binStumps=zeros(10,numFeats);
for f = offset+1:size(dataN,2)
  binv=getBinStumps(dataN(:,f),10);
  binStumps(:,f-offset)=binv;
  
  for b =1:10
    dataNB(:,offset+b+(f-offset-1)*10) = (dataN(:,f)<=binv(b));
  end
  
end
dlmwrite('binStumpsTemporalSkel.txt',binStumps','\t')
dlmwrite('data_temporal_skel_feats.b.txt',dataNB,'delimiter',',','precision','%d')


quit
