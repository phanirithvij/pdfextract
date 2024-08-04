{
  description = "A very basic pdf video extractor thing";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.05";
  };
  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      # TODO python deps, everything
      packages.${system} = {
        hello = pkgs.hello;
        default = self.packages.${system}.hello;
      };
      formatter.${system} = pkgs.nixfmt-rfc-style;
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [ (python3.withPackages (pp: [pp.pymupdf])) nixfmt-rfc-style ];
      };
    };
}
