function [data] = filereader(filename,indata)
% filename = 'filename';

fid=fopen(filename);
if fid == -1,
  warning('File does not exist');
  return
end

data = indata;
line = fgetl(fid);
line = fgetl(fid);
line = fgetl(fid);
while 1
    line = fgetl(fid);
    if length(line) <2,
        break
    elseif strncmp('*4',dblnk(line),2)
        break
    end
    strs = transpose(sscanf(line,'%f'));
    linedata = [strs(14),strs(19),strs(1:13),strs(15:18),strs(20:end)]; % organised line
    % if all temp same, not recording
    if isempty(data) == 1
        data = linedata;
    else
        ifeq  = abs(linedata(:,1:3)-data(:,1:3))<0.01;
        ifgt  = linedata(:,1:3)-data(:,1:3)>0.01;
        iflt  = linedata(:,1:3)-data(:,1:3)<0.01;
        logic = sum(ifeq,2)==3; % see which row match temps
        if any(logic) == 1
            data(logic,:) = linedata(:);
        else
%             % determine which line the new line should go
%             ifleq = iflt|ifeq;
%             % case 1 when #1,2 smeq, and #3 sm (eq eliminated previous step)
%             if any(sum(ifleq(:,1:3),2))==3;
%                 lineindex = find(sum(compare(:,1:3),2)==3,1,'last')+1;
%             % case 2 when #1 smeq, #2 eq -> go before,
%             elseif any(sum(compare(:,1:2),2))==2;
%                 lineindex = find(sum(compare(:,1:2),2)==2,1,'last')+1;
%             elseif any(sum(compare(:,1),2))==1;
%                 lineindex = find(sum(compare(:,1),2)==1,1,'last')+1;
%             else
%                 lineindex = 1;
%             end
%             if lineindex == 1
%                 data = [linedata; data];
%             elseif lineindex > length(data)
%                 data = [data; linedata];
%             else
%                 data = [data(1:lineindex-1,:); linedata; data(lineindex:end,:)];
%             end
            data = [data;linedata];
        end
    end
end
data = sortrows(data,[1 2 3]);
fclose(fid);