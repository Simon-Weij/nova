{
  inputs.flakelight.url = "github:nix-community/flakelight";
  outputs = {flakelight, ...}:
    flakelight ./. {
      devShell = {
        packages = pkgs: [pkgs.python313 pkgs.uv pkgs.fastapi-cli pkgs.python313Packages.fastapi];
      };
    };
}
