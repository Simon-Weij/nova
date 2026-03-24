{
  inputs.flakelight.url = "github:nix-community/flakelight";
  outputs = {flakelight, ...}:
    flakelight ./. {
      devShell = {
        packages = pkgs: [
          pkgs.python313
          pkgs.uv
          pkgs.fastapi-cli
          pkgs.python313Packages.fastapi
          pkgs.nodejs_24
          pkgs.portaudio
          pkgs.pkg-config
        ];

        shellHook = pkgs: ''
          export C_INCLUDE_PATH="${pkgs.portaudio}/include"
          export LIBRARY_PATH="${pkgs.portaudio}/lib"
        '';
      };
    };
}
