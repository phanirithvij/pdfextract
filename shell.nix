{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
  treefmt-nix ? import sources.treefmt-nix,
  lib ? pkgs.lib,
  ...
}:
let
  # IFD HAHAHA
  pkgs' = import (pkgs.applyPatches {
    name = "nixpkgs-patched-pymupdf";
    src = sources.nixpkgs;
    patches = [
      (pkgs.fetchpatch2 {
        url = "https://github.com/NixOS/nixpkgs/pull/334596.diff?full_index=1";
        hash = "sha256-NBS9dKXJUVhgTQUjKggXH4wMS3xGTYb77VKghcb0qgQ=";
      })
    ];
  }) { };
  treefmtCfg = (treefmt-nix.evalModule pkgs ./treefmt.nix).config.build;
in
pkgs.mkShellNoCC {
  packages = [
    (pkgs'.python3.withPackages (
      pp: with pp; [
        pymupdf
        icecream
        python-magic
      ]
    ))
    pkgs.npins
    treefmtCfg.wrapper
    (lib.attrValues treefmtCfg.programs)
  ];
}
