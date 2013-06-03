function [ bin_stumps ] = getBinStumps( values ,numBins )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
  sortedV = sort(values);
  len=length(sortedV)
  binSize = floor(len/(numBins+1))
  curPos=binSize
  bin_stumps=zeros(numBins,1);
  bin_stumps(1) = sortedV(curPos);
  for b = 2:numBins
     index=find(sortedV>bin_stumps(b-1),1);
         if(size(index,1)==0)
              bin_stumps(b:numBins)=bin_stumps(b-1);
             break;
         end
     if(index<=curPos+binSize)
         curPos=curPos+binSize
         bin_stumps(b) = sortedV(curPos);
     else
         curPos=index
         disp('overflow')
         bin_stumps(b) = sortedV(curPos);
         binSize=floor((len-curPos)/(numBins+1-b))
         if(binSize==0)
              bin_stumps(b:numBins)=bin_stumps(b);
             break;
         end
     end
  end
end

