{
  description = "A very basic pdf video extractor thing";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.05";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    treefmt-nix.inputs.nixpkgs.follows = "nixpkgs";
  };
  outputs =
    { self, nixpkgs, ... }@inputs:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      treefmtCfg = (inputs.treefmt-nix.lib.evalModule pkgs ./treefmt.nix).config.build;
    in
    {
      # TODO python deps, everything
      packages.${system} = {
        inherit (pkgs) hello;
        default = self.packages.${system}.hello;
      };
      formatter.${system} = treefmtCfg.wrapper;
      checks.${system}.formatting = treefmtCfg.check self;
      devShells.${system}.default = pkgs.mkShell {
        packages =
          with pkgs;
          [
            (python312.withPackages (
              pp: with pp; [
                pip
                pymupdf
                icecream
              ]
            ))
            mupdf
          ]
          ++ [
            statix
            deadnix
            treefmtCfg.wrapper
            (lib.attrValues treefmtCfg.programs)
          ];
      };
    };
}
