{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "vit-course-reg-planner-env";

  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.pandas
    pkgs.python312Packages.ics
    pkgs.python312Packages.tkinter
  ];

  shellHook = ''
    echo "Environment ready. Run 'python primary_window.py' to start the GUI."
  '';
}

