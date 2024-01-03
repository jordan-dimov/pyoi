PROGRAM PROBLEM ;

Var
  box,box1    : array [1..1000] of char ;
  st,stt      : array [1..1000] of byte ;
  spn,n,max   : integer ;
  em, em1, mm : integer ;
  flag        : boolean ;

PROCEDURE INPUT ;
var i: integer ;
begin
  em := 0 ;
  write ('n = ') ;
  readln (n) ;
  writeln ;
  for i := 1 to 2*n do
    begin
      write ('box ',i,' ') ;
      readln (box[i]) ;
      box1[i] := box[i] ;
      if (box[i]='O') and (em=0) then em := 1 ;
    end ;
  em1 := em ;
end ;

FUNCTION CHECK : boolean ;
var i   : integer ;
    lst : char ;
    f1  : boolean ;
begin
  f1 := true ;
  lst := box1[1] ;
  for i := 2 to 2*n do
    begin
      if (box1[i]='a') and (lst='b') then f1 := false ;
      if box1[i]<>'O' then lst := box1[i] ;
    end ;
  check := f1 ;
end ;

PROCEDURE PRINT ;
var i: integer ;
begin
  for i := 1 to 2*n do
    write (box1[i],' ') ;
  writeln ;
end ;

PROCEDURE MOVE (pos:integer) ;
begin
  spn := spn + 1;
  box1[em1] := box1[pos] ;
  box1[em1+1] := box1[pos+1] ;
  box1[pos] := 'O' ;
  box1[pos+1] := 'O' ;
  em1 := pos ;
  print ;
end ;

PROCEDURE MOVE1 (pos:integer) ;
begin
  spn := spn + 1;
  box1[em1] := box1[pos] ;
  box1[em1+1] := box1[pos+1] ;
  box1[pos] := 'O' ;
  box1[pos+1] := 'O' ;
  em1 := pos;
  st[spn] := pos ;
end ;

PROCEDURE FINDWAY ;
var k,t  : integer ;
    flag : boolean ;
begin
  spn := 0;
  k := 0;
  while (not check) and (k < n-1) do
    begin
      if box1[k+1]='a' then k := k+1
    else begin
      if box1[k+1]='b' then
        if box1[k+2]<>'O' then move (k+1)
          else begin
            move (em1+2) ;
            move (k+1) ;
          end ;
      t:=k+1 ;
      repeat
        t := t+1 ;
      until box1[t]='a' ;
      if t < 2*n then move (t)
        else begin
          move (t-1) ;
          move (k+2) ;
          move (k+4) ;
          move (k+1) ;
          if (not check) then
            move (2*n-1) ;
        end ;
      k := k+1;
    end ;
  end ;
end ;

PROCEDURE BACK ;
var i,j : integer ;
begin
  em1 := em ;
  for i := 1 to 2*n do
    box1[i] := box[i] ;
    j := spn-1 ; spn := 0 ;
    if j = 0 then flag := false
      else begin
        for i := 1 to j do
          move1 (st[i]) ;
      end ;
end ;

PROCEDURE FORWRD ;
var i,t : integer ;
begin
  if spn<mm then
    begin
      t:=1 ;
      while (box1[t]='O') or (box1[t+1]='O') do
        t := t+1 ;
      move1(t) ;
    end
    else begin
      repeat
        t := st[spn] ;
        back ;
        repeat
          t := t+1 ;
        until (t=2*n) or ((box1[t]<>'O') and (box1[t+1]<>'O')) ;
        if t<2*n then flag := true ;
      until (t<2*n) or (not flag) ;
      if t<2*n then move1(t) ;
    end ;
end ;

PROCEDURE FINDMIN ;
var i : integer ;
begin
  if check then begin
    mm := spn ;
    em1 := em ;
    for i := 1 to 2*n do
      box1[i] := box[i] ;
    max := mm+1 ;
    spn := 0;
    flag := true ;
    while (flag) and (spn<=mm) do
      if check then
        begin
          if max>spn then
            begin
              max := spn ;
              for i := 1 to max do
                stt[i] := st[i] ;
              mm := max ;
            end ;
          forwrd ;
        end
        else forwrd ;
    writeln ;
    writeln (max) ;
    for i := 1 to 2*n do
      box1[i] := box[i] ;
    em1 := em ;
    print ;
    for i := 1 to max do
      move (stt[i]) ;
  end
  else writeln ('no way') ;
end ;

BEGIN
  input ;
  print ;
  findway ;
  findmin ;
END.
