{
  sources ? import ./npins,
  pkgs ? import sources.nixpkgs { },
  treefmt-nix ? import sources.treefmt-nix,
  lib ? pkgs.lib,
  ...
}:
let
  treefmtCfg = (treefmt-nix.evalModule pkgs ./treefmt.nix).config.build;
in
pkgs.mkShellNoCC {
  venvDir = "./venv";
  buildInputs = with pkgs.python3Packages; [
    venvShellHook
    python
    pymupdf
    icecream
  ];
  packages = [
    pkgs.npins
    treefmtCfg.wrapper
    (lib.attrValues treefmtCfg.programs)
  ];
}
