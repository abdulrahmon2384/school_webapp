{ pkgs }: {
  deps = [
    pkgs.select username from student limit 5;
    pkgs.select username from student limit 5;
    pkgs.cd instance 
    pkgs.sqlite.bin
    pkgs.tree
  ];
}