%matrixes
%adding things for tests

if type==1
    
% type alpha' under construction
%# START OF poly(dG)-poly(dC) or poly(dA)-poly(dT)
%*(1-0.5*rand+0.25)
%*(1-0.05*rand+0.025)
  for k1=1:MD
       for k2=k1:MD 
       if k1==k2
             if mod(k1,3)==1
                  ESpeiragmeno=ES;
                   A(k1,k2)= ESpeiragmeno;  % 
             elseif mod(k1,3)==2            
                EGkCPeiragmeno=EGkC;
                   A(k1,k2)= EGkCPeiragmeno; % EGkC;
             elseif mod(k1,3)==0
                    ESpeiragmeno=ES;
                   A(k1,k2)= ESpeiragmeno;  
             end
         elseif mod(k1,3)==2 & mod(k2,3)==2 & abs(k1-k2)==3 
             A(k1,k2)= tGG;   % tGG 
         elseif mod(k1,3)==1 & mod(k2,3)==2 & abs(k1-k2)==1%0.02  
             A(k1,k2)= tS;    % tS
         elseif mod(k1,3)==2 & mod(k2,3)==1 & abs(k1-k2)==1%0.02
             A(k1,k2)= tS;    % tS
         elseif mod(k1,3)==0 & mod(k2,3)==2 & abs(k1-k2)==1%0.16 
             A(k1,k2)= tS;    % tS
         elseif mod(k1,3)==2 & mod(k2,3)==0 & abs(k1-k2)==1%0.16
             A(k1,k2)= tS;    % tS
         else
             A(k1,k2)= 0.0;
         end
       end 
       end 
        for k1=1:MD
         for k2=1:k1-1
             A(k1,k2)=A(k2,k1);
          end
         end